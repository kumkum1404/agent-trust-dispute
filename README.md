Agent Trust & Dispute
Overview

Agent Trust & Dispute is a security-focused transaction evaluation system designed to determine whether an AI agent's transaction should be Allowed, Sent for Human Review, or Blocked.

The system evaluates a transaction against the user's predefined agent mandate, analyzes transaction risk using multiple behavioral and financial signals, and creates a structured evidence packet for every evaluated transaction.

The payment flow is protected by placing the trust evaluation before Razorpay order creation:

Transaction
     ↓
Mandate Verification
     ↓
Catalog Price Analysis
     ↓
Intent & Behavioral Analysis
     ↓
ML Risk Prediction
     ↓
Final Decision
     ↓
 ┌──────────┬───────────┬─────────┐
 │  ALLOW   │   REVIEW  │  BLOCK  │
 └────┬─────┴─────┬─────┴────┬────┘
      ↓           ↓          ↓
 Razorpay     Human Review   Stop
   Order          ↓
 Creation     Approve/Reject

The project focuses on preventing unauthorized or suspicious transactions initiated by autonomous or AI-powered agents.

Key Features
1. Agent Mandate Verification

Every transaction is checked against the agent's authorized mandate.

The mandate contains:

Maximum spending limit
Allowed transaction categories
Allowed merchants
Expiration information
User and agent association

For example:

{
    "max_spending": 50000,
    "allowed_categories": [
        "electronics",
        "software",
        "books"
    ],
    "allowed_merchants": [
        "merchant_demo_001"
    ]
}

If a transaction violates mandatory authorization constraints, the transaction is BLOCKED.

2. Transaction Risk Analysis

The system evaluates multiple risk signals:

Price deviation from catalog median price
Purchase velocity
Agent behavior score
Intent drift
Mandate violation

These signals are passed to the ML risk prediction layer.

3. ML-Based Risk Scoring

The project uses an ML-based predict_risk() function to generate a risk score.

The risk evaluation receives:

price_deviation
purchase_velocity
agent_behavior_score
intent_drift
mandate_violation

The resulting risk score is combined with rule-based security checks to determine the final transaction decision.

4. Intent Drift Detection

The system checks whether the actual transaction matches the user's requested intent.

For example:

Requested Category → Books
Actual Category    → Electronics

This is identified as intent drift.

The same mechanism checks whether the transaction amount exceeds a requested maximum price.

5. Catalog Price Intelligence

The transaction amount is compared with the catalog median price for the product/category.

The system calculates:

Price Deviation =
(Transaction Amount - Catalog Median Price)
--------------------------------------------
          Catalog Median Price

A significant price deviation becomes a risk signal.

6. Three-Level Decision System

The trust engine produces three possible decisions:

Decision	Meaning
ALLOW	Transaction passed the trust controls
REVIEW	Transaction requires human verification
BLOCK	Transaction violated mandatory authorization controls

The current decision logic prioritizes mandate violations:

Invalid Mandate
      ↓
    BLOCK

Valid Mandate + Suspicious Signals
      ↓
    REVIEW

Valid Mandate + Low Risk
      ↓
    ALLOW
Human Review Workflow

Transactions classified as REVIEW are placed into an in-memory review queue.

The reviewer can:

REVIEW
  │
  ├── APPROVE
  │      ↓
  │   Razorpay Order Created
  │
  └── REJECT
         ↓
       Payment Blocked

This ensures that a suspicious transaction does not directly proceed to payment.

Payment Security Gate

Razorpay order creation occurs only after the trust decision.

ALLOW
Trust Evaluation
      ↓
    ALLOW
      ↓
Razorpay Order
   Created
REVIEW
Trust Evaluation
      ↓
    REVIEW
      ↓
Human Approval
      ↓
Razorpay Order
   Created
BLOCK
Trust Evaluation
      ↓
    BLOCK
      ↓
No Razorpay Order

This makes the trust engine a security layer before payment execution.

Evidence Generation

For every evaluated transaction, the system generates an evidence packet.

The evidence contains:

Evidence ID
Generation timestamp
Agent information
Mandate information
Transaction information
Mandate verification result
Risk score
Risk reasons
Final decision

Example structure:

