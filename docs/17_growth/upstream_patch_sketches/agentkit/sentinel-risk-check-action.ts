import { createSentinelClient } from "@beezshield/sentinel";

/**
 * Local-only optional example.
 * Not submitted upstream.
 * regression evidence only, not a security guarantee.
 * official provider coming next.
 */
export async function sentinelRiskCheckAction(contract_address: string) {
  const sentinel = createSentinelClient({ lane: "basic" });
  const decision = await sentinel.decideBeforeExecution({
    contract_address,
    chain: "base",
  });

  // allow/review/block policy assistance mapping
  if (decision.recommendation === "allow") return "allow";
  if (decision.recommendation === "review") return "review";
  return "block";
}

