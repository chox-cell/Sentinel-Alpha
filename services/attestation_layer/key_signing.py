import hashlib
import hmac
import os
from typing import Literal


def get_attestation_private_key() -> str | None:
    value = (os.getenv("SENTINEL_ATTESTATION_PRIVATE_KEY") or "").strip()
    return value or None


def get_attestation_public_key() -> str | None:
    value = (os.getenv("SENTINEL_ATTESTATION_PUBLIC_KEY") or "").strip()
    return value or None


def get_signing_mode() -> Literal["stub", "real_key"]:
    return "real_key" if get_attestation_private_key() else "stub"


def sign_attestation_message(message: str) -> str:
    mode = get_signing_mode()
    raw = str(message or "").encode("utf-8")
    if mode == "real_key":
        secret = get_attestation_private_key() or ""
        digest = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()
        return f"hmac-sha256:{digest}"

    digest = hashlib.sha256(raw).hexdigest()
    return f"sha256:{digest}"
