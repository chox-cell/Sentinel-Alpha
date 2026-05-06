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
  };

  console.log(JSON.stringify(sanitized, null, 2));
}

runDemo().catch((error) => {
  console.error("Local demo failed:", error);
  process.exit(1);
});
