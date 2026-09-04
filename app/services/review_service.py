from datetime import datetime
from typing import Dict, List, Optional


REVIEW_QUEUE: Dict[str, dict] = {}


def create_review_case(
    transaction_id: str,
    agent_id: str,
    amount: float,
    risk_score: float,
    risk_reasons: List[str],
    evidence_file: Optional[str] = None
):

    case = {
        "case_id": f"review_{transaction_id}",
        "transaction_id": transaction_id,
        "agent_id": agent_id,
        "amount": amount,
        "risk_score": risk_score,
        "risk_reasons": risk_reasons,
        "evidence_file": evidence_file,
        "status": "PENDING",
        "razorpay_order": None,
        "created_at": datetime.utcnow().isoformat(),
        "reviewed_at": None
    }

    REVIEW_QUEUE[transaction_id] = case

    return case


def get_review_case(transaction_id: str):

    return REVIEW_QUEUE.get(transaction_id)


def get_all_review_cases():

    return list(REVIEW_QUEUE.values())


def approve_review(transaction_id: str):

    case = REVIEW_QUEUE.get(transaction_id)

    if not case:
        return None

    case["status"] = "APPROVED"

    case["reviewed_at"] = (
        datetime.utcnow().isoformat()
    )

    return case


def reject_review(transaction_id: str):

    case = REVIEW_QUEUE.get(transaction_id)

    if not case:
        return None

    case["status"] = "REJECTED"

    case["reviewed_at"] = (
        datetime.utcnow().isoformat()
    )

    return case