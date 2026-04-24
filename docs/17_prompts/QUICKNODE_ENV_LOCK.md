# QUICKNODE ENV LOCK v0.1

Goal:
- Validate required QuickNode configuration safely before live webhook traffic.

Implementation:
- `shared/config/env.py`

Functions:
- `get_env_bool(name: str, default: bool = False) -> bool`
- `get_required_env(name: str) -> str`
- `get_quicknode_env_status() -> dict`

QuickNode env status shape:
- `webhook_url_configured: bool`
- `webhook_secret_configured: bool`
- `dry_run: bool`
- `signature_mode: "enabled" | "dev-disabled"`

Health endpoint:
- `GET /webhooks/quicknode/health` includes `quicknode_env_status`
- Must not expose secret values.
