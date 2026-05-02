import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  createSentinelClient,
  decideBeforeExecution,
  scoreContract,
  SentinelError,
  SentinelX402ChallengeError,
  normalizeSentinelDecision,
  isX402Challenge,
} from "./index.js";

const SAMPLE_200 = {
  api_version: "2026.8.0",
  decision: { action: "ALLOW", emergency_signal: "NONE", confidence: 0.75 },
  risk_metrics: { score: 12, threat_class: "normal" },
  signals: { insufficient_data: 1 },
  attestation: { signed_at: "2026-01-01T00:00:00Z" },
  latency: { lane: "standard", latency_ms: 10 },
  meta: { trace_id: "t1" },
  billing: { amount: "0.02", method: "x402", status: "demo" },
};

const CHALLENGE_DETAIL = {
  x402_version: "0.2",
  payment_method: "x402",
  network: "eip155:8453",
  pay_to: "0xabc0000000000000000000000000000000000000",
  amount_usdc: "0.02",
  asset: "USDC",
  resource: "/contracts/risk-score",
  instructions: "Pay",
  lane: "basic",
};

describe("createSentinelClient", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        Response.json(SAMPLE_200, {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );
  });
  afterEach(() => vi.unstubAllGlobals());

  it("defaults apiUrl lane timeout and PAYMENT-SIGNATURE", async () => {
    const client = createSentinelClient();
    expect(client.config.apiUrl).toBe("https://api.beezshield.com");
    expect(client.config.lane).toBe("basic");
    expect(client.config.timeoutMs).toBe(10000);

    await client.scoreContract({
      contractAddress: "0x1111111111111111111111111111111111111111",
    });

    expect(fetch).toHaveBeenCalledOnce();
    const [, init] = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls[0] as [string, RequestInit];
    const headers = new Headers(init.headers as HeadersInit);
    expect(headers.get("Content-Type")).toBe("application/json");
    expect(headers.get("X-SENTINEL-LANE")).toBe("basic");
    expect(headers.get("PAYMENT-SIGNATURE")).toBe("demo");
    expect(headers.get("X402-PAYMENT")).toBeNull();
    expect(JSON.parse(init.body as string)).toMatchObject({
      contract_address: "0x1111111111111111111111111111111111111111",
      chain: "base",
    });
  });

  it("sends X402-PAYMENT when configured", async () => {
    const client = createSentinelClient({
      x402Payment: 'token="fixture-not-secret"',
      paymentSignature: "should-not-send",
    });
    await client.scoreContract({ contractAddress: "0x1111111111111111111111111111111111111111" });
    const [, init] = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls[0] as [string, RequestInit];
    const headers = new Headers(init.headers as HeadersInit);
    expect(headers.get("X402-PAYMENT")).toBe('token="fixture-not-secret"');
    expect(headers.get("PAYMENT-SIGNATURE")).toBeNull();
  });

  it("normalizes 200 via normalizeSentinelDecision", () => {
    const d = normalizeSentinelDecision(SAMPLE_200);
    expect(d.action).toBe("allow");
    expect(d.score).toBe(12);
    expect(d.confidence).toBe(0.75);
    expect(d.emergencySignal).toBe("NONE");
    expect(d.threatClass).toBe("normal");
  });

  it("throws SentinelX402ChallengeError on 402", async () => {
    vi.mocked(fetch).mockImplementationOnce(async () =>
      Response.json({ detail: CHALLENGE_DETAIL }, { status: 402 }),
    );
    const client = createSentinelClient();
    await expect(
      client.scoreContract({ contractAddress: "0x1111111111111111111111111111111111111111" }),
    ).rejects.toMatchObject({ name: "SentinelX402ChallengeError", httpStatus: 402 });
  });

  it("isX402Challenge detects error and response shapes", async () => {
    vi.mocked(fetch).mockImplementationOnce(async () =>
      Response.json({ detail: CHALLENGE_DETAIL }, { status: 402 }),
    );
    const client = createSentinelClient();
    try {
      await client.scoreContract({ contractAddress: "0x1111111111111111111111111111111111111111" });
    } catch (e) {
      expect(e).toBeInstanceOf(SentinelX402ChallengeError);
      expect(isX402Challenge(e)).toBe(true);
    }
    expect(isX402Challenge({ detail: CHALLENGE_DETAIL })).toBe(true);
  });

  it("decideBeforeExecution maps allow to shouldExecute true", async () => {
    const client = createSentinelClient();
    const d = await client.decideBeforeExecution({
      contractAddress: "0x1111111111111111111111111111111111111111",
    });
    expect(d.shouldExecute).toBe(true);
    expect(d.action).toBe("allow");
    expect(d.raw).toEqual(SAMPLE_200);
  });

  it("decideBeforeExecution maps block to shouldExecute false", async () => {
    vi.mocked(fetch).mockImplementationOnce(async () =>
      Response.json(
        {
          ...SAMPLE_200,
          decision: { action: "BLOCK", emergency_signal: "NONE", confidence: 0.9 },
          risk_metrics: { score: 90, threat_class: "insufficient_data" },
        },
        { status: 200 },
      ),
    );
    const client = createSentinelClient();
    const d = await client.decideBeforeExecution({
      contractAddress: "0x1111111111111111111111111111111111111111",
    });
    expect(d.shouldExecute).toBe(false);
    expect(d.action).toBe("block");
  });

  it("402 in decideBeforeExecution throws (no fabricated decision)", async () => {
    vi.mocked(fetch).mockImplementationOnce(async () =>
      Response.json({ detail: CHALLENGE_DETAIL }, { status: 402 }),
    );
    const client = createSentinelClient();
    await expect(client.decideBeforeExecution({ contractAddress: "0x1111111111111111111111111111111111111111" })).rejects.toBeInstanceOf(
      SentinelX402ChallengeError,
    );
  });

  it("rejects invalid address before fetch", async () => {
    const client = createSentinelClient();
    await expect(client.scoreContract({ contractAddress: "not-an-address" })).rejects.toMatchObject({
      code: "VALIDATION",
    });
    expect(fetch).not.toHaveBeenCalled();
  });

  it("maps timeout to SentinelError TIMEOUT", async () => {
    vi.mocked(fetch).mockImplementationOnce(
      (_, init) =>
        new Promise((_res, rej) => {
          const signal = init?.signal as AbortSignal;
          if (signal.aborted) {
            const err = new Error("Aborted");
            err.name = "AbortError";
            rej(err);
            return;
          }
          signal?.addEventListener("abort", () => {
            const err = new Error("Aborted");
            err.name = "AbortError";
            rej(err);
          });
        }),
    );
    const client = createSentinelClient({ timeoutMs: 20 });
    await expect(client.scoreContract({ contractAddress: "0x2222222222222222222222222222222222222222" })).rejects.toMatchObject({
      code: "TIMEOUT",
    });
  });

  it("maps network failures to SentinelError NETWORK", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("offline"));
    const client = createSentinelClient();
    await expect(client.scoreContract({ contractAddress: "0x2222222222222222222222222222222222222222" })).rejects.toMatchObject({
      code: "NETWORK",
    });
  });
});

describe("standalone scoreContract with config override", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("respects overrides without mutating default client", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (_u, init) => {
        const headers = new Headers(init?.headers as HeadersInit);
        expect(headers.get("X-SENTINEL-LANE")).toBe("executive");
        return Response.json(SAMPLE_200);
      }),
    );

    await scoreContract({ contractAddress: "0x1111111111111111111111111111111111111111", lane: "executive" });
    vi.mocked(fetch).mockClear();
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        Response.json({
          ...SAMPLE_200,
          decision: { action: "REVIEW", confidence: 0.5, emergency_signal: "NONE" },
          risk_metrics: { score: 40, threat_class: "normal" },
        }),
      ),
    );
    await decideBeforeExecution(
      { contractAddress: "0x1111111111111111111111111111111111111111" },
      { lane: "basic", apiUrl: "https://stub.example.invalid" },
    );
    expect((fetch as unknown as ReturnType<typeof vi.fn>).mock.calls[0][0]).toBe(
      "https://stub.example.invalid/contracts/risk-score",
    );
  });
});
