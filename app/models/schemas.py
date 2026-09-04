from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Transaction(BaseModel):

    transaction_id: str
    agent_id: str
    user_id: Optional[str] = None

    product_name: str
    category: str
    merchant_id: str
    amount: float
    currency: str = "INR"

    timestamp: Optional[datetime] = None

    requested_category: Optional[str] = None
    requested_max_price: Optional[float] = None

    purchase_velocity: float = 1.0
    agent_behavior_score: float = 0.0

    user_intent: Optional[str] = None


class AgentMandate(BaseModel):

    agent_id: str
    user_id: Optional[str] = None

    max_spending: float
    allowed_categories: List[str]
    allowed_merchants: List[str]

    requested_category: Optional[str] = None
    requested_max_price: Optional[float] = None

    currency: str = "INR"
    active: bool = True
    expires_at: Optional[datetime] = None