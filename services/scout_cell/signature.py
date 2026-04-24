import hashlib
import hmac
import logging


logger = logging.getLogger(__name__)


def _normalize_signature(signature: str | None) -> str:
    provided = (signature or "").strip()
    if provided.startswith("sha256="):
        provided = provided.split("=", 1)[1]
    return provided


def verify_quicknode_signature(
    raw_body: bytes,
    signature: str | None,
    secret: str | None,
    nonce: str | None = None,
    timestamp: str | None = None,
) -> bool:
    if not secret:
        # Dev mode: signature verification disabled.
        return True

    provided = _normalize_signature(signature)
    if not provided:
        logger.warning(
            "QuickNode signature mismatch: missing signature (nonce_present=%s timestamp_present=%s body_len=%s)",
            bool(nonce),
            bool(timestamp),
            len(raw_body or b""),
        )
        return False

    ts = timestamp or ""
    nc = nonce or ""
    candidates = [
        raw_body,  # A) raw_body
        (ts + nc).encode("utf-8") + raw_body,  # B) timestamp + nonce + raw_body
        (nc + ts).encode("utf-8") + raw_body,  # C) nonce + timestamp + raw_body
        ts.encode("utf-8") + raw_body,  # D) timestamp + raw_body
    ]
    secret_bytes = secret.encode("utf-8")

    for candidate in candidates:
        expected = hmac.new(secret_bytes, candidate, hashlib.sha256).hexdigest()
        if hmac.compare_digest(provided, expected):
            return True

    logger.warning(
        "QuickNode signature mismatch: signature_present=%s nonce_present=%s timestamp_present=%s body_len=%s",
        bool(provided),
        bool(nonce),
        bool(timestamp),
        len(raw_body or b""),
    )
    return False
