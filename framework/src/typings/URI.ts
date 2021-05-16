export type WebSocketURL = `ws${"" | "s"}://${string}.${string}${
	| ""
	| `/${"" | string}`}${"" | `?${string}=${string}${"" | `&${string}`}`}`;

export type HTTPURL = `http${"" | "s"}://${string}.${string}${
	| ""
	| `/${"" | string}`}`;
