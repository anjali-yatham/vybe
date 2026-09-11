import os
from pathlib import Path

import joblib
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from agents.decision_agent import explain_flagged_transaction
from agents.investigation_agent import investigate_transaction
from agents.profiler_agent import get_user_trust_profile
from database.init_db import ResaleTransaction

# Load environment variables from .env
BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")

# Get database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from backend/.env")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Load the trained fraud detection model and scaler
ML_DIR = BACKEND_DIR / "ml"
fraud_model = joblib.load(ML_DIR / "fraud_model.pkl")
scaler = joblib.load(ML_DIR / "scaler.pkl")

# Feature columns used by the ML model (must match training order)
ML_FEATURE_COLUMNS = [
    "price_markup_ratio",
    "seller_account_age_days",
    "buyer_account_age_days",
    "hours_since_ticket_purchase",
    "seller_tickets_last_hour",
    "payment_reuse_count",
    "is_duplicate_ticket_attempt",
]


def evaluate_transaction(transaction: dict) -> dict:
    """
    Run the full fraud detection pipeline on a transaction.
    
    Args:
        transaction: Dictionary containing transaction details with keys:
                    transaction_id, seller_id, buyer_id, ticket_id,
                    price_markup_ratio, seller_account_age_days, 
                    buyer_account_age_days, hours_since_ticket_purchase,
                    seller_tickets_last_hour, payment_reuse_count,
                    is_duplicate_ticket_attempt
    
    Returns:
        Dictionary containing pipeline results:
        - transaction_id: The transaction ID
        - status: "allowed" or "flagged_for_review"
        - trust_profile: Seller trust profile from profiler agent
        - investigation_findings: Investigation results (None if allowed)
        - explanation: Plain English explanation (None if allowed)
    """
    print("=" * 80)
    print(f"EVALUATING TRANSACTION: {transaction['transaction_id']}")
    print("=" * 80)
    
    # ========== STEP 1: Profiler Agent ==========
    print("\n[STEP 1] Running Profiler Agent...")
    trust_profile = get_user_trust_profile(transaction["seller_id"])
    print(f"  Seller Trust Score: {trust_profile['trust_score']}")
    print(f"  Verified Fan: {trust_profile['verified_fan']}")
    print(f"  Total Resales: {trust_profile['total_resales']}")
    print(f"  Historical Fraud Rate: {trust_profile['fraud_rate'] * 100:.2f}%")
    
    # ========== STEP 2: Anomaly Detection ==========
    print("\n[STEP 2] Running Anomaly Detection (IsolationForest)...")
    
    # Extract and scale the 7 ML features
    feature_values = [transaction[col] for col in ML_FEATURE_COLUMNS]
    feature_array = np.array(feature_values).reshape(1, -1)
    scaled_features = scaler.transform(feature_array)
    
    # Run prediction
    prediction = fraud_model.predict(scaled_features)[0]
    # Convert IsolationForest output: -1 (outlier) -> 1 (flagged), 1 (inlier) -> 0 (not flagged)
    is_flagged = 1 if prediction == -1 else 0
    
    print(f"  Model Prediction: {'FLAGGED' if is_flagged else 'NOT FLAGGED'}")
    
    # ========== STEP 3: Decision Point ==========
    print("\n[STEP 3] Decision Point...")
    
    if not is_flagged:
        print("  ✓ ALLOWED AUTOMATICALLY")
        return {
            "transaction_id": transaction["transaction_id"],
            "status": "allowed",
            "trust_profile": trust_profile,
            "investigation_findings": None,
            "explanation": None,
        }
    
    print("  ⚠ FLAGGED - Proceeding to investigation...")
    
    # ========== STEP 4: Investigation Agent ==========
    print("\n[STEP 4] Running Investigation Agent...")
    investigation_findings = investigate_transaction(
        transaction["seller_id"],
        transaction["ticket_id"]
    )
    print(f"  Duplicate Ticket Found: {investigation_findings['duplicate_ticket_found']}")
    print(f"  Tickets Sold Last 24h: {investigation_findings['tickets_sold_last_24h']}")
    print(f"  Seller Historical Fraud Rate: {investigation_findings['seller_historical_fraud_rate'] * 100:.2f}%")
    print(f"  Repeat Buyer-Seller Pair: {investigation_findings['repeat_buyer_seller_pair']}")
    
    # ========== STEP 5: Decision & Explanation Agent ==========
    print("\n[STEP 5] Running Decision & Explanation Agent...")
    
    # Build feature dictionary for explanation
    feature_dict = {col: transaction[col] for col in ML_FEATURE_COLUMNS}
    explanation = explain_flagged_transaction(feature_dict)
    print(f"  Explanation: {explanation}")
    
    # ========== STEP 6: Return Final Result ==========
    print("\n[STEP 6] Generating Final Result...")
    print("  Status: FLAGGED FOR REVIEW")
    
    return {
        "transaction_id": transaction["transaction_id"],
        "status": "flagged_for_review",
        "trust_profile": trust_profile,
        "investigation_findings": investigation_findings,
        "explanation": explanation,
    }


