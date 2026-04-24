import importlib


def test_basic_scan_module_is_import_safe():
    module = importlib.import_module("sdk.python.examples.basic_scan")
    assert callable(module.main)
