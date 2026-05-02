import { afterEach, describe, expect, it, vi } from "vitest";
import {
  createSentinelClient,
  decideBeforeExecution,
  isX402Challenge,
  normalizeSentinelDecision,
  scoreContract,
  SentinelNetworkError,
  SentinelPaymentRequiredError,
  SentinelTimeoutError,
  SentinelValidationError,
} from "./index.js";

const sample200 = {
  api_version: "2026.8.0",
  decision: {
    action: "ALLOW",
    emergency_signal: "NONE",
    confidence: 0.75,
  },
  risk_metrics: { score: 12, threat_class: "normal" },
  signals: { insufficient_data: 1 },
  attestation: { signed_at: "2026-01-01T00:00:00Z" },
  latency: { lane: "standard", latency_ms: 5 },
  meta: { trace_id: "abc", ttl_seconds: 300 },
  billing: { amount: "0.02", method: "x402", status: "demo" },
};

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("createSentinelClient", () => {
  it("uses default apiUrl, lane, timeout", () => {
    const c = createSentinelClient();
    expect(c).toBeDefined();
  });

  it("sends required headers on POST", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(sample200), { status: 200, headers: { "Content-Type": "application/json" } }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const client = createSentinelClient({ apiUrl: "https://example.test/" });
    await client.scoreContract({
      contract_address: "0x1111111111111111111111111111111111111111",
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("https://example.test/contracts/risk-score");
    const headers = init.headers as Record<string, string>;
    expect(headers["Content-Type"]).toBe("application/json");
    expect(headers["X-SENTINEL-LANE"]).toBe("basic");
    expect(headers["X402-PAYMENT"]).toBeUndefined();
    expect(JSON.parse(init.body as string)).toMatchObject({
      contract_address: "0x1111111111111111111111111111111111111111",
      chain: "base",
    });
  });

  it("sends X402-PAYMENT when configured", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(sample200), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const client = createSentinelClient({ x402Payment: "test-settlement-header" });
    await client.scoreContract({
      contract_address: "0x1111111111111111111111111111111111111111",
    });

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect((init.headers as Record<string, string>)["X402-PAYMENT"]).toBe("test-settlement-header");
  });
});

describe("scoreContract", () => {
  it("returns body on 200", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(JSON.stringify(sample200), { status: 200 })),
    );
    const out = await scoreContract(
      { contract_address: "0x1111111111111111111111111111111111111111" },
      { apiUrl: "https://api.test" },
    );
    expect(out.risk_metrics.score).toBe(12);
  });

  it("throws SentinelPaymentRequiredError on 402", async () => {
    const body = {
      detail: {
        x402_version: "0.2",
        payment_method: "x402",
        network: "eip155:8453",
        resource: "/contracts/risk-score",
      },
    };
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(JSON.stringify(body), { status: 402 })),
    );

    try {
      await scoreContract({ contract_address: "0x1111111111111111111111111111111111111111" });
      expect.fail("expected throw");
    } catch (e) {
      expect(e).toBeInstanceOf(SentinelPaymentRequiredError);
      expect((e as SentinelPaymentRequiredError).code).toBe("SENTINEL_X402");
      expect((e as SentinelPaymentRequiredError).challenge.resource).toBe("/contracts/risk-score");
    }
  });
});

describe("normalizeSentinelDecision", () => {
  it("maps API fields", () => {
    const d = normalizeSentinelDecision(sample200 as never);
    expect(d.score).toBe(12);
    expect(d.confidence).toBe(0.75);
    expect(d.action).toBe("ALLOW");
    expect(d.emergencySignal).toBe("NONE");
    expect(d.traceId).toBe("abc");
  });
});

describe("isX402Challenge", () => {
  it("detects SentinelPaymentRequiredError", () => {
    const err = new SentinelPaymentRequiredError({
      resource: "/contracts/risk-score",
      x402_version: "0.2",
      payment_method: "x402",
    });
    expect(isX402Challenge(err)).toBe(true);
  });

  it("detects FastAPI-shaped body", () => {
    expect(
      isX402Challenge({
        detail: {
          resource: "/contracts/risk-score",
          x402_version: "0.2",
          payment_method: "x402",
        },
      }),
    ).toBe(true);
  });
});

describe("decideBeforeExecution", () => {
  it("maps ALLOW to shouldExecute true", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(JSON.stringify(sample200), { status: 200 })),
    );
    const r = await decideBeforeExecution(
      { contract_address: "0x1111111111111111111111111111111111111111" },
      { apiUrl: "https://api.test" },
    );
    expect(r.shouldExecute).toBe(true);
    expect(r.action).toBe("allow");
    expect(r.score).toBe(12);
  });

  it("maps BLOCK to shouldExecute false", async () => {
    const blocked = {
      ...sample200,
      decision: { action: "BLOCK", emergency_signal: "NONE", confidence: 0.9 },
      risk_metrics: { score: 90, threat_class: "liquidity_rug" },
    };
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(JSON.stringify(blocked), { status: 200 })),
    );
    const r = await decideBeforeExecution(
      { contract_address: "0x1111111111111111111111111111111111111111" },
      { apiUrl: "https://api.test" },
    );
    expect(r.shouldExecute).toBe(false);
    expect(r.action).toBe("block");
  });
});

describe("errors", () => {
  it("invalid address throws SentinelValidationError before fetch", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    await expect(scoreContract({ contract_address: "not-an-address" })).rejects.toBeInstanceOf(
      SentinelValidationError,
    );
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("timeout yields SentinelTimeoutError", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((_u: string, init: RequestInit) => {
        return new Promise((_resolve, reject) => {
          const onAbort = () => {
            reject(Object.assign(new Error("aborted"), { name: "AbortError" }));
          };
          if (init.signal?.aborted) {
            onAbort();
            return;
          }
          init.signal?.addEventListener("abort", onAbort, { once: true });
        });
      }),
    );
    await expect(
      scoreContract(
        { contract_address: "0x1111111111111111111111111111111111111111" },
        { apiUrl: "https://slow.test", timeoutMs: 5 },
      ),
    ).rejects.toBeInstanceOf(SentinelTimeoutError);
  });

  it("network failure yields SentinelNetworkError", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(
      scoreContract({ contract_address: "0x1111111111111111111111111111111111111111" }),
    ).rejects.toBeInstanceOf(SentinelNetworkError);
  });
});
