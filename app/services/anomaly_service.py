def calculate_anomaly_score(
    transaction,
    catalog_median_price,
    purchase_velocity=1,
    requested_category=None
):
    """
    Agent-specific transaction anomaly detection.

    Returns:
        anomaly_score: float between 0 and 1
        anomaly_reasons: list of detected anomalies
        signals: detailed scoring signals
    """

    score = 0.0
    reasons = []
    signals = {}

    # =====================================================
    # 1. PRICE ANOMALY
    # =====================================================

    if catalog_median_price and catalog_median_price > 0:

        price_ratio = transaction.amount / catalog_median_price

        signals["price_ratio"] = round(price_ratio, 3)

        # More than 2x catalog median
        if price_ratio >= 2.0:

            score += 0.35

            reasons.append(
                "Transaction price is significantly above the catalog median."
            )

        # Between 1.5x and 2x
        elif price_ratio >= 1.5:

            score += 0.20

            reasons.append(
                "Transaction price is moderately above the catalog median."
            )

        else:

            signals["price_anomaly"] = False

    else:

        signals["price_ratio"] = None


    # =====================================================
    # 2. INTENT / CATEGORY DRIFT
    # =====================================================

    if requested_category:

        transaction_category = (
            transaction.category or ""
        ).lower()

        requested_category = (
            requested_category or ""
        ).lower()

        if transaction_category != requested_category:

            score += 0.30

            reasons.append(
                "Transaction category does not match the user's requested intent."
            )

            signals["intent_drift"] = True

        else:

            signals["intent_drift"] = False

    else:

        signals["intent_drift"] = False


    # =====================================================
    # 3. PURCHASE VELOCITY
    # =====================================================

    signals["purchase_velocity"] = purchase_velocity

    if purchase_velocity >= 5:

        score += 0.25

        reasons.append(
            "Unusually high purchase velocity detected."
        )

    elif purchase_velocity >= 3:

        score += 0.15

        reasons.append(
            "Elevated purchase velocity detected."
        )


    # =====================================================
    # 4. HIGH VALUE TRANSACTION
    # =====================================================

    if transaction.amount >= 100000:

        score += 0.10

        reasons.append(
            "High-value agent initiated transaction detected."
        )


    # =====================================================
    # FINAL SCORE
    # =====================================================

    anomaly_score = min(score, 1.0)


    # =====================================================
    # SEVERITY
    # =====================================================

    if anomaly_score >= 0.70:

        severity = "CRITICAL"

    elif anomaly_score >= 0.45:

        severity = "HIGH"

    elif anomaly_score >= 0.20:

        severity = "MEDIUM"

    else:

        severity = "LOW"


    return {
        "anomaly_score": round(anomaly_score, 3),

        "severity": severity,

        "signals": signals,

        "reasons": reasons
    }