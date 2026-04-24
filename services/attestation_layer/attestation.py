import hashlib
from datetime import datetime, timezone

from services.attestation_layer.key_signing import get_signing_mode, sign_attestation_message
from services.identity.agent_identity import get_agent_identity

ENGINE_VERSION = "mycelium-wrsi-0.2"

def build_attestation(contract_address: str, chain: str, score: int, action: str, trace_id: str) -> dict:
    signed_at = datetime.now(timezone.utc).isoformat()
    agent_identity = get_agent_identity()

    raw = f"{contract_address}:{chain}:{score}:{action}:{trace_id}:{ENGINE_VERSION}:{signed_at}"
    fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    decision_fingerprint = f"sha256:{fingerprint}"
    signature_raw = f"{decision_fingerprint}{agent_identity['did']}{ENGINE_VERSION}"
    signature = sign_attestation_message(signature_raw)

    return {
        "decision_fingerprint": decision_fingerprint,
        "engine_version": ENGINE_VERSION,
        "signed_at": signed_at,
        "agent_identity": agent_identity,
        "attestation_version": "attestation-0.1",
        "signing_mode": get_signing_mode(),
        "signature": signature,
    }
