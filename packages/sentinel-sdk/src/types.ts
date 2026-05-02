export type SentinelClientConfig = {
  /** Base URL of the Sentinel Alpha API */
  apiUrl?: string;
  /** Lane header (`X-SENTINEL-LANE`), default basic */
  lane?: string;
  /** Request abort timeout */
  timeoutMs?: number;
  /** Optional PAYMENT-SIGNATURE header (e.g. demo only in dev) */
  paymentHeader?: string;
  /** Optional X402-PAYMENT header when you have a valid settlement */
  x402Payment?: string;
};

export type ScoreContractInput = {
  contract_address: string;
  chain?: string;
  context?: Record<string, unknown> | null;
};

/** FastAPI 402 detail payload (shape may evolve) */
export type X402Challenge = {
  x402_version?: string;
  payment_method?: string;
  network?: string;
  pay_to?: string;
  amount_usdc?: string | number;
  asset?: string;
  resource?: string;
  instructions?: string;
  lane?: string;
  [key: string]: unknown;
};

export type SentinelRiskResponse = {
  api_version: string;
  decision: {
    action: string;
    emergency_signal: string;
    confidence: number;
  };
  risk_metrics: {
    score: number;
    threat_class: string;
  };
  signals: Record<string, number | string | boolean | null | undefined>;
  attestation: Record<string, unknown>;
  latency: Record<string, unknown>;
  meta: Record<string, unknown>;
  billing: Record<string, unknown>;
};

export type SentinelDecision = {
  score: number;
  confidence: number;
  action: string;
  emergencySignal: string;
  threatClass: string;
  traceId?: string;
};

export type DecideBeforeExecutionResult = {
  shouldExecute: boolean;
  action: "allow" | "review" | "block";
  score: number;
  confidence: number;
  emergencySignal: string;
  raw: SentinelRiskResponse;
};
