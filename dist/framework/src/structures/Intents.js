"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Intents = /** @class */ (function () {
    function Intents(intents) {
        if (intents === void 0) { intents = Intents.NON_PRIVILEGED; }
        var bits = 1;
        for (var _i = 0, intents_1 = intents; _i < intents_1.length; _i++) {
            var intent = intents_1[_i];
            bits << Intents.intentsMap[intent];
        }
        this.bits = bits;
    }
    Intents.intentsMap = {
        GUILDS: 0,
        GUILD_MEMBERS: 1,
        GUILD_BANS: 2,
        GUILD_EMOJIS: 3,
        GUILD_INTEGRATIONS: 4,
        GUILD_WEBHOOKS: 5,
        GUILD_INVITES: 6,
        GUILD_VOICE_STATES: 7,
        GUILD_PRESENCES: 8,
        GUILD_MESSAGES: 9,
        GUILD_MESSAGE_REACTIONS: 10,
        GUILD_MESSAGE_TYPING: 11,
        DIRECT_MESSAGES: 12,
        DIRECT_MESSAGE_REACTIONS: 13,
        DIRECT_MESSAGE_TYPING: 14
    };
    Intents.ALL = [
        "GUILDS",
        "GUILD_MEMBERS",
        "GUILD_BANS",
        "GUILD_EMOJIS",
        "GUILD_INTEGRATIONS",
        "GUILD_WEBHOOKS",
        "GUILD_INVITES",
        "GUILD_VOICE_STATES",
        "GUILD_PRESENCES",
        "GUILD_MESSAGES",
        "GUILD_MESSAGE_REACTIONS",
        "GUILD_MESSAGE_TYPING",
        "DIRECT_MESSAGES",
        "DIRECT_MESSAGE_REACTIONS",
        "DIRECT_MESSAGE_TYPING"
    ];
    Intents.NON_PRIVILEGED = [
        "GUILDS",
        "GUILD_MEMBERS",
        "GUILD_BANS",
        "GUILD_EMOJIS",
        "GUILD_INTEGRATIONS",
        "GUILD_WEBHOOKS",
        "GUILD_INVITES",
        "GUILD_VOICE_STATES",
        "GUILD_MESSAGES",
        "GUILD_MESSAGE_REACTIONS",
        "GUILD_MESSAGE_TYPING",
        "DIRECT_MESSAGE_REACTIONS",
        "DIRECT_MESSAGE_TYPING"
    ];
    Intents.PRIVILEGED = ["GUILD_PRESENCES", "GUILD_MEMBERS"];
    return Intents;
}());
exports.default = Intents;
//# sourceMappingURL=Intents.js.map