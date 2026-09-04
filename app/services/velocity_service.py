from datetime import datetime, timedelta
from typing import Dict, List


# ============================================================
# IN-MEMORY TRANSACTION HISTORY
# ============================================================
# Demo/buildathon ke liye.
# Production version mein Redis / PostgreSQL use kiya ja sakta hai.

TRANSACTION_HISTORY: Dict[str, List[dict]] = {}


# ============================================================
# RECORD TRANSACTION
# ============================================================

def record_transaction(
    agent_id: str,
    transaction_id: str,
    amount: float,
    category: str,
    timestamp: datetime
):

    if agent_id not in TRANSACTION_HISTORY:
        TRANSACTION_HISTORY[agent_id] = []

    TRANSACTION_HISTORY[agent_id].append({

        "transaction_id": transaction_id,

        "amount": amount,

        "category": category,

        "timestamp": timestamp

    })


# ============================================================
# GET RECENT TRANSACTIONS
# ============================================================

def get_recent_transactions(
    agent_id: str,
    current_time: datetime,
    window_seconds: int = 300
):

    if agent_id not in TRANSACTION_HISTORY:
        return []

    cutoff_time = (
        current_time
        - timedelta(seconds=window_seconds)
    )

    recent = []

    for transaction in TRANSACTION_HISTORY[agent_id]:

        if transaction["timestamp"] >= cutoff_time:

            recent.append(transaction)

    return recent


# ============================================================
# CALCULATE PURCHASE VELOCITY
# ============================================================

def calculate_purchase_velocity(
    agent_id: str,
    current_time: datetime,
    window_seconds: int = 300
):

    recent_transactions = get_recent_transactions(
        agent_id=agent_id,
        current_time=current_time,
        window_seconds=window_seconds
    )

    return len(recent_transactions) + 1


# ============================================================
# VELOCITY RISK ANALYSIS
# ============================================================

def analyze_velocity(
    agent_id: str,
    current_time: datetime,
    window_seconds: int = 300
):

    recent_transactions = get_recent_transactions(
        agent_id=agent_id,
        current_time=current_time,
        window_seconds=window_seconds
    )

    velocity = len(recent_transactions) + 1

    if velocity >= 10:

        level = "CRITICAL"

        reason = (
            "Agent attempted an unusually large "
            "number of purchases in a short period."
        )

    elif velocity >= 5:

        level = "HIGH"

        reason = (
            "Agent purchase velocity is significantly "
            "higher than normal."
        )

    elif velocity >= 3:

        level = "MEDIUM"

        reason = (
            "Multiple purchases detected within "
            "a short time window."
        )

    else:

        level = "NORMAL"

        reason = (
            "Purchase velocity is within normal limits."
        )

    return {

        "velocity":
            velocity,

        "window_seconds":
            window_seconds,

        "recent_transaction_count":
            len(recent_transactions),

        "risk_level":
            level,

        "reason":
            reason,

        "recent_transactions":
            recent_transactions

    }


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_agent_history(agent_id: str):

    TRANSACTION_HISTORY.pop(
        agent_id,
        None
    )


def clear_all_history():

    TRANSACTION_HISTORY.clear()