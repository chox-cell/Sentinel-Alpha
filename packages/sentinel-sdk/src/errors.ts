import type { X402Challenge } from "./types.js";

export type SentinelErrorCode = "TIMEOUT" | "NETWORK" | "VALIDATION" | "UNSUPPORTED_RESPONSE" | "UNKNOWN";

export class SentinelError extends Error {
  readonly code: SentinelErrorCode;

  constructor(message: string, code: SentinelErrorCode, options?: { cause?: unknown }) {
    super(message, options);
    this.name = "SentinelError";
    this.code = code;
  }
}

export class SentinelX402ChallengeError extends Error {
  readonly challenge: X402Challenge;
  readonly httpStatus = 402;

  constructor(challenge: X402Challenge, options?: { cause?: unknown }) {
    super(`x402 payment required for ${challenge.resource}`, options);
    this.name = "SentinelX402ChallengeError";
    this.challenge = challenge;
  }
}
