import { SentinelX402ChallengeError } from "./errors.js";
import type { X402Challenge } from "./types.js";

function isChallengeShape(d: Record<string, unknown>): d is Record<string, string> {
  return typeof d.x402_version === "string" && typeof d.resource === "string";
}

export function parseX402Detail(detail: Record<string, unknown>): X402Challenge {
  if (!isChallengeShape(detail)) {
    throw new Error("Invalid x402 challenge payload");
  }
  return {
    x402Version: detail.x402_version,
    paymentMethod: String(detail.payment_method ?? ""),
    network: String(detail.network ?? ""),
    payTo: String(detail.pay_to ?? ""),
    amountUsdc: String(detail.amount_usdc ?? ""),
    asset: String(detail.asset ?? ""),
    resource: detail.resource,
    instructions: String(detail.instructions ?? ""),
    lane: String(detail.lane ?? "basic"),
  };
}

/** True if value is an x402 challenge error or a Fetch-like 402 JSON body we recognize. */
export function isX402Challenge(errorOrResponse: unknown): boolean {
  if (errorOrResponse instanceof SentinelX402ChallengeError) return true;
  if (!errorOrResponse || typeof errorOrResponse !== "object") return false;

  const v = errorOrResponse as Record<string, unknown>;

  if ("challenge" in v && v.challenge && typeof v.challenge === "object") {
    const ch = v.challenge as Record<string, unknown>;
    return typeof ch.x402Version === "string" && typeof ch.resource === "string";
  }

  if ("detail" in v && v.detail && typeof v.detail === "object") {
    return isChallengeShape(v.detail as Record<string, unknown>);
  }

  return isChallengeShape(v);
}
