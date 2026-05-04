import {
  createSentinelClient,
  SentinelPaymentRequiredError,
  type DecideBeforeExecutionResult,
} from "@beezshield/sentinel";

type ContractExecutionRequest = {
  contract_address: string;
  chain?: string;
};

async function executeContractInteraction(input: ContractExecutionRequest): Promise<void> {
  // Placeholder only. Real wallet / tx execution is intentionally out of scope.
  console.log("Execution placeholder:", input.contract_address, input.chain ?? "base");
}

function readConfig() {
  return {
    apiUrl: process.env.SENTINEL_API_URL || "https://api.beezshield.com",
    lane: process.env.SENTINEL_LANE || "basic",
    x402Payment: process.env.X402_PAYMENT || undefined,
  };
}

function logPolicyDecision(result: DecideBeforeExecutionResult): void {
  console.log("Sentinel decision:", {
    action: result.action,
    shouldExecute: result.shouldExecute,
    score: result.score,
    confidence: result.confidence,
    emergencySignal: result.emergencySignal,
  });
}

export async function runAgentkitStyleFlow(input: ContractExecutionRequest): Promise<void> {
  const config = readConfig();
  const sentinel = createSentinelClient({
    apiUrl: config.apiUrl,
    lane: config.lane,
    x402Payment: config.x402Payment,
  });

  try {
    const decision = await sentinel.decideBeforeExecution({
      contract_address: input.contract_address,
      chain: input.chain ?? "base",
    });

    logPolicyDecision(decision);

    if (decision.shouldExecute) {
      await executeContractInteraction(input);
      return;
    }

    // REVIEW/BLOCK path: route to manual review, alerting, or policy fallback.
    console.warn("Blocked by Sentinel policy gate:", decision.action);
  } catch (error) {
    if (error instanceof SentinelPaymentRequiredError) {
      console.error("x402 payment challenge received. Provide a valid X402_PAYMENT header value.");
      console.error("Challenge:", error.challenge);
      return;
    }

    throw error;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const contract_address = process.argv[2] || "0x1111111111111111111111111111111111111111";
  runAgentkitStyleFlow({ contract_address }).catch((err) => {
    console.error("Example failed:", err);
    process.exit(1);
  });
}