{
    "evidence_id": "EVD-txn_...",
    "generated_at": "...",

    "agent": {
        "agent_id": "agent_demo_001"
    },

    "mandate": {
        "max_spending": 50000,
        "allowed_categories": [
            "electronics",
            "software",
            "books"
        ]
    },

    "transaction": {
        "transaction_id": "txn_...",
        "product_name": "Laptop",
        "category": "electronics",
        "amount": 42000
    },

    "risk_analysis": {
        "risk_score": 0.02,
        "risk_reasons": []
    },

    "decision": {
        "action": "ALLOW"
    }
}

Evidence files are stored in:

evidence/

with the format:

EVD-{transaction_id}.json
Implemented Transaction Scenarios

The system currently supports the following demonstrated scenarios.

Safe Transaction

Example:

Product: Laptop
Amount: ₹42,000
Allowed Category: Electronics
Maximum Spending: ₹50,000
Merchant: Allowed
Risk Score: 0.02
Decision: ALLOW

The transaction passes the trust controls and proceeds to Razorpay order creation.

Suspicious Transaction

Example:

Product: Laptop
Amount: ₹47,000
Maximum Spending: ₹50,000
Category: Electronics
Risk Signal: High Purchase Velocity
Decision: REVIEW

The transaction is placed into the human review queue.

The reviewer can either approve or reject it.

Adversarial / Unauthorized Transaction

Example:

Product: Laptop
Amount: ₹42,000
Maximum Spending: ₹20,000
Allowed Category: Books
Actual Category: Electronics

The transaction violates:

Spending Limit
Category Restriction

Therefore:

Decision: BLOCK

No Razorpay order is created.

System Architecture
                    ┌──────────────────────┐
                    │      Frontend        │
                    │ Transaction / Review │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI API     │
                    │      routes.py       │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Mandate Service  │        │ Catalog Service  │
       │ Authorization    │        │ Median Price     │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌──────────────────────┐
                    │    Risk Service      │
                    │                      │
                    │ Intent Drift         │
                    │ Price Deviation      │
                    │ Behavior Signals     │
                    │ Mandate Violation    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     ML Predictor     │
                    │    predict_risk()    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Decision Engine    │
                    │                      │
                    │ ALLOW / REVIEW /     │
                    │ BLOCK                │
                    └───────┬───────┬──────┘
                            │       │
                 ┌──────────┘       └──────────┐
                 ▼                             ▼
       ┌──────────────────┐          ┌──────────────────┐
       │ Razorpay Service │          │ Evidence Service │
       │ Payment Gate     │          │ JSON Evidence    │
       └──────────────────┘          └──────────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Human Review Queue│
                  │ Approve / Reject  │
                  └───────────────────┘
Project Structure
agent-trust-dispute/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── mandate_service.py
│   │   ├── risk_service.py
│   │   ├── evidence_service.py
│   │   ├── catalog_service.py
│   │   └── razorpay_service.py
│   │
│   └── main.py
│
├── ml/
│   └── predict.py
│
├── evidence/
│   └── EVD-*.json
│
├── requirements.txt
│
└── README.md
Tech Stack
Backend
Python
FastAPI
Uvicorn
Pydantic
Machine Learning
ML-based risk prediction
Risk scoring
Behavioral and transaction risk signals
Payment
Razorpay
Data & Evidence
JSON
In-memory review queue
File-based evidence storage
Development
Git
GitHub
VS Code / GitHub Codespaces
API Endpoints
Evaluate Transaction
POST /api/evaluate

Evaluates a transaction against the supplied agent mandate and returns:

Mandate verification
Risk analysis
Final decision
Payment status
Evidence packet
Get Review Queue
GET /api/reviews

Returns transactions currently waiting for human review.

Get Single Review
GET /api/reviews/{transaction_id}

Returns the details of a specific review transaction.

Approve Review
POST /api/reviews/{transaction_id}/approve

Approves a pending transaction and creates the Razorpay order.

Reject Review
POST /api/reviews/{transaction_id}/reject

Rejects the transaction and prevents payment.

Screenshots

Screenshots README me add karna important hai, especially because this is a hackathon/project submission.

I recommend adding these screenshots in this exact order:

1. Main Dashboard

Put your screenshot here showing the main application interface.

## Application Dashboard

![Application Dashboard](screenshots/dashboard.png)
2. ALLOW Result

