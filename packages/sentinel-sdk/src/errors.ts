import type { X402Challenge } from "./types.js";

const SENTINEL_TIMEOUT = "SENTINEL_TIMEOUT";
const SENTINEL_NETWORK = "SENTINEL_NETWORK";
const SENTINEL_HTTP = "SENTINEL_HTTP";
const SENTINEL_VALIDATION = "SENTINEL_VALIDATION";
const SENTINEL_X402 = "SENTINEL_X402";

export class SentinelError extends Error {
  readonly code: string;
  constructor(code: string, message: string) {
    super(message);
    this.name = "SentinelError";
    this.code = code;
  }
}

export class SentinelTimeoutError extends SentinelError {
  constructor(message = "Request timed out") {
    super(SENTINEL_TIMEOUT, message);
    this.name = "SentinelTimeoutError";
  }
}

export class SentinelNetworkError extends SentinelError {
  readonly cause?: unknown;
  constructor(message = "Network error", cause?: unknown) {
    super(SENTINEL_NETWORK, message);
    this.name = "SentinelNetworkError";
    this.cause = cause;
  }
}

export class SentinelHttpError extends SentinelError {
  readonly status: number;
  readonly body?: unknown;
  constructor(status: number, message: string, body?: unknown) {
    super(SENTINEL_HTTP, message);
    this.name = "SentinelHttpError";
    this.status = status;
    this.body = body;
  }
}

export class SentinelValidationError extends SentinelError {
  constructor(message: string) {
    super(SENTINEL_VALIDATION, message);
    this.name = "SentinelValidationError";
  }
}

export class SentinelPaymentRequiredError extends SentinelError {
  readonly challenge: X402Challenge;
  constructor(challenge: X402Challenge) {
    super(SENTINEL_X402, "x402 payment required");
    this.name = "SentinelPaymentRequiredError";
    this.challenge = challenge;
  }
}
