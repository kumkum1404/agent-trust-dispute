from datetime import datetime

from app.models.schemas import AgentMandate, Transaction


def verify_mandate(
    mandate: AgentMandate,
    transaction: Transaction
):
    violations = []

    # 1. Check agent identity
    if mandate.agent_id != transaction.agent_id:
        violations.append("AGENT_ID_MISMATCH")

    # 2. Check spending limit
    if transaction.amount > mandate.max_spending:
        violations.append("SPENDING_LIMIT_EXCEEDED")

    # 3. Check category
    if transaction.category.lower() not in [
        category.lower()
        for category in mandate.allowed_categories
    ]:
        violations.append("CATEGORY_NOT_ALLOWED")

    # 4. Check merchant
    if transaction.merchant_id not in mandate.allowed_merchants:
        violations.append("MERCHANT_NOT_ALLOWED")

    # 5. Check expiry
    try:
        expiry_time = datetime.fromisoformat(
            mandate.expires_at
        )

        transaction_time = datetime.fromisoformat(
            transaction.timestamp
        )

        if transaction_time > expiry_time:
            violations.append("MANDATE_EXPIRED")

    except ValueError:
        violations.append("INVALID_TIMESTAMP")

    # Final decision
    if violations:
        return {
            "allowed": False,
            "violations": violations
        }

    return {
        "allowed": True,
        "violations": []
    }