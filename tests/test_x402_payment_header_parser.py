from services.x402.coinbase import parse_x402_payment_header


def test_parse_x402_payment_header_valid():
    tx_hash = "0x" + ("a" * 64)
    parsed = parse_x402_payment_header(f"tx:{tx_hash}")
    assert parsed == {"ok": True, "kind": "tx", "tx_hash": tx_hash}


def test_parse_x402_payment_header_invalid_prefix():
    parsed = parse_x402_payment_header("sig:0x" + ("a" * 64))
    assert parsed["ok"] is False
    assert parsed["error"] == "invalid_prefix"


def test_parse_x402_payment_header_invalid_hash_shape():
    parsed = parse_x402_payment_header("tx:0x1234")
    assert parsed["ok"] is False
    assert parsed["error"] == "invalid_tx_hash_shape"
