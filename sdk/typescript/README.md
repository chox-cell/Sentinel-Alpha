# Sentinel Alpha TypeScript SDK Stub

Lightweight fetch-based client for Sentinel Alpha.

## Usage

```ts
import { SentinelAlphaClient } from "./client";

const client = new SentinelAlphaClient(
  "http://localhost:8000",
  "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
);

const result = await client.scan("0x1111111111111111111111111111111111111111", "base");
console.log(result);
```

## API

- `new SentinelAlphaClient(baseUrl, paymentHeader?)`
- `scan(contractAddress, chain = "base")`
