/** Client configuration (no secrets required for unpaid / challenge flows). */
export type SentinelClientConfig = {
  /** Base URL without trailing slash. Default: production API host. */
  apiUrl?: string;
  /** Pricing lane header. Default: `basic`. */
  lane?: string;
  /** Request timeout in milliseconds. Default: `10000`. */
  timeoutMs?: number;
  /**
   * Value for `PAYMENT-SIGNATURE` when not using a settled `X402-PAYMENT`.
   * Default: `demo` (typically yields HTTP 402 until a real settlement header is supplied).
   */
  paymentSignature?: string;
  /** Alias for `paymentSignature`. */
  paymentHeader?: string;
  /** Settled x402 payload; when set, sent as `X402-PAYMENT` only (no automatic settlement). */
  x402Payment?: string;
};

export type ResolvedSentinelClientConfig = {
  apiUrl: string;
  lane: string;
  timeoutMs: number;
  /** Used only when `x402Payment` is unset */
  paymentSignature: string;
  x402Payment?: string;
};

export type ScoreContractInput = {
  contractAddress: string;
  chain?: string;
  context?: Record<string, unknown> | null;
  /** Overrides `config.lane` for this call. */
  lane?: string;
};

/** Raw `/contracts/risk-score` success body (snake_case mirrors the API). */
export type SentinelRiskResponse = {
  api_version: string;
  decision: {
    action: string;
    confidence: number;
    emergency_signal: string;
  };
  risk_metrics: {
    score: number;
    threat_class: string;
  };
  signals: Record<string, number>;
  attestation: Record<string, unknown>;
  latency: {
    lane: string;
    latency_ms: number;
  };
  meta: Record<string, unknown>;
  billing: Record<string, unknown>;
};

export type NormalizedSentinelAction = "allow" | "review" | "block" | "reduce" | "exit_now";

export type SentinelDecision = {
  action: NormalizedSentinelAction;
  score: number;
  confidence: number;
  emergencySignal: string;
  threatClass: string;
  raw: SentinelRiskResponse;
};

export type DecideBeforeExecutionResult = {
  shouldExecute: boolean;
  action: NormalizedSentinelAction;
  score: number;
  confidence: number;
  emergencySignal: string;
  raw: SentinelRiskResponse;
};

/** Parsed x402 challenge (camelCase). */
export type X402Challenge = {
  x402Version: string;
  paymentMethod: string;
  network: string;
  payTo: string;
  amountUsdc: string;
  asset: string;
  resource: string;
  instructions: string;
  lane: string;
};
