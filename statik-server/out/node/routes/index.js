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
exports.register = void 0;
const logger_1 = require("@coder/logger");
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const express = __importStar(require("express"));
const fs_1 = require("fs");
const path = __importStar(require("path"));
const http_1 = require("../../common/http");
const util_1 = require("../../common/util");
const cli_1 = require("../cli");
const constants_1 = require("../constants");
const heart_1 = require("../heart");
const http_2 = require("../http");
const settings_1 = require("../settings");
const update_1 = require("../update");
const util_2 = require("../util");
const domainProxy = __importStar(require("./domainProxy"));
const errors_1 = require("./errors");
const health = __importStar(require("./health"));
const login = __importStar(require("./login"));
const logout = __importStar(require("./logout"));
const pathProxy = __importStar(require("./pathProxy"));
const update = __importStar(require("./update"));
const vscode = __importStar(require("./vscode"));
const memory_router_1 = require("../statik/memory-router");
/**
 * Register all routes and middleware.
 */
const register = async (app, args) => {
    const heart = new heart_1.Heart(path.join(util_2.paths.data, "heartbeat"), async () => {
        return new Promise((resolve, reject) => {
            // getConnections appears to not call the callback when there are no more
            // connections.  Feels like it must be a bug?  For now add a timer to make
            // sure we eventually resolve.
            const timer = setTimeout(() => {
                logger_1.logger.debug("Node failed to respond with connections; assuming zero");
                resolve(false);
            }, 5000);
            app.server.getConnections((error, count) => {
                clearTimeout(timer);
                if (error) {
                    return reject(error);
                }
                logger_1.logger.debug((0, util_1.plural)(count, `${count} active connection`));
                resolve(count > 0);
            });
        });
    });
    app.router.disable("x-powered-by");
    app.wsRouter.disable("x-powered-by");
    app.router.use((0, cookie_parser_1.default)());
    app.wsRouter.use((0, cookie_parser_1.default)());
    const settings = new settings_1.SettingsProvider(path.join(args["user-data-dir"], "coder.json"));
    const updater = new update_1.UpdateProvider("https://api.github.com/repos/coder/code-server/releases/latest", settings);
    const common = (req, _, next) => {
        // /healthz|/healthz/ needs to be excluded otherwise health checks will make
        // it look like code-server is always in use.
        if (!/^\/healthz\/?$/.test(req.url)) {
            // NOTE@jsjoeio - intentionally not awaiting the .beat() call here because
            // we don't want to slow down the request.
            heart.beat();
        }
        // Add common variables routes can use.
        req.args = args;
        req.heart = heart;
        req.settings = settings;
        req.updater = updater;
        next();
    };
    app.router.use(common);
    app.wsRouter.use(common);
    app.router.use(/.*/, async (req, res, next) => {
        // If we're handling TLS ensure all requests are redirected to HTTPS.
        // TODO: This does *NOT* work if you have a base path since to specify the
        // protocol we need to specify the whole path.
        if (args.cert && !req.connection.encrypted) {
            return res.redirect(`https://${req.headers.host}${req.originalUrl}`);
        }
        next();
    });
    app.router.get(["/security.txt", "/.well-known/security.txt"], async (_, res) => {
        const resourcePath = path.resolve(constants_1.rootPath, "src/browser/security.txt");
        res.set("Content-Type", (0, util_2.getMediaMime)(resourcePath));
        res.send(await fs_1.promises.readFile(resourcePath));
    });
    app.router.get("/robots.txt", async (_, res) => {
        const resourcePath = path.resolve(constants_1.rootPath, "src/browser/robots.txt");
        res.set("Content-Type", (0, util_2.getMediaMime)(resourcePath));
        res.send(await fs_1.promises.readFile(resourcePath));
    });
    app.router.use("/", domainProxy.router);
    app.wsRouter.use("/", domainProxy.wsRouter.router);
    app.router.all("/proxy/:port{/*path}", async (req, res) => {
        await pathProxy.proxy(req, res);
    });
    app.wsRouter.get("/proxy/:port{/*path}", async (req) => {
        await pathProxy.wsProxy(req);
    });
    // These two routes pass through the path directly.
    // So the proxied app must be aware it is running
    // under /absproxy/<someport>/
    app.router.all("/absproxy/:port{/*path}", async (req, res) => {
        await pathProxy.proxy(req, res, {
            passthroughPath: true,
            proxyBasePath: args["abs-proxy-base-path"],
        });
    });
    app.wsRouter.get("/absproxy/:port{/*path}", async (req) => {
        await pathProxy.wsProxy(req, {
            passthroughPath: true,
            proxyBasePath: args["abs-proxy-base-path"],
        });
    });
    app.router.use(express.json());
    app.router.use(express.urlencoded({ extended: true }));
    app.router.use("/_static", express.static(constants_1.rootPath, {
        cacheControl: constants_1.commit !== "development",
        fallthrough: false,
        setHeaders: (res, path, stat) => {
            // The service worker is served from a sub-path on the static route so
            // this is required to allow it to register a higher scope (by default
            // the browser only allows it to register from its own path or lower).
            if (path.endsWith("/serviceWorker.js")) {
                res.setHeader("Service-Worker-Allowed", "/");
            }
        },
    }));
    app.router.use("/healthz", health.router);
    app.wsRouter.use("/healthz", health.wsRouter.router);
    if (args.auth === cli_1.AuthType.Password) {
        app.router.use("/login", login.router);
        app.router.use("/logout", logout.router);
    }
    else {
        app.router.all("/login", (req, res) => (0, http_2.redirect)(req, res, "/", {}));
        app.router.all("/logout", (req, res) => (0, http_2.redirect)(req, res, "/", {}));
    }
    app.router.use("/update", update.router);
    // Add Statik Memory Router for unified dashboard API
    const statikMemoryRouter = new memory_router_1.StatikMemoryRouter();
    app.router.use(statikMemoryRouter.getRouter());
    // For historic reasons we also load at /vscode because the root was replaced
    // by a plugin in v1 of Coder.  The plugin system (which was for internal use
    // only) has been removed, but leave the additional route for now.
    for (const routePrefix of ["/vscode", "/"]) {
        app.router.use(routePrefix, vscode.router);
        app.wsRouter.use(routePrefix, vscode.wsRouter.router);
    }
    app.router.use(() => {
        throw new http_1.HttpError("Not Found", http_1.HttpCode.NotFound);
    });
    app.router.use(errors_1.errorHandler);
    app.wsRouter.use(errors_1.wsErrorHandler);
    return () => {
        heart.dispose();
        vscode.dispose();
    };
};
exports.register = register;
//# sourceMappingURL=index.js.map