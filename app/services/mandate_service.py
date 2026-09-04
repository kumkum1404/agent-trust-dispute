from datetime import datetime, timezone


def verify_mandate(mandate, transaction):

    violations = []

    # Agent identity
    if mandate.agent_id != transaction.agent_id:
        violations.append(
            "Agent identity does not match mandate"
        )

    # Spending limit
    if transaction.amount > mandate.max_spending:
        violations.append(
            f"Spending limit exceeded: "
            f"₹{transaction.amount:.2f} > "
            f"₹{mandate.max_spending:.2f}"
        )

    # Category
    if mandate.allowed_categories:

        categories = [
            x.lower()
            for x in mandate.allowed_categories
        ]

        if transaction.category.lower() not in categories:
            violations.append(
                f"Category '{transaction.category}' "
                "is not allowed"
            )

    # Merchant
    if mandate.allowed_merchants:

        if transaction.merchant_id not in mandate.allowed_merchants:
            violations.append(
                f"Merchant '{transaction.merchant_id}' "
                "is not allowed"
            )

    # Expiry check
    expires_at = mandate.expires_at

    if expires_at is not None:

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(timezone.utc)

        if now > expires_at:
            violations.append(
                "Agent mandate has expired"
            )

    return {
        "valid": len(violations) == 0,
        "violations": violations
    }