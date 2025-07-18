#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const logger_1 = require("@coder/logger");
const cli_1 = require("./cli");
const constants_1 = require("./constants");
const main_1 = require("./main");
const wrapper_1 = require("./wrapper");
async function entry() {
    // There's no need to check flags like --help or to spawn in an existing
    // instance for the child process because these would have already happened in
    // the parent and the child wouldn't have been spawned. We also get the
    // arguments from the parent so we don't have to parse twice and to account
    // for environment manipulation (like how PASSWORD gets removed to avoid
    // leaking to child processes).
    if ((0, wrapper_1.isChild)(wrapper_1.wrapper)) {
        const args = await wrapper_1.wrapper.handshake();
        wrapper_1.wrapper.preventExit();
        const server = await (0, main_1.runCodeServer)(args);
        wrapper_1.wrapper.onDispose(() => server.dispose());
        return;
    }
    const cliArgs = (0, cli_1.parse)(process.argv.slice(2));
    const configArgs = await (0, cli_1.readConfigFile)(cliArgs.config);
    const args = await (0, cli_1.setDefaults)(cliArgs, configArgs);
    if (args.help) {
        console.log("code-server", (0, constants_1.getVersionString)());
        console.log("");
        console.log(`Usage: code-server [options] [path]`);
        console.log(`    - Opening a directory: code-server ./path/to/your/project`);
        console.log(`    - Opening a saved workspace: code-server ./path/to/your/project.code-workspace`);
        console.log("");
        console.log("Options");
        (0, cli_1.optionDescriptions)().forEach((description) => {
            console.log("", description);
        });
        return;
    }
    if (args.version) {
        if (args.json) {
            console.log((0, constants_1.getVersionJsonString)());
        }
        else {
            console.log((0, constants_1.getVersionString)());
        }
        return;
    }
    if ((0, main_1.shouldSpawnCliProcess)(args)) {
        logger_1.logger.debug("Found VS Code arguments; spawning VS Code CLI");
        return (0, main_1.runCodeCli)(args);
    }
    const socketPath = await (0, cli_1.shouldOpenInExistingInstance)(cliArgs, args["session-socket"]);
    if (socketPath) {
        logger_1.logger.debug("Trying to open in existing instance");
        return (0, main_1.openInExistingInstance)(args, socketPath);
    }
    return wrapper_1.wrapper.start(args);
}
entry().catch((error) => {
    logger_1.logger.error(error.message);
    wrapper_1.wrapper.exit(error);
});
//# sourceMappingURL=entry.js.map