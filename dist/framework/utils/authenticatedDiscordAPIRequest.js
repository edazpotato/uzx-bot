import { discordAPIURL } from ".";
import fetch from "@aero/centra";
function authenticatedDiscordApiRequest(route, options, token) {
    const request = fetch(`${discordAPIURL}/${route}`).header("Authorization", `Bot ${token}`);
    if (options.body) {
        request.body(options.body[0], options.body[1]);
    }
    return request.send();
}
export default authenticatedDiscordApiRequest;
//# sourceMappingURL=authenticatedDiscordAPIRequest.js.map