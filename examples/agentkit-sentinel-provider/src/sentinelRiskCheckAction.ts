import { createSentinelClient } from "@beezshield/sentinel";
import { createHash } from "node:crypto";

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

  const chainForRef = String(chain || "base").toLowerCase();
  const requestedActionForRef = String(input.requested_action || "unknown").toLowerCase();
  const intentForRef = typeof input.intent === "string" ? input.intent : JSON.stringify(input.intent ?? "unknown");
  const contractHash = createHash("sha256").update(String(input.contract_address).toLowerCase()).digest("hex");
  const intentHash = createHash("sha256").update(intentForRef).digest("hex");
  const actionRefPayload = JSON.stringify({
    chain: chainForRef,
    contract_address_hash: contractHash,
    requested_action: requestedActionForRef,
    intent_hash: intentHash,
  });
  const action_ref = createHash("sha256").update(actionRefPayload).digest("hex");
  const sentinel_decision_ref = createHash("sha256")
    .update(
      JSON.stringify({
        action_ref,
        decision_action: action,
        confidence,
      })
    )
    .digest("hex");
  const payment_decision_link_ref = createHash("sha256")
    .update(
      JSON.stringify({
        sentinel_decision_ref,
        action_ref,
        payment_request_id: "demo-payment-request",
        payment_hash: null,
        payment_protocol: "x402",
        payment_status: "unknown",
      })
    )
    .digest("hex");

  return {
    action,
    reason,
    confidence,
    sentinelDecision: decision,
    explanation,
    notSecurityGuarantee: true,
    sentinel_decision_ref,
    action_ref,
    payment_decision_link_ref,
    payment_protocol: "x402",
    payment_status: "unknown",
    automatic_settlement_claimed: false,
    demoOnly: true,
  };
}
