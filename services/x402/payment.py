import os
from dotenv import load_dotenv
from fastapi import HTTPException
from services.x402.coinbase import verify_demo_payment

load_dotenv()

def require_payment(payment_signature: str | None):
    mode = os.getenv("PAYMENT_MODE", "demo")

    if mode == "demo":
        if not verify_demo_payment(payment_signature):
            raise HTTPException(status_code=402, detail="Payment Required")
        return

    raise HTTPException(status_code=501, detail="Real payment mode not wired yet")
