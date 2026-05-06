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
};
