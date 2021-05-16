require("module-alias/register");

import { CommandClient, Intents } from "@framework";

import dotenv from "dotenv";
import path from "path";

dotenv.config();

const intents = new Intents(); // new Intents(Intents.ALL);

const client = new CommandClient({ intents: intents }, process.env.TOKEN);

client.loadCommands(path.join(__dirname, "commands"), { overwrite: true });

client.start(() => {
	console.log(`Logged in as ${client.user.tag}!`);
});
