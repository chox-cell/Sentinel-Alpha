from pydantic import BaseModel
from typing import Optional, Dict, Any

class RiskScoreRequest(BaseModel):
    contract_address: str
    chain: str
    context: Optional[Dict[str, Any]] = None
