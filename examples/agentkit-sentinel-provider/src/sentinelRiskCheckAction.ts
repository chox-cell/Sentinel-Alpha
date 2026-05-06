import { createSentinelClient } from "@beezshield/sentinel";

import type { SentinelRiskCheckInput, SentinelRiskCheckResult } from "./types.js";

/**
 * Action Provider-style prototype only.
 * Not an official Coinbase AgentKit provider.
 * Local/test-only sketch showing where an AgentKit Action Provider could call Sentinel.
 */
export async function sentinelRiskCheckAction(input: SentinelRiskCheckInput): Promise<SentinelRiskCheckResult> {
  const lane = input.lane ?? "basic";
  const chain = input.chain ?? "base";

  const sentinel = createSentinelClient({ lane });
  const decision = await sentinel.decideBeforeExecution({
    contract_address: input.contract_address,
    chain,
    context: {
      requested_action: input.requested_action,
      intent: input.intent,
    },
  });

  const recommendation = String(
    (decision as { recommendation?: string }).recommendation ??
      (decision as { action?: string }).action ??
      "review"
  ).toLowerCase();

  const action: "allow" | "review" | "block" =
    recommendation === "allow" ? "allow" : recommendation === "block" ? "block" : "review";

  const reason = action === "allow" ? "Sentinel recommended allow." : "Sentinel recommended caution path.";
  const confidence = (decision as { confidence?: number | string }).confidence ?? "unknown";
  const explanation =
    "Pre-execution risk decision mapped to allow/review/block policy assistance. Not a security guarantee.";

  return {
    action,
    reason,
    confidence,
    sentinelDecision: decision,
    explanation,
    notSecurityGuarantee: true,
  };
}
