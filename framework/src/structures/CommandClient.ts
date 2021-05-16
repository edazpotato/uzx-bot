import {
	Command,
	Intents,
	User,
	authenticatedDiscordAPIRequest,
	discordAPIURL
} from "..";

import WebSocket from "ws";
import command from "bot/src/commands/ping";
import fetch from "@aero/centra";

interface CommandClientOptions {
	intents: Intents;
}

interface LoadCommandsOptions {
	overwrite: boolean;
}

type GatewayResponse = {
	url: string;
	shards: number;
	session_start_limit: {
		total: number;
		remaining: number;
		reset_after: number;
		max_concurrency: number;
	};
};

type EventName =
	| "GUILD_CREATE"
	| "GUILD_UPDATE"
	| "GUILD_DELETE"
	| "GUILD_ROLE_CREATE"
	| "GUILD_ROLE_UPDATE"
	| "GUILD_ROLE_DELETE"
	| "CHANNEL_CREATE"
	| "CHANNEL_UPDATE"
	| "CHANNEL_DELETE"
	| "CHANNEL_PINS_UPDATE"
	| "THREAD_CREATE"
	| "THREAD_UPDATE"
	| "THREAD_DELETE"
	| "THREAD_LIST_SYNC"
	| "THREAD_MEMBER_UPDATE"
	| "THREAD_MEMBERS_UPDATE"
	| "GUILD_MEMBER_ADD"
	| "GUILD_MEMBER_UPDATE"
	| "GUILD_MEMBER_REMOVE"
	| "THREAD_MEMBERS_UPDATE"
	| "GUILD_BAN_ADD"
	| "GUILD_BAN_REMOVE"
	| "GUILD_EMOJIS_UPDATE"
	| "GUILD_INTEGRATIONS_UPDATE"
	| "INTEGRATION_CREATE"
	| "INTEGRATION_UPDATE"
	| "INTEGRATION_DELETE"
	| "WEBHOOKS_UPDATE"
	| "INVITE_CREATE"
	| "INVITE_DELETE"
	| "VOICE_STATE_UPDATE"
	| "PRESENCE_UPDATE"
	| "MESSAGE_CREATE"
	| "MESSAGE_UPDATE"
	| "MESSAGE_DELETE"
	| "MESSAGE_DELETE_BULK"
	| "MESSAGE_REACTION_ADD"
	| "MESSAGE_REACTION_REMOVE"
	| "MESSAGE_REACTION_REMOVE_ALL"
	| "MESSAGE_REACTION_REMOVE_EMOJI"
	| "TYPING_START"
	| "MESSAGE_CREATE"
	| "MESSAGE_UPDATE"
	| "MESSAGE_DELETE"
	| "CHANNEL_PINS_UPDATE"
	| "MESSAGE_REACTION_ADD"
	| "MESSAGE_REACTION_REMOVE"
	| "MESSAGE_REACTION_REMOVE_ALL"
	| "MESSAGE_REACTION_REMOVE_EMOJI"
	| "TYPING_START";

class CommandClient {
	ws: WebSocket;
	heartbeatInterval?: number;
	private WebSocketHeartbeatTimeout?: any;
	private gatewayURL?: string;
	private lastHeartbeatAcknowledged: boolean;
	lastHeartbeatSequenceNumber: number | null;

	readonly token: string;
	readonly intents: Intents;

	recommendShards: number;
	user: User;

	id: string;

	constructor(options: CommandClientOptions, token: string) {
		const { intents } = options;
		this.intents = intents;

		this.token = token;

		this.lastHeartbeatSequenceNumber = null;
	}

	WebSocketHeartbeat() {
		clearTimeout(this.WebSocketHeartbeatTimeout);
		if (!this.lastHeartbeatAcknowledged && this.ws) {
			return this.ws.terminate();
		}

		this.lastHeartbeatAcknowledged = false;
		this.ws.send(
			JSON.stringify({ op: 1, d: this.lastHeartbeatSequenceNumber })
		);

		this.WebSocketHeartbeatTimeout = setTimeout(() => {
			this.WebSocketHeartbeat();
		}, this.heartbeatInterval);
	}

