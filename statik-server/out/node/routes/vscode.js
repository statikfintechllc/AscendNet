"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ensureVSCodeLoaded = exports.wsRouter = exports.router = void 0;
exports.dispose = dispose;
const logger_1 = require("@coder/logger");
const crypto = __importStar(require("crypto"));
const express = __importStar(require("express"));
const fs_1 = require("fs");
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const util_1 = require("../../common/util");
const cli_1 = require("../cli");
const constants_1 = require("../constants");
const http_1 = require("../http");
const socket_1 = require("../socket");
const util_2 = require("../util");
const wsRouter_1 = require("../wsRouter");
exports.router = express.Router();
exports.wsRouter = (0, wsRouter_1.Router)();
/**
 * Load then create the VS Code server.
 */
async function loadVSCode(req) {
    // Since server-main.js is an ES module, we have to use `import`.  However,
    // tsc will transpile this to `require` unless we change our module type,
    // which will also require that we switch to ESM, since a hybrid approach
    // breaks importing `rotating-file-stream` for some reason.  To work around
    // this, use `eval` for now, but we should consider switching to ESM.
    let modPath = path.join(constants_1.vsRootPath, "out/server-main.js");
    if (os.platform() === "win32") {
        // On Windows, absolute paths of ESM modules must be a valid file URI.
        modPath = "file:///" + modPath.replace(/\\/g, "/");
    }
    const mod = (await eval(`import("${modPath}")`));
    const serverModule = await mod.loadCodeWithNls();
    return serverModule.createServer(null, Object.assign(Object.assign({}, (await (0, cli_1.toCodeArgs)(req.args))), { "accept-server-license-terms": true, 
        // This seems to be used to make the connection token flags optional (when
        // set to 1.63) but we have always included them.
        compatibility: "1.64", "without-connection-token": true }));
}
// To prevent loading the module more than once at a time.  We also have the
// resolved value so you do not need to `await` everywhere.
let vscodeServerPromise;
// The resolved value from the dynamically loaded VS Code server.  Do not use
// without first calling and awaiting `ensureCodeServerLoaded`.
let vscodeServer;
/**
 * Ensure the VS Code server is loaded.
 */
