"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Command = /** @class */ (function () {
    function Command(options, exec) {
        var type = options.type, name = options.name, description = options.description, enabledByDefault = options.enabledByDefault;
        if (type !== "global")
            throw new Error("Only global commands are supported rn");
        if (!name.match(/^[\w-]{1,32}$/))
            throw new Error("Command names must be 1-32 characters long, have no spaces, and have no special characters except dashes (-) and underscores (_).\n(Must match ^[w-]{1,32}$)");
        if (description.length < 1 || description.length > 100)
            throw new Error("Command descriptions must be between 1 and 100 characters long.");
        this.type = type;
        this.name = name;
        this.description = description;
        if (enabledByDefault !== undefined) {
            this.enabledByDefault = enabledByDefault;
        }
        else {
            this.enabledByDefault = false;
        }
    }
    return Command;
}());
exports.default = Command;
//# sourceMappingURL=Command.js.map