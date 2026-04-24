import re

EVM_ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")

def is_valid_evm_address(address: str) -> bool:
    return bool(EVM_ADDRESS_RE.match(address or ""))

def is_probably_evm_like(address: str) -> bool:
    return isinstance(address, str) and address.startswith("0x")

def normalize_address(address: str) -> str:
    if not address:
        return ""
    return address.strip().lower()

def normalize_chain(chain: str) -> str:
    return (chain or "base").strip().lower()
