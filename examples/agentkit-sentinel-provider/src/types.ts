export type SentinelRiskCheckInput = {
  contract_address: string;
  chain?: string;
  lane?: string;
  requested_action?: string;
  intent?: string;
};

export type SentinelRiskCheckAction = "allow" | "review" | "block";

export type SentinelRiskCheckResult = {
  action: SentinelRiskCheckAction;
  reason: string;
  confidence: number | string;
  sentinelDecision: unknown;
  explanation: string;
  notSecurityGuarantee: true;
  sentinel_decision_ref?: string;
  action_ref?: string;
  payment_decision_link_ref?: string;
  payment_protocol?: "x402" | "lightning" | "unknown";
  payment_status?: "required" | "authorized" | "settled" | "failed" | "unknown";
  automatic_settlement_claimed?: false;
  demoOnly?: true;
};