	loadCommands(commands: string | Command[], options: LoadCommandsOptions) {
		const { overwrite } = options;

		let commandsList = commands;
		if (typeof commands === "string") {
			if (commands.length < 1)
				throw new Error("Provide a path to the commands directory!");
		}
		if (commandsList.length < 1) return 0;
		return commandsList.length;

		let currentCommands = [];
		if (!overwrite) {
		}
		for (const command of commandsList) {
			// TODO: Load command
		}
	}

	handleEvent(name, data) {
		console.log(`${name} event received from Discord!`, data);
	}

	connectWebSocket() {
		clearTimeout(this.WebSocketHeartbeatTimeout);
		this.ws = new WebSocket(this.gatewayURL);
	}

	async start(callback: Function) {
		await authenticatedDiscordAPIRequest("/gateway/bot", {}, this.token)
			.then(async (res) => {
				if (res.statusCode !== 200)
					throw new Error(`Request not okay! ${res.statusCode}`);
				const data = JSON.parse(res.body) as GatewayResponse;
				this.gatewayURL = `${data.url}?v=9&encoding=json`;
				this.recommendShards = data.shards;
			})
			.catch((err) => {
				throw new Error(
					`An error occured while fetching the gateway address from Discord.\n\n${err}`
				);
			});

		this.connectWebSocket();

		this.ws.on("message", (rawData: string) => {
			try {
				const data = JSON.parse(rawData);
				const opCode = data.op as number;
				const eventData = data.d as any;

				console.log(`Recived opcode ${opCode} from Discord.`);

				/* These are set if the Opcode is 0: Gateway Dispatch Opcode */
				let sequenceNumber: number;
				let eventName: EventName;
				if (opCode === 0) {
					sequenceNumber = data.s;
					eventName = data.t as EventName;
				}

				if (sequenceNumber)
					this.lastHeartbeatSequenceNumber = sequenceNumber;

				switch (opCode) {
					case 0:
						/* Opcode 0: Dispatch */
						/* The client has recived an event from Discord! */

						this.handleEvent(eventName, eventData);
						break;

					case 1:
						/* Opcode 1: Heartbeat */
						/* We immediatley respond with a heatbeat. */
						this.lastHeartbeatAcknowledged = true;
						this.WebSocketHeartbeat();
						break;

					case 9:
						/* Opcode 9: Invalid Session */
						/* We should reconnect and re identity. */
						this.ws.terminate();
						break;

					case 10:
						/* Opcode 10: Hello */
						/* We are connected! We now need to send a heartbeat to the
						 * gateway after Math.random()*heartbeat_interval miliseconds.
						 */

						this.heartbeatInterval =
							eventData["heartbeat_interval"];
						this.lastHeartbeatAcknowledged = true;

						this.WebSocketHeartbeatTimeout = setTimeout(
							this.WebSocketHeartbeat,
							this.heartbeatInterval * Math.random()
						);

						this.ws.send(
							JSON.stringify({
								op: 2,
								d: {
									token: this.token,
									intents: this.intents,
									compress: true,
									properties: {
										$os: process.platform,
										$browser:
											"UZX Slash Commands framework",
										$device: "UZX Slash Commands framework"
									}
								}
							})
						);
						break;

					case 11:
						/* Opcode 11: Heartbeat ACK */
						/* The last heartbeat has been acknowledged. */
						this.lastHeartbeatAcknowledged = true;
						break;
				}
			} catch (err) {
				throw new Error(
					`An error occured when handing a message from Discord.\n\n${err}`
				);
			}
		});

		this.ws.on("close", () => clearTimeout(this.WebSocketHeartbeatTimeout));
	}
}

export default CommandClient;
