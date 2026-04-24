import hashlib
import hmac


def verify_quicknode_signature(raw_body: bytes, signature: str | None, secret: str | None) -> bool:
    if not secret:
        # Dev mode: signature verification disabled.
        return True

    if not signature:
        return False

    expected = hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    provided = signature.strip()
    if provided.startswith("sha256="):
        provided = provided.split("=", 1)[1]

    return hmac.compare_digest(provided, expected)
