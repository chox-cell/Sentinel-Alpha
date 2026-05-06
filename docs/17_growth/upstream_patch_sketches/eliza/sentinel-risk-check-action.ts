import { createSentinelClient } from "@beezshield/sentinel";

/**
 * Local-only optional example.
 * Not submitted upstream.
 * regression evidence only, not a security guarantee.
 * This is policy assistance, not a trading bot claim.
 */
export async function sentinelRiskCheckAction(contract_address: string) {
  const sentinel = createSentinelClient({ lane: "basic" });
  const decision = await sentinel.decideBeforeExecution({
    contract_address,
    chain: "base",
  });

  // allow/review/block policy assistance
  switch (decision.recommendation) {
    case "allow":
      return { route: "allow" };
    case "review":
      return { route: "review" };
    default:
      return { route: "block" };
  }
}

