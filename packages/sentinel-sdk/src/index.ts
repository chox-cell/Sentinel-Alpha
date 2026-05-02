export type {
  DecideBeforeExecutionResult,
  NormalizedSentinelAction,
  ResolvedSentinelClientConfig,
  ScoreContractInput,
  SentinelClientConfig,
  SentinelDecision,
  SentinelRiskResponse,
  X402Challenge,
} from "./types.js";

export { SentinelError } from "./errors.js";
export type { SentinelErrorCode } from "./errors.js";
export { SentinelX402ChallengeError } from "./errors.js";

export { normalizeSentinelDecision } from "./normalize.js";
export { isX402Challenge } from "./x402.js";

export {
  createSentinelClient,
  decideBeforeExecution,
  scoreContract,
} from "./client.js";
export type { SentinelClient } from "./client.js";
