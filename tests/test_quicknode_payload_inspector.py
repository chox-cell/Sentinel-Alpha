from services.scout_cell.payload_inspector import inspect_quicknode_payload


def test_inspect_quicknode_payload_summary_shape():
    payload = {
        "data": {
            "receipts": [{"logs": [{"address": "0x1"}, {"address": "0x2"}]}],
            "meta": {"chain": "base"},
        },
        "receipt": {"logs": [{"address": "0x3"}]},
        "logs": [{"address": "0x4"}],
    }

    summary = inspect_quicknode_payload(payload)
    assert summary["top_level_type"] == "dict"
    assert "data" in summary["top_level_keys"]
    assert summary["data_type"] == "dict"
    assert "receipts" in summary["data_keys"]
    assert isinstance(summary["possible_list_paths"], list)
    assert isinstance(summary["sample_paths_only"], list)
    assert summary["receipt_count_guess"] == 1
    assert summary["log_count_guess"] == 2


def test_inspect_quicknode_payload_handles_non_dict():
    summary = inspect_quicknode_payload({"data": ["a", "b", "c"]})
    assert summary["data_type"] == "list"
    assert "data" in summary["possible_list_paths"]
