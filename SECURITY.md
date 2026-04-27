# Security Policy

## No Secrets Policy

- Never commit `.env`, private keys, API keys, or webhook secrets.
- Keep production credentials only in secure environment management systems.
- Public docs and manifests must never contain secret values.

## Reporting Security Issues

Please report potential vulnerabilities privately to:

- `security@your-domain.example` (placeholder contact)

Do not open public issues for active vulnerabilities.

## Production Environment Warning

- Use production-safe settings before enabling public traffic.
- Do not enable mock verification in production.
- Rotate credentials immediately if accidental exposure is suspected.
