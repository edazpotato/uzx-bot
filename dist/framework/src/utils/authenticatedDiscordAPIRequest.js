"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var _1 = require(".");
var centra_1 = __importDefault(require("@aero/centra"));
function authenticatedDiscordApiRequest(route, options, token) {
    var request = centra_1.default(_1.discordAPIURL + "/" + route).header("Authorization", "Bot " + token);
    if (options.body) {
        request.body(options.body[0], options.body[1]);
    }
    return request.send();
}
exports.default = authenticatedDiscordApiRequest;
//# sourceMappingURL=authenticatedDiscordAPIRequest.js.map