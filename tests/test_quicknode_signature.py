import hashlib
import hmac

from services.scout_cell.signature import verify_quicknode_signature


def test_signature_verification_disabled_without_secret():
    assert verify_quicknode_signature(b'{"hello":"world"}', None, None) is True
    assert verify_quicknode_signature(b'{"hello":"world"}', "anything", "") is True


def test_signature_verification_fails_with_wrong_signature():
    raw = b'{"k":"v"}'
    assert verify_quicknode_signature(raw, "bad-signature", "secret") is False


def test_signature_verification_passes_with_valid_hmac():
    raw = b'{"k":"v"}'
    secret = "secret"
    signature = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()
    assert verify_quicknode_signature(raw, signature, secret) is True
