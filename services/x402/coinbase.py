import os
from dotenv import load_dotenv

load_dotenv()


def verify_demo_payment(payment_signature: str | None) -> bool:
    expected = os.getenv("PAYMENT_DEMO_SIGNATURE", "demo")
    return payment_signature == expected


def verify_real_payment_placeholder(x402_payment_header: str | None) -> bool:
    # v0.1 placeholder only: syntactic check while settlement integration is pending.
    value = (x402_payment_header or "").strip()
    return bool(value)
