import os
import joblib


MODEL_PATH = "models/risk_model.joblib"


def load_model():

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Model not found. Run "
            "python ml/train_model.py"
        )

    return joblib.load(
        MODEL_PATH
    )


def predict_risk(
    price_deviation,
    velocity,
    behavior_score,
    intent_drift,
    mandate_violation
):

    model = load_model()

    features = [[
        price_deviation,
        velocity,
        behavior_score,
        intent_drift,
        mandate_violation
    ]]

    probability = model.predict_proba(
        features
    )[0][1]

    return {
        "risk_score": round(
            float(probability),
            4
        ),

        "risk_prediction":
            int(probability >= 0.50),

        "risk_level":
            (
                "HIGH"
                if probability >= 0.70
                else "MEDIUM"
                if probability >= 0.40
                else "LOW"
            )
    }