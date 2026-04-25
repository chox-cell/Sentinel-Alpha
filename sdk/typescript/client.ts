export type ScanRequest = {
  contract_address: string;
  chain?: string;
  context?: Record<string, unknown> | null;
};

export class SentinelAlphaClient {
  baseUrl: string;
  paymentHeader?: string;

  constructor(baseUrl: string, paymentHeader?: string) {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.paymentHeader = paymentHeader;
  }

  async scan(contractAddress: string, chain = "base"): Promise<Record<string, unknown>> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.paymentHeader) {
      headers["X402-PAYMENT"] = this.paymentHeader;
    } else {
      headers["PAYMENT-SIGNATURE"] = "demo";
    }

    const payload: ScanRequest = {
      contract_address: contractAddress,
      chain,
      context: null,
    };

    const response = await fetch(`${this.baseUrl}/contracts/risk-score`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Sentinel Alpha scan failed: ${response.status}`);
    }
    return (await response.json()) as Record<string, unknown>;
  }
}
