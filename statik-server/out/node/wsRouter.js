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
exports.wss = exports.WebsocketRouter = exports.handleUpgrade = void 0;
exports.Router = Router;
const express = __importStar(require("express"));
const http = __importStar(require("http"));
const Websocket = __importStar(require("ws"));
const handleUpgrade = (app, server) => {
    server.on("upgrade", (req, socket, head) => {
        socket.pause();
        const wreq = req;
        wreq.ws = socket;
        wreq.head = head;
        wreq._ws_handled = false;
        app.handle(wreq, new http.ServerResponse(wreq), () => {
            if (!wreq._ws_handled) {
                socket.end("HTTP/1.1 404 Not Found\r\n\r\n");
            }
        });
    });
};
exports.handleUpgrade = handleUpgrade;
class WebsocketRouter {
    constructor() {
        this.router = express.Router();
    }
    /**
     * Handle a websocket at this route. Note that websockets are immediately
     * paused when they come in.
     *
     * If the origin header exists it must match the host or the connection will
     * be prevented.
     */
    ws(route, ...handlers) {
        this.router.get(route, ...handlers.map((handler) => {
            const wrapped = (req, res, next) => {
                ;
                req._ws_handled = true;
                return handler(req, res, next);
            };
            return wrapped;
        }));
    }
}
exports.WebsocketRouter = WebsocketRouter;
function Router() {
    return new WebsocketRouter();
}
exports.wss = new Websocket.Server({ noServer: true });
//# sourceMappingURL=wsRouter.js.map