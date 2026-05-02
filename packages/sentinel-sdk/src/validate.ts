import { SentinelError } from "./errors.js";

const EVM_ADDRESS = /^0x[a-fA-F0-9]{40}$/;

export function assertValidContractAddress(contractAddress: string): void {
  const v = (contractAddress ?? "").trim();
  if (!EVM_ADDRESS.test(v)) {
    throw new SentinelError("contractAddress must be a 42-char hex EVM address (0x + 40 hex).", "VALIDATION");
  }
}
