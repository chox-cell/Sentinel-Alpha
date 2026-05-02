# @beezshield/sentinel

Minimal TypeScript SDK for Sentinel Alpha (**BeezShield**) — call `/contracts/risk-score`, normalize decisions, and handle **x402** payment challenges when no settlement header is supplied.

## Status / publishing

- **Planned package name:** `@beezshield/sentinel` — **`npm publish` is not done yet.** This package ships in-repo first (`packages/sentinel-sdk`).
- The SDK does **not** perform automatic x402 settlement. You supply `x402Payment` when you already have one, or handle the **`402`** challenge yourself.

Install from the workspace (until published):

```bash
npm install ./packages/sentinel-sdk
```

The following is the **canonical name after publish** (not live on npm today):

```bash
npm install @beezshield/sentinel
```

## Quick start

```ts
import {
  createSentinelClient,
  isX402Challenge,
  SentinelPaymentRequiredError,
} from "@beezshield/sentinel";

const client = createSentinelClient({
  // apiUrl defaults to https://api.beezshield.com
  // lane defaults to "basic"
  // timeoutMs defaults to 10000
});

try {
  const result = await client.scoreContract({
    contract_address: "0x1111111111111111111111111111111111111111",
    chain: "base",
  });
  console.log(result.risk_metrics.score);
} catch (e) {
  if (e instanceof SentinelPaymentRequiredError) {
    console.log("x402 challenge:", e.challenge);
  }
  throw e;
}
```

## x402 challenges

Without a valid `X402-PAYMENT` (or a dev-only `paymentHeader` you control), the API typically returns **HTTP 402**. The SDK throws `SentinelPaymentRequiredError` with a typed `challenge` parsed from the response body.

```ts
import { isX402Challenge, SentinelPaymentRequiredError } from "@beezshield/sentinel";

function handle(err: unknown) {
  if (err instanceof SentinelPaymentRequiredError || isX402Challenge(err)) {
    // Surface pay_to, amount_usdc, etc. from err.challenge when using SentinelPaymentRequiredError
    return "payment_required";
  }
}
```

## Decide before execution

Map the API decision to a simple execution gate (**not** legal/financial advice — your policy may differ later):

```ts
const gate = await client.decideBeforeExecution({
  contract_address: "0x…",
  chain: "base",
});
if (!gate.shouldExecute) {
  // block or review flows
}
```

- `ALLOW` → `shouldExecute: true`
- `REVIEW`, `REDUCE` → `shouldExecute: false` / `action: "review"`
- `BLOCK` or emergency `EXIT_NOW` → `shouldExecute: false` / `action: "block"`

## Configuration

| Field | Default | Notes |
|-------|---------|--------|
| `apiUrl` | `https://api.beezshield.com` | Trailing slashes stripped |
| `lane` | `basic` | Sent as `X-SENTINEL-LANE` |
| `timeoutMs` | `10000` | Abort via `AbortSignal` |
| `x402Payment` | — | Set `X402-PAYMENT` when you have a settlement |
| `paymentHeader` | — | Optional `PAYMENT-SIGNATURE` (e.g. local demo only) |

## AgentKit

**Coinbase AgentKit provider integration is not live in this package** — treat as a future extension; wire this client manually for now.

## Build

```bash
cd packages/sentinel-sdk
npm install
npm run build
npm test
```

## License

MIT
