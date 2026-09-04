import os
import joblib
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report
)


np.random.seed(42)


def generate_dataset(n=5000):

    X = []
    y = []

    for _ in range(n):

        price_deviation = np.random.uniform(0, 1)

        velocity = np.random.randint(1, 15)

        behavior_score = np.random.uniform(0, 1)

        intent_drift = np.random.uniform(0, 1)

        mandate_violation = np.random.randint(0, 2)

        risk = (
            price_deviation * 0.25
            + min(velocity / 10, 1) * 0.20
            + behavior_score * 0.20
            + intent_drift * 0.20
            + mandate_violation * 0.30
        )

        label = int(risk >= 0.45)

        X.append([
            price_deviation,
            velocity,
            behavior_score,
            intent_drift,
            mandate_violation
        ])

        y.append(label)

    return np.array(X), np.array(y)


def train():

    X, y = generate_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    print("\n===== MODEL PERFORMANCE =====")

    print(
        "Accuracy:",
        round(
            accuracy_score(
                y_test,
                predictions
            ),
            4
        )
    )

    print(
        "Precision:",
        round(
            precision_score(
                y_test,
                predictions
            ),
            4
        )
    )

    print(
        "Recall:",
        round(
            recall_score(
                y_test,
                predictions
            ),
            4
        )
    )

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        model,
        "models/risk_model.joblib"
    )

    print(
        "\nSaved: models/risk_model.joblib"
    )


if __name__ == "__main__":
    train()