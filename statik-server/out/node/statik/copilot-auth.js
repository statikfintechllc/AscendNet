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
exports.CopilotAuthManager = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class CopilotAuthManager {
    constructor() {
        this.authPath = "/root/.statik/keys";
        this.ensureAuthDirectory();
    }
    ensureAuthDirectory() {
        if (!fs.existsSync(this.authPath)) {
            fs.mkdirSync(this.authPath, { recursive: true });
        }
    }
    loadGitHubToken() {
        const tokenPath = path.join(this.authPath, "github-token");
        if (fs.existsSync(tokenPath)) {
            return fs.readFileSync(tokenPath, "utf8").trim();
        }
        return null;
    }
    loadMeshIdentity() {
        const identityPath = path.join(this.authPath, "mesh-identity.json");
        if (fs.existsSync(identityPath)) {
            return fs.readFileSync(identityPath, "utf8");
        }
        return null;
    }
    injectCopilotSettings() {
        const token = this.loadGitHubToken();
        if (!token) {
            console.warn("⚠️  No GitHub token found, Copilot disabled");
            return {};
        }
        console.log("🤖 Injecting Copilot auth for persistent session");
        return {
            "github.copilot.enable": true,
            "github.copilotChat.enabled": true,
            "workbench.experimental.chat.enabled": true,
            "github.copilot.advanced": {
                "authProvider": "persistent",
                "token": token
            }
        };
    }
}
exports.CopilotAuthManager = CopilotAuthManager;
//# sourceMappingURL=copilot-auth.js.map