Show the successful transaction evaluation.

## Transaction Evaluation - ALLOW

![Allow Transaction](screenshots/allow.png)

Your current example with:

Risk Score: 0.02
Decision: ALLOW

is perfect for this screenshot.

3. REVIEW Result

Show the suspicious transaction.

## Transaction Evaluation - REVIEW

![Review Transaction](screenshots/review.png)

Use the screen where:

Decision: REVIEW

and the review option is visible.

4. Human Review

This is particularly important because it demonstrates the actual workflow.

## Human Review

![Human Review](screenshots/human-review.png)

Show the Approve and Reject options.

5. BLOCK Result

Show the adversarial transaction.

## Transaction Evaluation - BLOCK

![Blocked Transaction](screenshots/block.png)

Your current evidence showing:

Spending limit exceeded
Category 'electronics' is not allowed
Decision: BLOCK

is ideal.

6. Evidence Packet

Show the generated JSON evidence.

## Evidence Packet

![Evidence Packet](screenshots/evidence.png)

This demonstrates that every evaluation produces auditable evidence.

Evidence-Based Decision Flow

The complete implemented flow is:

              Transaction
                   │
                   ▼
          Mandate Verification
                   │
          ┌────────┴────────┐
          │                 │
        Invalid            Valid
          │                 │
          ▼                 ▼
        BLOCK         Risk Evaluation
                            │
                            ▼
                    ML Risk Prediction
                            │
                            ▼
                    Decision Engine
                       /    |    \
                      /     |     \
                     ▼      ▼      ▼
                  ALLOW   REVIEW  BLOCK
                    │       │
                    │       ▼
                    │   Human Review
                    │      /   \
                    │     ▼     ▼
                    │ APPROVE REJECT
                    │    │       │
                    └────┤       │
                         ▼       ▼
                  Razorpay   Payment
                    Order    Blocked
Security & Trust Controls

The system combines rule-based authorization and ML-based risk analysis.

Rule-Based Controls
Spending limit validation
Category authorization
Merchant authorization
Intent constraints
Transaction restrictions
Risk-Based Controls
Price deviation
Purchase velocity
Agent behavior score
Intent drift
ML risk score

This combination prevents the system from relying only on an ML prediction for authorization.

Current Payment Protection

The important security property of the implementation is:

Transaction
     ↓
Trust Evaluation
     ↓
Decision
     ↓
Payment

rather than:

Transaction
     ↓
Payment
     ↓
Trust Evaluation

For BLOCK, Razorpay order creation does not occur.

For REVIEW, Razorpay order creation occurs only after human approval.

Running the Project Locally

Clone the repository:

git clone <your-repository-url>
cd agent-trust-dispute

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn app.main:app --reload

The application runs on:

http://127.0.0.1:8000

FastAPI API documentation is available through:

/docs
Example Decision Summary
Scenario	Mandate	Risk Signals	Decision	Payment
Safe Laptop Purchase	Valid	Low	ALLOW	Razorpay Order
Suspicious Laptop Purchase	Valid	High Purchase Velocity	REVIEW	Human Approval Required
Unauthorized Laptop Purchase	Invalid	Spending + Category Violation	BLOCK	Blocked
Project Highlights
Agent mandate-based authorization
ML-assisted transaction risk scoring
Intent drift detection
Catalog price deviation analysis
Behavioral risk signals
Three-level decision system: ALLOW / REVIEW / BLOCK
Human-in-the-loop review workflow
Razorpay payment gate
Evidence packet generation
Persistent JSON evidence files
Review approval and rejection APIs
FastAPI backend architecture
Conclusion

Agent Trust & Dispute provides a transaction-level trust layer for autonomous agents.

Instead of allowing an AI agent to directly execute a payment, the system first verifies whether the transaction is authorized, evaluates its risk, generates evidence, and then determines whether it should be:

ALLOWED
   ↓
REVIEWED BY A HUMAN
   ↓
or BLOCKED

This creates a controlled transaction flow where authorization, risk assessment, human oversight, evidence generation, and payment execution are connected in a single system.

Screenshots folder

README ke saath repository me ye folder bana dena:

screenshots/
├── dashboard.png
├── allow.png
├── review.png
├── human-review.png
├── block.png
└── evidence.png