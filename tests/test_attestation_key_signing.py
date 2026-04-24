import hashlib
import hmac

from services.attestation_layer import key_signing


def test_signing_mode_stub_without_private_key(monkeypatch):
    monkeypatch.delenv("SENTINEL_ATTESTATION_PRIVATE_KEY", raising=False)
    assert key_signing.get_signing_mode() == "stub"
    sig = key_signing.sign_attestation_message("abc")
    assert sig == f"sha256:{hashlib.sha256(b'abc').hexdigest()}"


def test_signing_mode_real_key_with_private_key(monkeypatch):
    monkeypatch.setenv("SENTINEL_ATTESTATION_PRIVATE_KEY", "secret")
    assert key_signing.get_signing_mode() == "real_key"
    sig = key_signing.sign_attestation_message("abc")
    expected = hmac.new(b"secret", b"abc", hashlib.sha256).hexdigest()
    assert sig == f"hmac-sha256:{expected}"