const ensureVSCodeLoaded = async (req, _, next) => {
    if (vscodeServer) {
        return next();
    }
    if (!vscodeServerPromise) {
        vscodeServerPromise = loadVSCode(req);
    }
    try {
        vscodeServer = await vscodeServerPromise;
    }
    catch (error) {
        vscodeServerPromise = undefined; // Unset so we can try again.
        (0, util_1.logError)(logger_1.logger, "CodeServerRouteWrapper", error);
        if (constants_1.isDevMode) {
            return next(new Error((error instanceof Error ? error.message : error) +
                " (Have you applied the patches? If so, VS Code may still be compiling)"));
        }
        return next(error);
    }
    return next();
};
exports.ensureVSCodeLoaded = ensureVSCodeLoaded;
exports.router.get("/", exports.ensureVSCodeLoaded, async (req, res, next) => {
    const isAuthenticated = await (0, http_1.authenticated)(req);
    const NO_FOLDER_OR_WORKSPACE_QUERY = !req.query.folder && !req.query.workspace;
    // Ew means the workspace was closed so clear the last folder/workspace.
    const FOLDER_OR_WORKSPACE_WAS_CLOSED = req.query.ew;
    if (!isAuthenticated) {
        const to = (0, http_1.self)(req);
        return (0, http_1.redirect)(req, res, "login", {
            to: to !== "/" ? to : undefined,
        });
    }
    if (NO_FOLDER_OR_WORKSPACE_QUERY && !FOLDER_OR_WORKSPACE_WAS_CLOSED) {
        const settings = await req.settings.read();
        const lastOpened = settings.query || {};
        // This flag disables the last opened behavior
        const IGNORE_LAST_OPENED = req.args["ignore-last-opened"];
        const HAS_LAST_OPENED_FOLDER_OR_WORKSPACE = lastOpened.folder || lastOpened.workspace;
        const HAS_FOLDER_OR_WORKSPACE_FROM_CLI = req.args._.length > 0;
        const to = (0, http_1.self)(req);
        let folder = undefined;
        let workspace = undefined;
        // Redirect to the last folder/workspace if nothing else is opened.
        if (HAS_LAST_OPENED_FOLDER_OR_WORKSPACE && !IGNORE_LAST_OPENED) {
            folder = lastOpened.folder;
            workspace = lastOpened.workspace;
        }
        else if (HAS_FOLDER_OR_WORKSPACE_FROM_CLI) {
            const lastEntry = path.resolve(req.args._[req.args._.length - 1]);
            const entryIsFile = await (0, util_2.isFile)(lastEntry);
            const IS_WORKSPACE_FILE = entryIsFile && path.extname(lastEntry) === ".code-workspace";
            if (IS_WORKSPACE_FILE) {
                workspace = lastEntry;
            }
            else if (!entryIsFile) {
                folder = lastEntry;
            }
        }
        if (folder || workspace) {
            return (0, http_1.redirect)(req, res, to, {
                folder,
                workspace,
            });
        }
    }
    // Store the query parameters so we can use them on the next load.  This
    // also allows users to create functionality around query parameters.
    await req.settings.write({ query: req.query });
    next();
});
exports.router.get("/manifest.json", async (req, res) => {
    const appName = req.args["app-name"] || "code-server";
    res.writeHead(200, { "Content-Type": "application/manifest+json" });
    res.end((0, http_1.replaceTemplates)(req, JSON.stringify({
        name: appName,
        short_name: appName,
        start_url: ".",
        display: "fullscreen",
        display_override: ["window-controls-overlay"],
        description: "Run Code on a remote server.",
        icons: [192, 512]
            .map((size) => [
            {
                src: `{{BASE}}/_static/src/browser/media/pwa-icon-${size}.png`,
                type: "image/png",
                sizes: `${size}x${size}`,
                purpose: "any",
            },
            {
                src: `{{BASE}}/_static/src/browser/media/pwa-icon-maskable-${size}.png`,
                type: "image/png",
                sizes: `${size}x${size}`,
                purpose: "maskable",
            },
        ])
            .flat(),
    }, null, 2)));
});
// Statik Dashboard route - Unified AscendNet AI modules
exports.router.get("/statik-dashboard", http_1.ensureAuthenticated, async (req, res) => {
    try {
        const dashboardPath = path.join(__dirname, "../../browser/pages/statik-dashboard.html");
        const dashboardHtml = await fs_1.promises.readFile(dashboardPath, "utf8");
        // Replace template variables
        const processedHtml = (0, http_1.replaceTemplates)(req, dashboardHtml, {
            title: "Statik-Server - Unified AI Dashboard"
        });
        res.setHeader("Content-Type", "text/html");
        res.send(processedHtml);
    }
    catch (error) {
        logger_1.logger.error("Failed to serve Statik dashboard:", (0, logger_1.field)("error", error));
        res.status(500).send("Dashboard temporarily unavailable");
    }
});
// Dashboard asset routes
exports.router.get("/statik-dashboard.css", async (req, res) => {
    try {
        const cssPath = path.join(__dirname, "../../browser/pages/statik-dashboard.css");
        const cssContent = await fs_1.promises.readFile(cssPath, "utf8");
        res.setHeader("Content-Type", "text/css");
        res.send(cssContent);
    }
    catch (error) {
        res.status(404).send("CSS not found");
    }
});
exports.router.get("/statik-dashboard.js", async (req, res) => {
    try {
        const jsPath = path.join(__dirname, "../../browser/pages/statik-dashboard.js");
        const jsContent = await fs_1.promises.readFile(jsPath, "utf8");
        res.setHeader("Content-Type", "application/javascript");
        res.send(jsContent);
    }
    catch (error) {
        res.status(404).send("JavaScript not found");
    }
});
let mintKeyPromise;
exports.router.post("/mint-key", async (req, res) => {
    if (!mintKeyPromise) {
        mintKeyPromise = new Promise(async (resolve) => {
            const keyPath = path.join(req.args["user-data-dir"], "serve-web-key-half");
            logger_1.logger.debug(`Reading server web key half from ${keyPath}`);
            try {
                resolve(await fs_1.promises.readFile(keyPath));
                return;
            }
            catch (error) {
                if (error.code !== "ENOENT") {
                    (0, util_1.logError)(logger_1.logger, `read ${keyPath}`, error);
                }
            }
            // VS Code wants 256 bits.
            const key = crypto.randomBytes(32);
            try {
                await fs_1.promises.writeFile(keyPath, key);
            }
            catch (error) {
                (0, util_1.logError)(logger_1.logger, `write ${keyPath}`, error);
            }
            resolve(key);
        });
    }
    const key = await mintKeyPromise;
    res.end(key);
});
exports.router.all(/.*/, http_1.ensureAuthenticated, exports.ensureVSCodeLoaded, async (req, res) => {
    vscodeServer.handleRequest(req, res);
});
const socketProxyProvider = new socket_1.SocketProxyProvider();
exports.wsRouter.ws(/.*/, http_1.ensureOrigin, http_1.ensureAuthenticated, exports.ensureVSCodeLoaded, async (req) => {
    const wrappedSocket = await socketProxyProvider.createProxy(req.ws);
    // This should actually accept a duplex stream but it seems Code has not
    // been updated to match the Node 16 types so cast for now.  There does not
    // appear to be any code specific to sockets so this should be fine.
    vscodeServer.handleUpgrade(req, wrappedSocket);
    req.ws.resume();
});
function dispose() {
    vscodeServer === null || vscodeServer === void 0 ? void 0 : vscodeServer.dispose();
    socketProxyProvider.stop();
}
//# sourceMappingURL=vscode.js.map