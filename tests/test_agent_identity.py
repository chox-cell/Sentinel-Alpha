from services.identity.agent_identity import get_agent_identity


def test_get_agent_identity_shape_and_values():
    identity = get_agent_identity()

    assert identity == {
        "agent_name": "Sentinel Alpha",
        "engine_name": "Mycelium Engine",
        "agent_system": "Sentinel Cells",
        "primary_endpoint": "/contracts/risk-score",
        "identity_version": "identity-0.1",
        "did": "did:sentinel-alpha:local",
    }
