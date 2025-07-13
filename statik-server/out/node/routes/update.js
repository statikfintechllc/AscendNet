"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.router = void 0;
const express_1 = require("express");
const constants_1 = require("../constants");
const http_1 = require("../http");
exports.router = (0, express_1.Router)();
exports.router.get("/check", http_1.ensureAuthenticated, async (req, res) => {
    const update = await req.updater.getUpdate(req.query.force === "true");
    res.json({
        checked: update.checked,
        latest: update.version,
        current: constants_1.version,
        isLatest: req.updater.isLatestVersion(update),
    });
});
//# sourceMappingURL=update.js.map