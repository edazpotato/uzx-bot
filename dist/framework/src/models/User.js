"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var User = /** @class */ (function () {
    function User(_a) {
        var bot = _a.bot, name = _a.name, discriminator = _a.discriminator;
    }
    Object.defineProperty(User.prototype, "tag", {
        get: function () {
            return this.name + "#" + this.discriminator;
        },
        enumerable: false,
        configurable: true
    });
    User.prototype.avatarURL = function () {
        return this._avatarURL;
    };
    return User;
}());
exports.default = User;
//# sourceMappingURL=User.js.map