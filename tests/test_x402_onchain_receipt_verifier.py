import json

from services.x402.onchain_verifier import (
    BASE_USDC_ADDRESS,
    ERC20_TRANSFER_TOPIC0,
    verify_usdc_transfer_tx,
)


class _MockResp:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def _treasury_topic(treasury_40hex: str) -> str:
    h = treasury_40hex.lower().replace("0x", "")
    return "0x" + ("0" * 24) + h


def _make_receipt(*, status="0x1", logs=None, result_present=True):
    if not result_present:
        return {"jsonrpc": "2.0", "id": 1, "result": None}
    return {"jsonrpc": "2.0", "id": 1, "result": {"status": status, "logs": logs or []}}


def test_verified_transfer(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    treasury = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    amount_hex = hex(50_000)[2:].rjust(64, "0")

    def fake_post(url, data=None, headers=None, timeout=None):
        assert timeout == 8
        body = json.loads(data) if isinstance(data, str) else data
        assert body["method"] == "eth_getTransactionReceipt"
        txh = body["params"][0]
        assert txh.startswith("0x") and len(txh) == 66
        log = {
            "address": BASE_USDC_ADDRESS,
            "topics": [
                ERC20_TRANSFER_TOPIC0,
                "0x" + "0" * 24 + "11" * 20,
                _treasury_topic(treasury),
            ],
            "data": "0x" + amount_hex,
        }
        return _MockResp(200, _make_receipt(logs=[log]))

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    tx = "0x" + ("c" * 64)
    out = verify_usdc_transfer_tx(tx, expected_amount=0.02, treasury_wallet=treasury)
    assert out["verified"] is True
    assert out["status"] == "verified"
    assert out["tx_hash"] == tx
    assert out["amount_units"] == 50_000
    assert out["expected_units"] == 20_000
    assert out["treasury_wallet"] == treasury.lower()


def test_wrong_recipient(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    treasury = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    other = "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    amount_hex = hex(50_000)[2:].rjust(64, "0")

    def fake_post(url, data=None, headers=None, timeout=None):
        log = {
            "address": BASE_USDC_ADDRESS,
            "topics": [
                ERC20_TRANSFER_TOPIC0,
                "0x" + "0" * 24 + "11" * 20,
                _treasury_topic(other),
            ],
            "data": "0x" + amount_hex,
        }
        return _MockResp(200, _make_receipt(logs=[log]))

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("d" * 64),
        expected_amount=0.02,
        treasury_wallet=treasury,
    )
    assert out["verified"] is False
    assert out["status"] == "no_matching_usdc_transfer"


def test_amount_too_low(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    treasury = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    amount_hex = hex(5_000)[2:].rjust(64, "0")

    def fake_post(url, data=None, headers=None, timeout=None):
        log = {
            "address": BASE_USDC_ADDRESS,
            "topics": [
                ERC20_TRANSFER_TOPIC0,
                "0x" + "0" * 24 + "11" * 20,
                _treasury_topic(treasury),
            ],
            "data": "0x" + amount_hex,
        }
        return _MockResp(200, _make_receipt(logs=[log]))

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("e" * 64),
        expected_amount=0.02,
        treasury_wallet=treasury,
    )
    assert out["verified"] is False
    assert out["status"] == "amount_too_low"


def test_tx_failed(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    def fake_post(url, data=None, headers=None, timeout=None):
        return _MockResp(200, _make_receipt(status="0x0", logs=[]))

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("f" * 64),
        expected_amount=0.02,
        treasury_wallet="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    assert out["verified"] is False
    assert out["status"] == "tx_failed"


def test_receipt_not_found(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    def fake_post(url, data=None, headers=None, timeout=None):
        return _MockResp(200, _make_receipt(result_present=False))

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("1" * 64),
        expected_amount=0.02,
        treasury_wallet="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    assert out["verified"] is False
    assert out["status"] == "receipt_not_found"


def test_rpc_error_jsonrpc(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    def fake_post(url, data=None, headers=None, timeout=None):
        return _MockResp(
            200,
            {"jsonrpc": "2.0", "id": 1, "error": {"code": -32000, "message": "bad"}},
        )

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("2" * 64),
        expected_amount=0.02,
        treasury_wallet="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    assert out["verified"] is False
    assert out["status"] == "rpc_error"


def test_rpc_error_http(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    def fake_post(url, data=None, headers=None, timeout=None):
        return _MockResp(500, {})

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("3" * 64),
        expected_amount=0.02,
        treasury_wallet="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    assert out["verified"] is False
    assert out["status"] == "rpc_error"


def test_rpc_error_request_exception(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base.rpc.example")

    def fake_post(url, data=None, headers=None, timeout=None):
        raise OSError("network down")

    monkeypatch.setattr("services.x402.onchain_verifier.requests.post", fake_post)

    out = verify_usdc_transfer_tx(
        "0x" + ("4" * 64),
        expected_amount=0.02,
        treasury_wallet="0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    assert out["verified"] is False
    assert out["status"] == "rpc_error"
