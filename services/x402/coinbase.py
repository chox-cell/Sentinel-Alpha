import os
from dotenv import load_dotenv

load_dotenv()

def verify_demo_payment(payment_signature: str | None) -> bool:
    expected = os.getenv("PAYMENT_DEMO_SIGNATURE", "demo")
    return payment_signature == expected
