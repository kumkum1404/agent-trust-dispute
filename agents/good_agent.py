import requests


API_URL = (
    "http://127.0.0.1:8000/api/evaluate"
)


payload = {

    "mandate": {

        "agent_id":
            "agent_good_01",

        "max_spending":
            50000,

        "allowed_categories": [
            "laptop"
        ],

        "allowed_merchants": [
            "merchant_001",
            "merchant_002"
        ],

        "expires_at":
            "2026-12-31T23:59:59"
    },

    "transaction": {

        "transaction_id":
            "txn_good_agent_001",

        "agent_id":
            "agent_good_01",

        "product_name":
            "HP Laptop",

        "category":
            "laptop",

        "merchant_id":
            "merchant_001",

        "amount":
            42000,

        "timestamp":
            "2026-09-03T10:00:00",

        "user_intent":
            "Buy an HP laptop under 50000",

        "requested_category":
            "laptop",

        "requested_max_price":
            50000
    }
}


response = requests.post(
    API_URL,
    json=payload
)


print(
    response.status_code
)

print(
    response.json()
)