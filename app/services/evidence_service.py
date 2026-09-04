import json
import os
from datetime import datetime, timezone


EVIDENCE_DIR = "evidence"


def generate_evidence_packet(
    mandate,
    transaction,
    verification,
    risk_score,
    risk_reasons,
    action
):

    # Optional fields ko safely read karo
    timestamp = getattr(transaction, "timestamp", None)
    user_intent = getattr(transaction, "user_intent", None)

    packet = {

        "evidence_id":
            f"EVD-{transaction.transaction_id}",

        "generated_at":
            datetime.now(timezone.utc).isoformat(),

        "agent": {

            "agent_id":
                transaction.agent_id
        },

        "mandate": {

            "max_spending":
                mandate.max_spending,

            "allowed_categories":
                mandate.allowed_categories,

            "allowed_merchants":
                mandate.allowed_merchants,

            "expires_at":
                str(mandate.expires_at)
            if mandate.expires_at is not None
            else None
        },

        "transaction": {

            "transaction_id":
                transaction.transaction_id,

            "product_name":
                transaction.product_name,

            "category":
                transaction.category,

            "merchant_id":
                transaction.merchant_id,

            "amount":
                transaction.amount,

            "currency":
                getattr(transaction, "currency", "INR"),

            "timestamp":
                str(timestamp)
            if timestamp is not None
            else None,

            "user_intent":
                user_intent
        },

        "verification":
            verification,

        "risk_analysis": {

            "risk_score":
                risk_score,

            "risk_reasons":
                risk_reasons
        },

        "decision": {

            "action":
                action
        }
    }

    return packet


def save_evidence_packet(packet):

    os.makedirs(
        EVIDENCE_DIR,
        exist_ok=True
    )

    path = os.path.join(
        EVIDENCE_DIR,
        f"{packet['evidence_id']}.json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            packet,
            f,
            indent=4,
            default=str
        )

    return path