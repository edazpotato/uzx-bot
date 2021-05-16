type CommandCallback = (interaction: any) => Promise<any>;

interface CommandOptions {
	type: "global";
	name: string;
	description: string;
	enabledByDefault?: boolean;
}

class Command {
	type: "global";
	enabledByDefault: boolean;
	name: string;
	description: string;
	exec: CommandCallback;

	constructor(options: CommandOptions, exec: CommandCallback) {
		const { type, name, description, enabledByDefault } = options;
		if (type !== "global")
			throw new Error("Only global commands are supported rn");

		if (!name.match(/^[\w-]{1,32}$/))
			throw new Error(
				"Command names must be 1-32 characters long, have no spaces, and have no special characters except dashes (-) and underscores (_).\n(Must match ^[w-]{1,32}$)"
			);

		if (description.length < 1 || description.length > 100)
			throw new Error(
				"Command descriptions must be between 1 and 100 characters long."
			);

		this.type = type;
		this.name = name;
		this.description = description;

		if (enabledByDefault !== undefined) {
			this.enabledByDefault = enabledByDefault;
		} else {
			this.enabledByDefault = false;
		}
	}
}

export default Command;
