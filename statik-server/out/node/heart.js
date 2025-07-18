"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Heart = void 0;
exports.heartbeatTimer = heartbeatTimer;
const logger_1 = require("@coder/logger");
const fs_1 = require("fs");
/**
 * Provides a heartbeat using a local file to indicate activity.
 */
class Heart {
    constructor(heartbeatPath, isActive) {
        this.heartbeatPath = heartbeatPath;
        this.isActive = isActive;
        this.heartbeatInterval = 60000;
        this.lastHeartbeat = 0;
        this.beat = this.beat.bind(this);
        this.alive = this.alive.bind(this);
    }
    alive() {
        const now = Date.now();
        return now - this.lastHeartbeat < this.heartbeatInterval;
    }
    /**
     * Write to the heartbeat file if we haven't already done so within the
     * timeout and start or reset a timer that keeps running as long as there is
     * activity. Failures are logged as warnings.
     */
    async beat() {
        if (this.alive()) {
            return;
        }
        logger_1.logger.debug("heartbeat");
        this.lastHeartbeat = Date.now();
        if (typeof this.heartbeatTimer !== "undefined") {
            clearTimeout(this.heartbeatTimer);
        }
        this.heartbeatTimer = setTimeout(() => heartbeatTimer(this.isActive, this.beat), this.heartbeatInterval);
        try {
            return await fs_1.promises.writeFile(this.heartbeatPath, "");
        }
        catch (error) {
            logger_1.logger.warn(error.message);
        }
    }
    /**
     * Call to clear any heartbeatTimer for shutdown.
     */
    dispose() {
        if (typeof this.heartbeatTimer !== "undefined") {
            clearTimeout(this.heartbeatTimer);
        }
    }
}
exports.Heart = Heart;
/**
 * Helper function for the heartbeatTimer.
 *
 * If heartbeat is active, call beat. Otherwise do nothing.
 *
 * Extracted to make it easier to test.
 */
async function heartbeatTimer(isActive, beat) {
    try {
        if (await isActive()) {
            beat();
        }
    }
    catch (error) {
        logger_1.logger.warn(error.message);
    }
}
//# sourceMappingURL=heart.js.map