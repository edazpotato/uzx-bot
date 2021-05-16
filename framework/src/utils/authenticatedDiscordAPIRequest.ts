import { discordAPIURL } from ".";
import fetch from "@aero/centra";

interface AuthenticatedDiscordApiRequestOptions {
	method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
	body?: [any, string];
}

function authenticatedDiscordApiRequest(
	route: string,
	options: AuthenticatedDiscordApiRequestOptions,
	token: string
) {
	const request = fetch(`${discordAPIURL}/${route}`).header(
		"Authorization",
		`Bot ${token}`
	);
	if (options.body) {
		request.body(options.body[0], options.body[1]);
	}
	return request.send();
}

export default authenticatedDiscordApiRequest;
