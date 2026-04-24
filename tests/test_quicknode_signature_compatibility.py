import hashlib
import hmac

from services.scout_cell.signature import verify_quicknode_signature


def _sig(secret: str, payload: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def test_signature_compatibility_raw_body():
    body = b'{"k":"v"}'
    secret = "secret"
    signature = _sig(secret, body)
    assert verify_quicknode_signature(body, signature, secret) is True


def test_signature_compatibility_timestamp_nonce_body():
    body = b'{"k":"v"}'
    secret = "secret"
    timestamp = "1730000000"
    nonce = "abc123"
    signature = _sig(secret, (timestamp + nonce).encode("utf-8") + body)
    assert verify_quicknode_signature(body, signature, secret, nonce=nonce, timestamp=timestamp) is True


def test_signature_compatibility_nonce_timestamp_body():
    body = b'{"k":"v"}'
    secret = "secret"
    timestamp = "1730000000"
    nonce = "abc123"
    signature = _sig(secret, (nonce + timestamp).encode("utf-8") + body)
    assert verify_quicknode_signature(body, signature, secret, nonce=nonce, timestamp=timestamp) is True


def test_signature_compatibility_timestamp_body():
    body = b'{"k":"v"}'
    secret = "secret"
    timestamp = "1730000000"
    signature = _sig(secret, timestamp.encode("utf-8") + body)
    assert verify_quicknode_signature(body, signature, secret, timestamp=timestamp) is True


def test_signature_compatibility_dev_disabled():
    assert verify_quicknode_signature(b"{}", None, None, nonce="n", timestamp="t") is True


def test_signature_compatibility_mismatch_returns_false():
    assert verify_quicknode_signature(b"{}", "bad", "secret", nonce="n", timestamp="t") is False
