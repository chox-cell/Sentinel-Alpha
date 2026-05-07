import { sentinelRiskCheckAction } from "./sentinelRiskCheckAction.js";

async function runDemo() {
  const result = await sentinelRiskCheckAction({
    contract_address: "0x1111111111111111111111111111111111111111",
    chain: "base",
    requested_action: "example_onchain_action",
    intent: "demo risk check before execution",
  });

  const sanitized = {
    action: result.action,
    reason: result.reason,
    confidence: result.confidence,
    explanation: result.explanation,
    notSecurityGuarantee: result.notSecurityGuarantee,
    sentinel_decision_ref: result.sentinel_decision_ref,
    action_ref: result.action_ref,
    payment_decision_link_ref: result.payment_decision_link_ref,
    payment_protocol: result.payment_protocol ?? "x402",
    payment_status: result.payment_status ?? "unknown",
    automatic_settlement_claimed: result.automatic_settlement_claimed ?? false,
    demoOnly: result.demoOnly ?? true,
  };

  console.log(JSON.stringify(sanitized, null, 2));
}

runDemo().catch((error) => {
  console.error("Local demo failed:", error);
  process.exit(1);
});
