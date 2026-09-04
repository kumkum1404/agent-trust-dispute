# AgentTrust Dispute

## AI-Powered Agent Trust & Transaction Dispute System

AgentTrust Dispute is a security-focused transaction evaluation system designed to verify whether an AI agent is authorized to perform a purchase on behalf of a user.

The system combines **mandate verification, risk analysis, behavioral signals, catalog price intelligence, human review, evidence generation, and payment gating** to prevent unauthorized or suspicious transactions.

---

## Problem Statement

As AI agents increasingly perform actions such as purchasing products and making payments on behalf of users, there is a need for a reliable trust layer between the agent and the payment system.

An agent may:

- Exceed the user's spending limit
- Purchase products outside the permitted category
- Use an unauthorized merchant
- Make unusually frequent purchases
- Behave differently from its expected pattern
- Attempt transactions that conflict with user intent

AgentTrust Dispute evaluates these conditions before allowing a payment to proceed.

---

## Key Features

### 1. Agent Mandate Verification

Every transaction is checked against the user's predefined mandate.

The mandate contains:

- Maximum spending limit
- Allowed product categories
- Allowed merchants
- Mandate expiry
- Agent and user identification

Invalid mandates can immediately block a transaction.

---

### 2. Risk Analysis

The system calculates transaction risk using multiple signals:

- Price deviation from catalog median
- Purchase velocity
- Agent behavior score
- Intent drift
- Mandate violations

A risk score is generated for every evaluated transaction.

---

### 3. Three-Level Decision System

Transactions are classified into three outcomes:

| Decision | Meaning |
|----------|---------|
| `ALLOW` | Transaction passed trust controls |
| `REVIEW` | Transaction requires human verification |
| `BLOCK` | Transaction violates mandatory authorization rules |

---

### 4. Human Review Queue

Suspicious transactions are added to a review queue.

A human reviewer can:

- Approve the transaction
- Reject the transaction

A Razorpay order is created only after approval.

---

### 5. Payment Gating

The system prevents unauthorized transactions from reaching the payment layer.

Payment flow:

```text
Transaction
     ↓
Mandate Verification
     ↓
Risk Analysis
     ↓
Decision
  ↙    ↓     ↘
BLOCK REVIEW  ALLOW
        ↓       ↓
     Human    Razorpay
     Review    Order

```
### 6. Evidence Generation

Every evaluated transaction generates an evidence packet containing:

- Transaction details
- Agent information
- Mandate information
- Mandate verification result
- Risk score
- Risk reasons
- Final decision
- Generation timestamp

Evidence packets are stored as JSON files for auditability and dispute investigation.

Example:
```text
evidence/
├── EVD-txn_....json
├── EVD-txn_suspicious_....json
└── EVD-txn_adversarial_....json
```

---


##  System Architecture
```text
                    ┌──────────────────┐
                    │     Frontend     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   FastAPI API    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌─────────────┐ ┌─────────────┐
       │   Mandate  │ │ Risk Engine │ │   Catalog   │
       │ Verification│ │ + ML Model  │ │ Intelligence│
       └──────┬─────┘ └──────┬──────┘ └─────────────┘
              │              │
              └──────┬───────┘
                     ▼
              ┌───────────────┐
              │ Decision Layer│
              └───────┬───────┘
                      │
            ┌─────────┼─────────┐
            ▼         ▼         ▼
         BLOCK      REVIEW     ALLOW
                     │           │
                     ▼           ▼
               Human Review   Razorpay
                     │
                     ▼
               Approve/Reject

                     +
                     │
                     ▼
              Evidence Packet

```

---


##  Technology Stack
- Backend:Python, FastAPI, Uvicorn
- Machine Learning: Scikit-learn
- Risk Engine: Rule-based risk evaluation + ML risk scoring
- Data Validation: Pydantic
- Payment Gateway: Razorpay API
- Frontend: HTML, CSS, JavaScript
- Evidence & Audit: JSON-based evidence packets
- API Testing: Swagger / OpenAPI
- Development: Git, GitHub, GitHub Codespaces
---

## Installation

Clone Repository

```bash
git clone https://github.com/kumkum1404/agent-trust-dispute.git
```

Go inside the project folder

```bash
cd agent-trust-dispute
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run project

```bash
uvicorn app.main:app --reload
```

---

## Future Enhancements

- Real-time Agent Behavior Monitoring using historical transaction patterns
- Advanced ML/Deep Learning Risk Models for improved fraud and anomaly detection
- Real-time Product Price APIs instead of static catalog data
- Persistent Database for transactions, mandates, reviews, and evidence
- Blockchain-based Evidence Storage for tamper-resistant audit trails
- Automated Dispute Resolution with AI-assisted investigation
- Multi-Agent Trust Management for organizations using multiple AI agents
- Real-time Notifications through email/SMS when suspicious transactions require approval
- Production-grade Authentication & RBAC for users, agents, and reviewers
- Cloud Deployment & Monitoring for scalable production usage
---

## Developer

**Kumkum Manjhi**

Final Year B.Tech CSE Student

⭐ If you like this project, don't forget to star the repository.
