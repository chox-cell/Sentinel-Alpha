import { SentinelPaymentRequiredError } from "./errors.js";
import type { SentinelDecision, SentinelRiskResponse, X402Challenge } from "./types.js";

export function normalizeSentinelDecision(response: SentinelRiskResponse): SentinelDecision {
  const traceId =
    typeof response.meta?.trace_id === "string" ? response.meta.trace_id : undefined;
  return {
    score: response.risk_metrics.score,
    confidence: response.decision.confidence,
    action: response.decision.action,
    emergencySignal: response.decision.emergency_signal,
    threatClass: response.risk_metrics.threat_class,
    traceId,
  };
}

export function isX402Challenge(errorOrResponse: unknown): boolean {
  if (errorOrResponse instanceof SentinelPaymentRequiredError) {
    return true;
  }
  if (!errorOrResponse || typeof errorOrResponse !== "object") {
    return false;
  }
  const o = errorOrResponse as Record<string, unknown>;
  if (o.challenge && typeof o.challenge === "object") {
    return looksLikeChallenge(o.challenge as Record<string, unknown>);
  }
  if (o.detail && typeof o.detail === "object") {
    return looksLikeChallenge(o.detail as Record<string, unknown>);
  }
  return looksLikeChallenge(o);
}

function looksLikeChallenge(o: Record<string, unknown>): boolean {
  const resource = o.resource;
  return (
    typeof resource === "string" &&
    resource.includes("/contracts/risk-score") &&
    (o.x402_version !== undefined || o.payment_method === "x402")
  );
}

export function parseX402ChallengeFromBody(body: unknown): X402Challenge | null {
  if (!body || typeof body !== "object") {
    return null;
  }
  const o = body as Record<string, unknown>;
  const detail = o.detail;
  if (detail && typeof detail === "object") {
    return detail as X402Challenge;
  }
  if (looksLikeChallenge(o)) {
    return o as X402Challenge;
  }
  return null;
}
