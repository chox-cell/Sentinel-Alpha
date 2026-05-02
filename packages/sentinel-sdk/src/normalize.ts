import type { NormalizedSentinelAction, SentinelDecision, SentinelRiskResponse } from "./types.js";

function normalizeAction(apiAction: string): NormalizedSentinelAction {
  const a = (apiAction ?? "").trim().toUpperCase();
  if (a === "ALLOW") return "allow";
  if (a === "REVIEW") return "review";
  if (a === "BLOCK") return "block";
  if (a === "REDUCE") return "reduce";
  if (a === "EXIT_NOW") return "exit_now";
  return "review";
}

export function normalizeSentinelDecision(response: SentinelRiskResponse): SentinelDecision {
  const action = normalizeAction(response.decision.action);
  return {
    action,
    score: response.risk_metrics.score,
    confidence: response.decision.confidence,
    emergencySignal: response.decision.emergency_signal,
    threatClass: response.risk_metrics.threat_class,
    raw: response,
  };
}

export function shouldExecuteForAction(action: NormalizedSentinelAction): boolean {
  return action === "allow";
}
