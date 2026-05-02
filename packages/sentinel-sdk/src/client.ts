import { SentinelError } from "./errors.js";
import { SentinelX402ChallengeError } from "./errors.js";
import type {
  DecideBeforeExecutionResult,
  ResolvedSentinelClientConfig,
  ScoreContractInput,
  SentinelClientConfig,
  SentinelRiskResponse,
} from "./types.js";
import { normalizeSentinelDecision, shouldExecuteForAction } from "./normalize.js";
import { parseX402Detail } from "./x402.js";
import { assertValidContractAddress } from "./validate.js";

const DEFAULT_API_URL = "https://api.beezshield.com";
const DEFAULT_TIMEOUT_MS = 10_000;

function resolveConfig(config: SentinelClientConfig): ResolvedSentinelClientConfig {
  const resolved: ResolvedSentinelClientConfig = {
    apiUrl: (config.apiUrl ?? DEFAULT_API_URL).replace(/\/+$/, ""),
    lane: (config.lane ?? "basic").trim().toLowerCase() || "basic",
    timeoutMs: config.timeoutMs ?? DEFAULT_TIMEOUT_MS,
    paymentSignature: config.paymentSignature ?? config.paymentHeader ?? "demo",
  };
  if (config.x402Payment !== undefined) {
    resolved.x402Payment = config.x402Payment;
  }
  return resolved;
}

async function parseJsonSafe(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return null;
  }
}

function buildHeaders(resolved: ResolvedSentinelClientConfig, lane: string): Record<string, string> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-SENTINEL-LANE": lane,
  };
  if (resolved.x402Payment) {
    headers["X402-PAYMENT"] = resolved.x402Payment;
  } else {
    headers["PAYMENT-SIGNATURE"] = resolved.paymentSignature;
  }
  return headers;
}

export type SentinelClient = {
  readonly config: ResolvedSentinelClientConfig;
  scoreContract(input: ScoreContractInput): Promise<SentinelRiskResponse>;
  decideBeforeExecution(input: ScoreContractInput): Promise<DecideBeforeExecutionResult>;
};

export function createSentinelClient(config: SentinelClientConfig = {}): SentinelClient {
  const resolved = resolveConfig(config);

  async function scoreContract(input: ScoreContractInput): Promise<SentinelRiskResponse> {
    assertValidContractAddress(input.contractAddress);

    const lane = (input.lane ?? resolved.lane).trim().toLowerCase() || "basic";
    const url = `${resolved.apiUrl}/contracts/risk-score`;
    const body = {
      contract_address: input.contractAddress.trim(),
      chain: (input.chain ?? "base").trim().toLowerCase() || "base",
      context: input.context ?? null,
    };

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), resolved.timeoutMs);

    let response: Response;
    try {
      response = await fetch(url, {
        method: "POST",
        headers: buildHeaders(resolved, lane),
        body: JSON.stringify(body),
        signal: controller.signal,
      });
    } catch (err) {
      clearTimeout(timer);
      if (err instanceof Error && err.name === "AbortError") {
        throw new SentinelError(`Request timed out after ${resolved.timeoutMs}ms`, "TIMEOUT", { cause: err });
      }
      throw new SentinelError("Network request failed", "NETWORK", { cause: err });
    } finally {
      clearTimeout(timer);
    }

    const payload = await parseJsonSafe(response);

    if (response.status === 402) {
      const root = payload && typeof payload === "object" ? (payload as Record<string, unknown>) : null;
      const detail = root?.detail;
      if (!detail || typeof detail !== "object") {
        throw new SentinelError("HTTP 402 without x402 challenge detail", "UNSUPPORTED_RESPONSE");
      }
      throw new SentinelX402ChallengeError(parseX402Detail(detail as Record<string, unknown>));
    }

    if (!response.ok) {
      throw new SentinelError(`HTTP ${response.status} from risk-score`, "UNKNOWN");
    }

    if (!payload || typeof payload !== "object") {
      throw new SentinelError("Non-JSON or empty success body", "UNSUPPORTED_RESPONSE");
    }

    return payload as SentinelRiskResponse;
  }

  async function decideBeforeExecution(input: ScoreContractInput): Promise<DecideBeforeExecutionResult> {
    const raw = await scoreContract(input);
    const n = normalizeSentinelDecision(raw);
    return {
      shouldExecute: shouldExecuteForAction(n.action),
      action: n.action,
      score: n.score,
      confidence: n.confidence,
      emergencySignal: n.emergencySignal,
      raw,
    };
  }

  return { config: resolved, scoreContract, decideBeforeExecution };
}

let _defaultClient: SentinelClient | null = null;

function getDefaultClient(): SentinelClient {
  if (!_defaultClient) _defaultClient = createSentinelClient({});
  return _defaultClient;
}

/** Score a contract using optional config override (merges with defaults for that call only). */
export async function scoreContract(
  input: ScoreContractInput,
  configOverride?: SentinelClientConfig,
): Promise<SentinelRiskResponse> {
  const client = configOverride ? createSentinelClient(configOverride) : getDefaultClient();
  return client.scoreContract(input);
}

export async function decideBeforeExecution(
  input: ScoreContractInput,
  configOverride?: SentinelClientConfig,
): Promise<DecideBeforeExecutionResult> {
  const client = configOverride ? createSentinelClient(configOverride) : getDefaultClient();
  return client.decideBeforeExecution(input);
}
