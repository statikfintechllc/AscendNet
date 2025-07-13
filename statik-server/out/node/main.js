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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runCodeServer = exports.openInExistingInstance = exports.runCodeCli = exports.shouldSpawnCliProcess = void 0;
const logger_1 = require("@coder/logger");
const http_1 = __importDefault(require("http"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const util_1 = require("../common/util");
const app_1 = require("./app");
const cli_1 = require("./cli");
const constants_1 = require("./constants");
const routes_1 = require("./routes");
const util_2 = require("./util");
/**
 * Return true if the user passed an extension-related VS Code flag.
 */
const shouldSpawnCliProcess = (args) => {
    return (!!args["list-extensions"] ||
        !!args["install-extension"] ||
        !!args["uninstall-extension"] ||
        !!args["locate-extension"]);
};
exports.shouldSpawnCliProcess = shouldSpawnCliProcess;
/**
 * Run Code's CLI for things like managing extensions.
 */
const runCodeCli = async (args) => {
    logger_1.logger.debug("Running Code CLI");
    try {
        // See vscode.loadVSCode for more on this jank.
        process.env.CODE_SERVER_PARENT_PID = process.pid.toString();
        let modPath = path.join(constants_1.vsRootPath, "out/server-main.js");
        if (os.platform() === "win32") {
            // On Windows, absolute paths of ESM modules must be a valid file URI.
            modPath = "file:///" + modPath.replace(/\\/g, "/");
        }
        const mod = (await eval(`import("${modPath}")`));
        const serverModule = await mod.loadCodeWithNls();
        await serverModule.spawnCli(await (0, cli_1.toCodeArgs)(args));
        // Rather than have the caller handle errors and exit, spawnCli will exit
        // itself.  Additionally, it does this on a timeout set to 0.  So, try
        // waiting for VS Code to exit before giving up and doing it ourselves.
        await new Promise((r) => setTimeout(r, 1000));
        logger_1.logger.warn("Code never exited");
        process.exit(0);
    }
    catch (error) {
        // spawnCli catches all errors, but just in case that changes.
        logger_1.logger.error("Got error from Code", error);
        process.exit(1);
    }
};
exports.runCodeCli = runCodeCli;
const openInExistingInstance = async (args, socketPath) => {
    const pipeArgs = {
        type: "open",
        folderURIs: [],
        fileURIs: [],
        forceReuseWindow: args["reuse-window"],
        forceNewWindow: args["new-window"],
        gotoLineMode: true,
    };
    for (let i = 0; i < args._.length; i++) {
        const fp = args._[i];
        if (await (0, util_2.isDirectory)(fp)) {
            pipeArgs.folderURIs.push(fp);
        }
        else {
            pipeArgs.fileURIs.push(fp);
        }
    }
    if (pipeArgs.forceNewWindow && pipeArgs.fileURIs.length > 0) {
        logger_1.logger.error("--new-window can only be used with folder paths");
        process.exit(1);
    }
    if (pipeArgs.folderURIs.length === 0 && pipeArgs.fileURIs.length === 0) {
        logger_1.logger.error("Please specify at least one file or folder");
        process.exit(1);
    }
    const vscode = http_1.default.request({
        path: "/",
        method: "POST",
        socketPath,
    }, (response) => {
        response.on("data", (message) => {
            logger_1.logger.debug("got message from Code", (0, logger_1.field)("message", message.toString()));
        });
    });
    vscode.on("error", (error) => {
        logger_1.logger.error("got error from Code", (0, logger_1.field)("error", error));
    });
    vscode.write(JSON.stringify(pipeArgs));
    vscode.end();
};
exports.openInExistingInstance = openInExistingInstance;
const runCodeServer = async (args) => {
    logger_1.logger.info(`code-server ${constants_1.version} ${constants_1.commit}`);
    logger_1.logger.info(`Using user-data-dir ${args["user-data-dir"]}`);
    logger_1.logger.debug(`Using extensions-dir ${args["extensions-dir"]}`);
    if (args.auth === cli_1.AuthType.Password && !args.password && !args["hashed-password"]) {
        throw new Error("Please pass in a password via the config file or environment variable ($PASSWORD or $HASHED_PASSWORD)");
    }
    const app = await (0, app_1.createApp)(args);
    const protocol = args.cert ? "https" : "http";
    const serverAddress = (0, app_1.ensureAddress)(app.server, protocol);
    const disposeRoutes = await (0, routes_1.register)(app, args);
    logger_1.logger.info(`Using config file ${args.config}`);
    logger_1.logger.info(`${protocol.toUpperCase()} server listening on ${serverAddress.toString()}`);
    if (args.auth === cli_1.AuthType.Password) {
        logger_1.logger.info("  - Authentication is enabled");
        if (args.usingEnvPassword) {
            logger_1.logger.info("    - Using password from $PASSWORD");
        }
        else if (args.usingEnvHashedPassword) {
            logger_1.logger.info("    - Using password from $HASHED_PASSWORD");
        }
        else if (args["hashed-password"]) {
            logger_1.logger.info(`    - Using hashed-password from ${args.config}`);
        }
        else {
            logger_1.logger.info(`    - Using password from ${args.config}`);
        }
    }
    else {
        logger_1.logger.info("  - Authentication is disabled");
    }
    if (args.cert) {
        logger_1.logger.info(`  - Using certificate for HTTPS: ${args.cert.value}`);
    }
    else {
        logger_1.logger.info("  - Not serving HTTPS");
    }
    if (args["disable-proxy"]) {
        logger_1.logger.info("  - Proxy disabled");
    }
    else if (args["proxy-domain"].length > 0) {
        logger_1.logger.info(`  - ${(0, util_1.plural)(args["proxy-domain"].length, "Proxying the following domain")}:`);
        args["proxy-domain"].forEach((domain) => logger_1.logger.info(`    - ${domain}`));
    }
    if (args["skip-auth-preflight"]) {
        logger_1.logger.info("  - Skipping authentication for preflight requests");
    }
    if (process.env.VSCODE_PROXY_URI) {
        logger_1.logger.info(`Using proxy URI in PORTS tab: ${process.env.VSCODE_PROXY_URI}`);
    }
    const sessionServerAddress = app.editorSessionManagerServer.address();
    if (sessionServerAddress) {
        logger_1.logger.info(`Session server listening on ${sessionServerAddress.toString()}`);
    }
    if (process.env.EXTENSIONS_GALLERY) {
        logger_1.logger.info("Using custom extensions gallery");
        logger_1.logger.debug(`  - ${process.env.EXTENSIONS_GALLERY}`);
    }
    if (args.enable && args.enable.length > 0) {
        logger_1.logger.info("Enabling the following experimental features:");
        args.enable.forEach((feature) => {
            if (Object.values(cli_1.Feature).includes(feature)) {
                logger_1.logger.info(`  - "${feature}"`);
            }
            else {
                logger_1.logger.error(`  X "${feature}" (unknown feature)`);
            }
        });
        // TODO: Could be nice to add wrapping to the logger?
        logger_1.logger.info("  The code-server project does not provide stability guarantees or commit to fixing bugs relating to these experimental features. When filing bug reports, please ensure that you can reproduce the bug with all experimental features turned off.");
    }
    if (args.open) {
        try {
            await (0, util_2.open)(serverAddress);
            logger_1.logger.info(`Opened ${serverAddress}`);
        }
        catch (error) {
            logger_1.logger.error("Failed to open", (0, logger_1.field)("address", serverAddress.toString()), (0, logger_1.field)("error", error));
        }
    }
    return {
        server: app.server,
        dispose: async () => {
            disposeRoutes();
            await app.dispose();
        },
    };
};
exports.runCodeServer = runCodeServer;
//# sourceMappingURL=main.js.map