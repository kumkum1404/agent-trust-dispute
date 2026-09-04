from app.services.mandate_service import verify_mandate
from ml.predict import predict_risk


def evaluate_transaction(
    mandate,
    transaction,
    catalog_median_price,
    purchase_velocity,
    agent_behavior_score
):

    # ============================================================
    # 1. MANDATE VERIFICATION
    # ============================================================

    mandate_result = verify_mandate(
        mandate,
        transaction
    )

    # ============================================================
    # 2. PRICE DEVIATION
    # ============================================================

    if catalog_median_price and catalog_median_price > 0:

        price_deviation = max(
            0,
            (
                transaction.amount - catalog_median_price
            ) / catalog_median_price
        )

    else:
        price_deviation = 0.0

    # ============================================================
    # 3. INTENT DRIFT
    # ============================================================

    intent_drift = 0.0

    if transaction.requested_category:

        if (
            transaction.category.lower()
            != transaction.requested_category.lower()
        ):
            intent_drift = 1.0

    if transaction.requested_max_price is not None:

        if (
            transaction.amount
            > transaction.requested_max_price
        ):
            intent_drift = 1.0

    # ============================================================
    # 4. MANDATE VIOLATION
    # ============================================================

    mandate_violation = (
        0
        if mandate_result["valid"]
        else 1
    )

    # ============================================================
    # 5. ML RISK
    # ============================================================

    risk_result = predict_risk(
        price_deviation,
        purchase_velocity,
        agent_behavior_score,
        intent_drift,
        mandate_violation
    )

    risk_score = float(
        risk_result["risk_score"]
    )

    # ============================================================
    # 6. RISK SIGNALS
    # ============================================================

    reasons = []

    if mandate_result.get("violations"):

        reasons.extend(
            mandate_result["violations"]
        )

    if price_deviation > 0.20:

        reasons.append(
            f"Price is "
            f"{price_deviation * 100:.1f}% "
            "above catalog median"
        )

    if purchase_velocity >= 5:

        reasons.append(
            "Unusually high purchase velocity"
        )

    if intent_drift == 1.0:

        reasons.append(
            "Transaction deviates from user intent"
        )

    if agent_behavior_score >= 0.80:

        reasons.append(
            "Agent behavior score is unusually high"
        )

    # ============================================================
    # 7. FINAL DECISION
    #
    # IMPORTANT:
    #
    # Invalid mandate = BLOCK
    #
    # Valid mandate + suspicious behaviour = REVIEW
    #
    # Clean transaction = ALLOW
    #
    # This prevents a suspicious demo transaction from
    # immediately becoming BLOCK just because ML gives
    # a high score.
    # ============================================================

    if not mandate_result["valid"]:

        action = "BLOCK"

        reason = (
            "Mandatory agent authorization "
            "constraint violated"
        )

    elif (
        risk_score >= 0.40
        or price_deviation > 0.20
        or purchase_velocity >= 5
        or agent_behavior_score >= 0.80
        or intent_drift == 1.0
    ):

        action = "REVIEW"

        reason = (
            "Transaction requires additional "
            "human review"
        )

    else:

        action = "ALLOW"

        reason = (
            "Transaction passed trust controls"
        )

    # ============================================================
    # 8. RETURN RESULT
    # ============================================================

    return {

        "mandate_verification":
            mandate_result,

        "risk_analysis": {

            **risk_result,

            "catalog_median_price":
                catalog_median_price,

            "price_deviation":
                round(
                    price_deviation,
                    4
                ),

            "purchase_velocity":
                purchase_velocity,

            "agent_behavior_score":
                agent_behavior_score,

            "intent_drift":
                intent_drift,

            "risk_reasons":
                reasons
        },

        "final_decision": {

            "action":
                action,

            "reason":
                reason
        }
    }