from app.models.schemas import UserIntent, Transaction


def normalize(value: str | None) -> str:
    if not value:
        return ""

    return value.strip().lower()


def evaluate_user_intent(
    intent: UserIntent,
    transaction: Transaction
):

    violations = []
    checks = {}

    # =====================================================
    # 1. CATEGORY CHECK
    # =====================================================

    if intent.allowed_category:

        category_match = (
            normalize(transaction.category)
            == normalize(intent.allowed_category)
        )

        checks["category_match"] = category_match

        if not category_match:
            violations.append(
                "Transaction category does not match "
                "the user's authorized category."
            )

    # =====================================================
    # 2. PRODUCT CHECK
    # =====================================================

    if intent.allowed_product:

        product_match = (
            normalize(transaction.product_name)
            == normalize(intent.allowed_product)
        )

        checks["product_match"] = product_match

        if not product_match:
            violations.append(
                "Purchased product does not match "
                "the product authorized by the user."
            )

    # =====================================================
    # 3. MERCHANT CHECK
    # =====================================================

    if intent.allowed_merchant:

        merchant_match = (
            normalize(transaction.merchant_id)
            == normalize(intent.allowed_merchant)
        )

        checks["merchant_match"] = merchant_match

        if not merchant_match:
            violations.append(
                "Merchant is different from the merchant "
                "authorized by the user."
            )

    # =====================================================
    # 4. BUDGET CHECK
    # =====================================================

    if intent.max_budget is not None:

        budget_match = (
            transaction.amount
            <= intent.max_budget
        )

        checks["budget_match"] = budget_match

        if not budget_match:
            violations.append(
                "Transaction amount exceeds "
                "the user's authorized budget."
            )

    # =====================================================
    # 5. FINAL INTENT DECISION
    # =====================================================

    intent_match = len(violations) == 0

    return {

        "intent_match": intent_match,

        "checks": checks,

        "violations": violations,

        "violation_count":
            len(violations),

        "user_request":
            intent.request,

        "decision":
            "PASS"
            if intent_match
            else "VIOLATION"

    }