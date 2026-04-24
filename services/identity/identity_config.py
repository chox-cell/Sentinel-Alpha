import os


def get_identity_status() -> dict:
    identity_mode = (os.getenv("SENTINEL_IDENTITY_MODE") or "local_stub").strip() or "local_stub"
    did = (os.getenv("SENTINEL_AGENT_DID") or "did:sentinel-alpha:local").strip() or "did:sentinel-alpha:local"
    erc8004_contract = (os.getenv("SENTINEL_ERC8004_CONTRACT_ADDRESS") or "").strip()
    attestation_public_key = (os.getenv("SENTINEL_ATTESTATION_PUBLIC_KEY") or "").strip()

    return {
        "identity_mode": identity_mode,
        "did": did,
        "agent_name": "Sentinel Alpha",
        "engine_name": "Mycelium Engine",
        "attestation_version": "attestation-0.1",
        "erc8004_enabled": bool(erc8004_contract) and identity_mode == "erc8004",
        "real_key_enabled": bool(attestation_public_key) and identity_mode == "real_key",
    }
