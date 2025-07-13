"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.router = void 0;
const express_1 = require("express");
const http_1 = require("../../common/http");
const http_2 = require("../http");
const util_1 = require("../util");
exports.router = (0, express_1.Router)();
exports.router.get("/", async (req, res) => {
    // Must use the *identical* properties used to set the cookie.
    res.clearCookie(http_1.CookieKeys.Session, (0, http_2.getCookieOptions)(req));
    const to = (0, util_1.sanitizeString)(req.query.to) || "/";
    return (0, http_2.redirect)(req, res, to, { to: undefined, base: undefined, href: undefined });
});
//# sourceMappingURL=logout.js.map