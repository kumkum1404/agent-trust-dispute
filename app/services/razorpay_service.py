import os
import razorpay

from dotenv import load_dotenv


load_dotenv()


KEY_ID = os.getenv(
    "RAZORPAY_KEY_ID"
)

KEY_SECRET = os.getenv(
    "RAZORPAY_KEY_SECRET"
)


client = razorpay.Client(
    auth=(
        KEY_ID,
        KEY_SECRET
    )
)


def create_razorpay_order(
    amount,
    transaction_id
):

    order_data = {

        "amount":
            int(amount * 100),

        "currency":
            "INR",

        "receipt":
            transaction_id,

        "notes": {

            "source":
                "agent_trust_dispute",

            "transaction_id":
                transaction_id
        }
    }

    return client.order.create(
        data=order_data
    )