if __name__ == "__main__":
    print("FRAUD DETECTION PIPELINE TEST")
    print("=" * 80)
    
    with Session(engine) as session:
        # Pick one flagged transaction (is_fraud=1)
        print("\nFetching a FLAGGED transaction from database...")
        flagged_stmt = select(ResaleTransaction).where(
            ResaleTransaction.is_fraud == True
        ).limit(1)
        flagged_txn = session.execute(flagged_stmt).scalar_one_or_none()
        
        # Pick one legit transaction (is_fraud=0)
        print("Fetching a LEGIT transaction from database...")
        legit_stmt = select(ResaleTransaction).where(
            ResaleTransaction.is_fraud == False
        ).limit(1)
        legit_txn = session.execute(legit_stmt).scalar_one_or_none()
        
        if not flagged_txn or not legit_txn:
            print("Error: Could not find both flagged and legit transactions.")
            exit(1)
        
        # Prepare transaction dictionaries
        flagged_dict = {
            "transaction_id": flagged_txn.transaction_id,
            "seller_id": flagged_txn.seller_id,
            "buyer_id": flagged_txn.buyer_id,
            "ticket_id": flagged_txn.ticket_id,
            "price_markup_ratio": float(flagged_txn.price_markup_ratio),
            "seller_account_age_days": float(flagged_txn.seller_account_age_days),
            "buyer_account_age_days": float(flagged_txn.buyer_account_age_days),
            "hours_since_ticket_purchase": float(flagged_txn.hours_since_ticket_purchase),
            "seller_tickets_last_hour": flagged_txn.seller_tickets_last_hour,
            "payment_reuse_count": flagged_txn.payment_reuse_count,
            "is_duplicate_ticket_attempt": int(flagged_txn.is_duplicate_ticket_attempt),
        }
        
        legit_dict = {
            "transaction_id": legit_txn.transaction_id,
            "seller_id": legit_txn.seller_id,
            "buyer_id": legit_txn.buyer_id,
            "ticket_id": legit_txn.ticket_id,
            "price_markup_ratio": float(legit_txn.price_markup_ratio),
            "seller_account_age_days": float(legit_txn.seller_account_age_days),
            "buyer_account_age_days": float(legit_txn.buyer_account_age_days),
            "hours_since_ticket_purchase": float(legit_txn.hours_since_ticket_purchase),
            "seller_tickets_last_hour": legit_txn.seller_tickets_last_hour,
            "payment_reuse_count": legit_txn.payment_reuse_count,
            "is_duplicate_ticket_attempt": int(legit_txn.is_duplicate_ticket_attempt),
        }
    
    # Test 1: Evaluate flagged transaction
    print("\n\n")
    print("█" * 80)
    print("TEST 1: EVALUATING KNOWN FLAGGED TRANSACTION")
    print("█" * 80)
    result1 = evaluate_transaction(flagged_dict)
    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print(f"  Status: {result1['status']}")
    print("=" * 80)
    
    # Test 2: Evaluate legit transaction
    print("\n\n")
    print("█" * 80)
    print("TEST 2: EVALUATING KNOWN LEGIT TRANSACTION")
    print("█" * 80)
    result2 = evaluate_transaction(legit_dict)
    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print(f"  Status: {result2['status']}")
    print("=" * 80)
    
    print("\n\nPIPELINE TEST COMPLETE!")
