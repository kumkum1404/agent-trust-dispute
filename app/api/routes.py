from fastapi import APIRouter, HTTPException

from app.models.schemas import AgentMandate, Transaction

from app.services.risk_service import evaluate_transaction

from app.services.evidence_service import (
    generate_evidence_packet,
    save_evidence_packet
)

from app.services.razorpay_service import (
    create_razorpay_order
)

from app.services.catalog_service import (
    get_catalog_median_price
)


router = APIRouter()


# ============================================================
# IN-MEMORY REVIEW QUEUE
# ============================================================

review_queue = {}


# ============================================================
# EVALUATE TRANSACTION
# ============================================================

@router.post("/evaluate")
def evaluate(
    mandate: AgentMandate,
    transaction: Transaction
):

    # --------------------------------------------------------
    # 1. CATALOG INTELLIGENCE
    # --------------------------------------------------------

    catalog_median_price = get_catalog_median_price(
        product_name=transaction.product_name,
        category=transaction.category
    )

    # --------------------------------------------------------
    # 2. SCENARIO-BASED RISK INPUTS
    #
    # Frontend can send:
    #
    # Safe:
    # purchase_velocity = 1
    # agent_behavior_score = 0.05
    #
    # Suspicious:
    # purchase_velocity = 4
    # agent_behavior_score = 0.65
    #
    # Adversarial:
    # mandate violations handle the BLOCK
    # --------------------------------------------------------

    purchase_velocity = 1
    agent_behavior_score = 0.05

    # Read optional demo headers from transaction object
    # if they exist. Otherwise safe defaults are used.

    purchase_velocity = transaction.purchase_velocity
    agent_behavior_score = transaction.agent_behavior_score

    # --------------------------------------------------------
    # 3. SECURITY + ML RISK EVALUATION
    # --------------------------------------------------------

    result = evaluate_transaction(
        mandate=mandate,
        transaction=transaction,

        catalog_median_price=catalog_median_price,

        purchase_velocity=purchase_velocity,

        agent_behavior_score=agent_behavior_score
    )

    final_action = result["final_decision"]["action"]

    # --------------------------------------------------------
    # 4. GENERATE EVIDENCE
    # --------------------------------------------------------

    evidence = generate_evidence_packet(
        mandate=mandate,
        transaction=transaction,

        verification=result["mandate_verification"],

        risk_score=result["risk_analysis"]["risk_score"],

        risk_reasons=result["risk_analysis"]["risk_reasons"],

        action=final_action
    )

    evidence_path = save_evidence_packet(
        evidence
    )

    # --------------------------------------------------------
    # 5. PAYMENT GATE
    # --------------------------------------------------------

    razorpay_order = None

    payment_status = "BLOCKED_BEFORE_RAZORPAY"

    # --------------------------------------------------------
    # 6. ALLOW
    # --------------------------------------------------------

    if final_action == "ALLOW":

        razorpay_order = create_razorpay_order(
            amount=transaction.amount,
            transaction_id=transaction.transaction_id
        )

        payment_status = "RAZORPAY_ORDER_CREATED"

    # --------------------------------------------------------
    # 7. REVIEW
    # --------------------------------------------------------

    elif final_action == "REVIEW":

        review_queue[
            transaction.transaction_id
        ] = {

            "transaction_id":
                transaction.transaction_id,

            "agent_id":
                transaction.agent_id,

            "product_name":
                transaction.product_name,

            "category":
                transaction.category,

            "merchant_id":
                transaction.merchant_id,

            "amount":
                transaction.amount,

            "risk_score":
                result["risk_analysis"]["risk_score"],

            "risk_reasons":
                result["risk_analysis"]["risk_reasons"],

            "status":
                "PENDING_REVIEW",

            "mandate":
                mandate.model_dump(),

            "transaction":
                transaction.model_dump(),

            "evidence":
                evidence,

            "evidence_file":
                evidence_path
        }

        payment_status = "WAITING_FOR_HUMAN_REVIEW"

    # --------------------------------------------------------
    # 8. BLOCK
    # --------------------------------------------------------

    elif final_action == "BLOCK":

        payment_status = "BLOCKED_BY_TRUST_ENGINE"

    # --------------------------------------------------------
    # 9. RESPONSE
    # --------------------------------------------------------

    return {

        "transaction_id":
            transaction.transaction_id,

        "security_layer": {

            "mandate_verification":
                result["mandate_verification"],

            "risk_analysis":
                result["risk_analysis"],

            "final_decision":
                result["final_decision"]
        },

        "payment": {

            "status":
                payment_status,

            "razorpay_order":
                razorpay_order
        },

        "evidence": {

            "packet":
                evidence,

            "file":
                evidence_path
        }
    }


# ============================================================
# GET REVIEW QUEUE
# ============================================================

@router.get("/reviews")
def get_reviews():

    pending_reviews = [
        review
        for review in review_queue.values()
        if review["status"] == "PENDING_REVIEW"
    ]

    return {
        "count": len(pending_reviews),
        "reviews": pending_reviews
    }

# ============================================================
# GET SINGLE REVIEW
# ============================================================

@router.get("/reviews/{transaction_id}")
def get_review(
    transaction_id: str
):

    review = review_queue.get(
        transaction_id
    )

    if not review:

        raise HTTPException(
            status_code=404,
            detail="Review transaction not found"
        )

    return review


# ============================================================
# APPROVE REVIEW
# ============================================================

@router.post("/reviews/{transaction_id}/approve")
def approve_review(transaction_id: str):

    review = review_queue.get(transaction_id)

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review transaction not found"
        )

    if review["status"] != "PENDING_REVIEW":
        raise HTTPException(
            status_code=400,
            detail="Transaction has already been processed"
        )

    razorpay_order = create_razorpay_order(
        amount=review["amount"],
        transaction_id=review["transaction_id"]
    )

    review["status"] = "APPROVED"
    review["payment_status"] = "RAZORPAY_ORDER_CREATED"
    review["razorpay_order"] = razorpay_order

    return {
        "success": True,
        "message": "Transaction approved by human reviewer",
        "transaction_id": transaction_id,
        "status": "APPROVED",
        "payment": {
            "status": "RAZORPAY_ORDER_CREATED",
            "razorpay_order": razorpay_order
        }
    }

# ============================================================
# REJECT REVIEW
# ============================================================

@router.post("/reviews/{transaction_id}/reject")
def reject_review(transaction_id: str):

    review = review_queue.get(transaction_id)

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review transaction not found"
        )

    if review["status"] != "PENDING_REVIEW":
        raise HTTPException(
            status_code=400,
            detail="Transaction has already been processed"
        )

    review["status"] = "REJECTED"
    review["payment_status"] = "BLOCKED_AFTER_HUMAN_REVIEW"

    return {
        "success": True,
        "message": "Transaction rejected by human reviewer",
        "transaction_id": transaction_id,
        "status": "REJECTED",
        "payment": {
            "status": "BLOCKED_AFTER_HUMAN_REVIEW"
        }
    }