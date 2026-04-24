import hashlib
from datetime import datetime, timezone

ENGINE_VERSION = "mycelium-wrsi-0.2"

def build_attestation(contract_address: str, chain: str, score: int, action: str, trace_id: str) -> dict:
    signed_at = datetime.now(timezone.utc).isoformat()

    raw = f"{contract_address}:{chain}:{score}:{action}:{trace_id}:{ENGINE_VERSION}:{signed_at}"
    fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    return {
        "decision_fingerprint": f"sha256:{fingerprint}",
        "engine_version": ENGINE_VERSION,
        "signed_at": signed_at,
    }
