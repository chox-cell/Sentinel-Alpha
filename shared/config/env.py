import os


def get_env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not str(value).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(value).strip()


def get_quicknode_env_status() -> dict:
    webhook_url = os.getenv("QUICKNODE_WEBHOOK_URL")
    webhook_secret = os.getenv("QUICKNODE_WEBHOOK_SECRET")
    dry_run = get_env_bool("QUICKNODE_DRY_RUN", default=False)

    secret_configured = bool(str(webhook_secret or "").strip())
    return {
        "webhook_url_configured": bool(str(webhook_url or "").strip()),
        "webhook_secret_configured": secret_configured,
        "dry_run": dry_run,
        "signature_mode": "enabled" if secret_configured else "dev-disabled",
    }
