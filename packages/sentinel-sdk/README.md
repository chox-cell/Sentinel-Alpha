# @beezshield/sentinel

Minimal TypeScript client for **Sentinel Alpha** contract risk scoring over HTTPS, with typed **HTTP 402 x402 challenges** when payment is required.

## Publish status

**This package is not published to npm yet.** The npm name `@beezshield/sentinel` is the planned package name — **publish pending**.

Install locally from this repo after build:

```bash
cd packages/sentinel-sdk
npm install
npm run build
npm pack   # produces a tarball for local installs
```

Planned npm install once published:

```bash
npm install @beezshield/sentinel
```

_(Do not assume the registry tarball exists until release is announced.)_

## Quick start

```typescript
import {
  createSentinelClient,
  SentinelX402ChallengeError,
  isX402Challenge,
} from "@beezshield/sentinel";

const client = createSentinelClient({
  apiUrl: "https://api.beezshield.com",
  lane: "basic",
});

try {
  const raw = await client.scoreContract({
    contractAddress: "0x1111111111111111111111111111111111111111",
    chain: "base",
    context: { event_type: "new_deploy" },
  });
  console.log(raw.risk_metrics.score);
} catch (e) {
  if (e instanceof SentinelX402ChallengeError) {
    console.warn("Payment required:", e.challenge.amountUsdc, e.challenge.resource);
  }
  throw e;
}
```

Top-level helpers (defaults: production `apiUrl`, `lane: basic`, `timeoutMs: 10000`) are also exported:

```typescript
import { scoreContract } from "@beezshield/sentinel";

await scoreContract({ contractAddress: "0x…", chain: "base" }, { lane: "executive" });
```

## Headers

- Always sends `Content-Type: application/json` and **`X-SENTINEL-LANE`** (`basic` unless overridden).
- Sends **`X402-PAYMENT`** only when `x402Payment` is set on the client (you supply a settled payload from your payment flow — **automatic settlement is not implemented**).
- Otherwise sends **`PAYMENT-SIGNATURE`** (default `"demo"`; production typically responds with **HTTP 402** until a valid payment path is used).

## Handling x402 (402 Payment Required)

Successful paid traffic returns HTTP **200** with the risk payload. Without valid settlement:

- `scoreContract` / `decideBeforeExecution` **throw** **`SentinelX402ChallengeError`** with a camelCase **`challenge`** (`x402Version`, `payTo`, `amountUsdc`, `resource`, etc.).

Detect errors or opaque bodies with **`isX402Challenge`** when needed.

Normalize success bodies with **`normalizeSentinelDecision`**.

## Deciding before execution

```typescript
import { createSentinelClient, SentinelX402ChallengeError } from "@beezshield/sentinel";

const client = createSentinelClient();

try {
  const d = await client.decideBeforeExecution({
    contractAddress: "0x…",
    chain: "base",
  });

  console.log(d.shouldExecute, d.action, d.score, d.confidence, d.emergencySignal);
  // shouldExecute === true only when normalized action === "allow"
} catch (e) {
  if (e instanceof SentinelX402ChallengeError) {
    // Explicit payment-required path — never fabricates a fake allow/block decision.
    return;
  }
  throw e;
}
```

Actions map from the API uppercase strings to lowercase enum-style values (`allow`, `review`, `block`, `reduce`, `exit_now`).

## AgentKit Provider

An **official AgentKit provider for this SDK is not live yet**. Integrate manually with `fetch`/HTTP where needed until a packaged provider ships.

## License

MIT (see repository root `LICENSE` where applicable).
