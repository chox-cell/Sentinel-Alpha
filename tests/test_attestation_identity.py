import hashlib

from services.attestation_layer.attestation import ENGINE_VERSION, build_attestation


def test_attestation_includes_identity_and_signature_stub():
    att = build_attestation(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        score=85,
        action="BLOCK",
        trace_id="trace-1",
    )

    assert "decision_fingerprint" in att
    assert "engine_version" in att
    assert "signed_at" in att
    assert att["attestation_version"] == "attestation-0.1"
    assert att["agent_identity"]["agent_name"] == "Sentinel Alpha"
    assert att["agent_identity"]["did"] == "did:sentinel-alpha:local"

    expected_sig = hashlib.sha256(
        f"{att['decision_fingerprint']}{att['agent_identity']['did']}{ENGINE_VERSION}".encode("utf-8")
    ).hexdigest()
    assert att["signature"] == f"sha256:{expected_sig}"
