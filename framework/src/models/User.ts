import { HTTPURL } from "../typings";

class User {
	id: string;
	bot: boolean;
	name: string;
	discriminator: string;

	private _avatarURL: HTTPURL;

	constructor({ bot, name, discriminator }) {}

	get tag() {
		return `${this.name}#${this.discriminator}`;
	}

	avatarURL(): string {
		return this._avatarURL;
	}
}

export default User;
