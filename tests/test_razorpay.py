from app.services.razorpay_service import (
    create_razorpay_order
)


order = create_razorpay_order(
    amount=100,
    transaction_id=
        "test_razorpay_001"
)


print(
    "\n===== RAZORPAY TEST ORDER ====="
)

print(order)