import { SentinelValidationError } from "./errors.js";

const ADDR = /^0x[a-fA-F0-9]{40}$/;

export function assertValidContractAddress(address: string): void {
  if (!ADDR.test((address || "").trim())) {
    throw new SentinelValidationError("Invalid contract_address (expected 0x + 40 hex chars)");
  }
}

export function isValidContractAddress(address: string): boolean {
  return ADDR.test((address || "").trim());
}
