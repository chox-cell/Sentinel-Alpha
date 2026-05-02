import type {
  DecideBeforeExecutionResult,
  ScoreContractInput,
  SentinelClientConfig,
  SentinelRiskResponse,
} from "./types.js";
import {
  SentinelHttpError,
  SentinelNetworkError,
  SentinelPaymentRequiredError,
  SentinelTimeoutError,
} from "./errors.js";
import { assertValidContractAddress } from "./validation.js";
import { normalizeSentinelDecision, parseX402ChallengeFromBody } from "./normalize.js";

const DEFAULT_API = "https://api.beezshield.com";
const DEFAULT_LANE = "basic";
const DEFAULT_TIMEOUT_MS = 10_000;

export type SentinelClient = {
  scoreContract(input: ScoreContractInput): Promise<SentinelRiskResponse>;
  decideBeforeExecution(input: ScoreContractInput): Promise<DecideBeforeExecutionResult>;
};

export function createSentinelClient(rawConfig?: SentinelClientConfig): SentinelClient {
  const cfg: Required<
    Pick<
      SentinelClientConfig,
      "apiUrl" | "lane" | "timeoutMs"
    >
  > &
    Pick<SentinelClientConfig, "paymentHeader" | "x402Payment"> = {
    apiUrl: rawConfig?.apiUrl?.replace(/\/+$/, "") ?? DEFAULT_API,
    lane: rawConfig?.lane?.trim()?.toLowerCase() || DEFAULT_LANE,
    timeoutMs:
      typeof rawConfig?.timeoutMs === "number" && rawConfig.timeoutMs > 0
        ? rawConfig.timeoutMs
        : DEFAULT_TIMEOUT_MS,
    paymentHeader: rawConfig?.paymentHeader,
    x402Payment: rawConfig?.x402Payment,
  };

  async function postRiskScore(
    payload: Record<string, unknown>,
  ): Promise<Response> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), cfg.timeoutMs);
    try {
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        "X-SENTINEL-LANE": cfg.lane,
      };
      if (cfg.x402Payment) {
        headers["X402-PAYMENT"] = cfg.x402Payment;
      }
      if (cfg.paymentHeader) {
        headers["PAYMENT-SIGNATURE"] = cfg.paymentHeader;
      }

      return await fetch(`${cfg.apiUrl}/contracts/risk-score`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") {
        throw new SentinelTimeoutError();
      }
      throw new SentinelNetworkError("Sentinel Alpha request failed", err);
    } finally {
      clearTimeout(timer);
    }
  }

  function assertRiskPayload(input: ScoreContractInput): Record<string, unknown> {
    assertValidContractAddress(input.contract_address);
    return {
      contract_address: input.contract_address.trim(),
      chain: (input.chain ?? "base").trim().toLowerCase(),
      context: input.context ?? null,
    };
  }

  async function runScore(input: ScoreContractInput): Promise<SentinelRiskResponse> {
    const payload = assertRiskPayload(input);
    let res: Response;
    try {
      res = await postRiskScore(payload);
    } catch (e) {
      if (e instanceof SentinelTimeoutError || e instanceof SentinelNetworkError) {
        throw e;
      }
      throw new SentinelNetworkError("Sentinel Alpha request failed", e);
    }

    const text = await res.text();
    let raw: unknown;
    try {
      raw = text ? JSON.parse(text) : null;
    } catch {
      throw new SentinelHttpError(res.status, "Invalid JSON from Sentinel Alpha", text);
    }

    if (res.status === 402) {
      const ch = parseX402ChallengeFromBody(raw);
      if (ch) {
        throw new SentinelPaymentRequiredError(ch);
      }
      throw new SentinelHttpError(402, "Payment required without x402 payload", raw);
    }

    if (!res.ok) {
      throw new SentinelHttpError(
        res.status,
        `Sentinel Alpha error (HTTP ${res.status})`,
        raw,
      );
    }

    return raw as SentinelRiskResponse;
  }

  return {
    scoreContract: runScore,
    async decideBeforeExecution(input: ScoreContractInput): Promise<DecideBeforeExecutionResult> {
      const raw = await runScore(input);
      const n = normalizeSentinelDecision(raw);
      const coarse = coarseAction(raw.decision.action, raw.decision.emergency_signal);
      return {
        shouldExecute: coarse === "allow",
        action: coarse,
        score: n.score,
        confidence: n.confidence,
        emergencySignal: n.emergencySignal,
        raw,
      };
    },
  };
}

function coarseAction(apiAction: string, emergencySignal: string): "allow" | "review" | "block" {
  const a = apiAction.trim().toUpperCase();
  if (emergencySignal === "EXIT_NOW") {
    return "block";
  }
  switch (a) {
    case "ALLOW":
      return "allow";
    case "BLOCK":
    case "EXIT_NOW":
      return "block";
    case "REDUCE":
    case "REVIEW":
    default:
      return "review";
  }
}

export async function scoreContract(
  input: ScoreContractInput,
  config?: SentinelClientConfig,
): Promise<SentinelRiskResponse> {
  return createSentinelClient(config).scoreContract(input);
}

export async function decideBeforeExecution(
  input: ScoreContractInput,
  config?: SentinelClientConfig,
): Promise<DecideBeforeExecutionResult> {
  const client = createSentinelClient(config);
  const raw = await client.scoreContract(input);
  const n = normalizeSentinelDecision(raw);
  const coarse = coarseAction(raw.decision.action, raw.decision.emergency_signal);
  return {
    shouldExecute: coarse === "allow",
    action: coarse,
    score: n.score,
    confidence: n.confidence,
    emergencySignal: n.emergencySignal,
    raw,
  };
}
