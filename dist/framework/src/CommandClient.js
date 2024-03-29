"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var _1 = require(".");
var ws_1 = __importDefault(require("ws"));
var CommandClient = /** @class */ (function () {
    function CommandClient(options, token) {
        var _a = options;
        this.token = token;
    }
    CommandClient.prototype.WebSocketHeartbeat = function () {
        var _this = this;
        clearTimeout(this.ws.heartbeatTimeout);
        if (!this.lastHeartbeatAcknowledged) {
            return fthis.ws.terminate();
        }
        this.ws.heartbeatTimeout = setTimeout(function () {
            _this.ws.terminate();
        }, this.heartbeatInterval);
    };
    CommandClient.prototype.loadCommands = function (commands, options) {
        var overwrite = options.overwrite;
        var commandsList = commands;
        if (typeof commands === "string") {
            if (commands.length < 1)
                throw new Error("Provide a path to the commands directory!");
        }
        if (commandsList.length < 1)
            return 0;
        return commandsList.length;
        var currentCommands = [];
        if (!overwrite) {
        }
        for (var _i = 0, commandsList_1 = commandsList; _i < commandsList_1.length; _i++) {
            var command_1 = commandsList_1[_i];
            // TODO: Load command
        }
    };
    CommandClient.prototype.start = function (callback) {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, _1.authenticatedDiscordAPIRequest("/gateway/bot", {}, this.token)
                            .then(function (res) { return __awaiter(_this, void 0, void 0, function () {
                            var data;
                            return __generator(this, function (_a) {
                                if (res.statusCode !== 200)
                                    throw new Error("Request not okay! " + res.statusCode);
                                data = JSON.parse(res.body);
                                this.gatewayURL = data.url + "?v=9&encoding=json";
                                this.recommendShards = data.shards;
                                return [2 /*return*/];
                            });
                        }); })
                            .catch(function (err) {
                            throw new Error("An error occured while fetching the gateway address from Discord.\n\n" + err);
                        })];
                    case 1:
                        _a.sent();
                        this.ws = new ws_1.default(this.gatewayURL);
                        this.ws.on("message", function (rawData) {
                            try {
                                var data = JSON.parse(rawData);
                                var opCode = data.op;
                                var eventData = data.d;
                                switch (opCode) {
                                    case 1:
                                        /* Opcode 1: Heartbeat */
                                        // We immediatley respond with a heatbeat.
                                        _this.lastHeartbeatAcknowledged = true;
                                        _this.WebSocketHeartbeat();
                                        break;
                                    case 10:
                                        /* Opcode 10: Hello */
                                        _this.heartbeatInterval = eventData["heartbeat_interval"];
                                        _this.lastHeartbeatAcknowledged = true;
                                        _this.ws.heartbeatTimeout = setTimeout(_this.WebSocketHeartbeat, _this.heartbeatInterval * Math.random());
                                        break;
                                    case 11:
                                        /* Opcode 11: Heartbeat ACK */
                                        // The heartbeat has been aknoledged.
                                        _this.lastHeartbeatAcknowledged = true;
                                        break;
                                }
                            }
                            catch (err) {
                                throw new Error("An error occured when handing a message from Discord.\n\n" + err);
                            }
                        });
                        this.ws.on('close', function () { return clearTimeout(_this.ws.heartbeatTimeout); });
                        return [2 /*return*/];
                }
            });
        });
    };
    return CommandClient;
}());
exports.default = CommandClient;
//# sourceMappingURL=CommandClient.js.map