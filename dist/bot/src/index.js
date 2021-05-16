"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require("module-alias/register");
var _framework_1 = require("@framework");
var dotenv_1 = __importDefault(require("dotenv"));
var path_1 = __importDefault(require("path"));
dotenv_1.default.config();
var intents = new _framework_1.Intents(); // new Intents(Intents.ALL);
var client = new _framework_1.CommandClient({ intents: intents }, process.env.TOKEN);
client.loadCommands(path_1.default.join(__dirname, "commands"), { overwrite: true });
client.start(function () {
    console.log("Logged in as " + client.user.tag + "!");
});
//# sourceMappingURL=index.js.map