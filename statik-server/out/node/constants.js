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
exports.httpProxyUri = exports.isDevMode = exports.tmpdir = exports.codeVersion = exports.commit = exports.version = exports.vsRootPath = exports.rootPath = void 0;
exports.getPackageJson = getPackageJson;
exports.getVersionString = getVersionString;
exports.getVersionJsonString = getVersionJsonString;
const logger_1 = require("@coder/logger");
const os = __importStar(require("os"));
const path = __importStar(require("path"));
function getPackageJson(relativePath) {
    let pkg = {};
    try {
        pkg = require(relativePath);
    }
    catch (error) {
        logger_1.logger.warn(error.message);
    }
    return pkg;
}
exports.rootPath = path.resolve(__dirname, "../..");
exports.vsRootPath = path.join(exports.rootPath, "lib/vscode");
const PACKAGE_JSON = "package.json";
const pkg = getPackageJson(`${exports.rootPath}/${PACKAGE_JSON}`);
const codePkg = getPackageJson(`${exports.vsRootPath}/${PACKAGE_JSON}`) || { version: "0.0.0" };
exports.version = pkg.version || "development";
exports.commit = pkg.commit || "development";
exports.codeVersion = codePkg.version || "development";
exports.tmpdir = path.join(os.tmpdir(), "code-server");
exports.isDevMode = exports.commit === "development";
exports.httpProxyUri = process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy;
/**
 * getVersionString returns a human-readable version string suitable
 * for outputting to the console.
 */
function getVersionString() {
    return [exports.version, exports.commit, "with Code", exports.codeVersion].join(" ");
}
/**
 * getVersionJsonString returns a machine-readable version string
 * suitable for outputting to the console.
 */
function getVersionJsonString() {
    return JSON.stringify({
        codeServer: exports.version,
        commit: exports.commit,
        vscode: exports.codeVersion,
    });
}
//# sourceMappingURL=constants.js.map