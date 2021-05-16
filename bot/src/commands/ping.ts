import { Command } from "@framework";

const command = new Command(
	{
		type: "global",
		name: "ping",
		description: "Pong!"
	},
	async (interaction) => {}
);

export default command;
