import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

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


def investigate_transaction(seller_id: str, ticket_id: str) -> dict:
    """
    Perform a deep investigation on a flagged transaction to gather context.
    
    Args:
        seller_id: The seller's user ID
        ticket_id: The ticket ID being investigated
    
    Returns:
        Dictionary containing investigation findings:
        - duplicate_ticket_found: Whether this ticket appears multiple times
        - tickets_sold_last_24h: Number of tickets this seller sold in last 24 hours
        - seller_historical_fraud_rate: The seller's historical fraud rate
        - repeat_buyer_seller_pair: Whether this buyer-seller pair has transacted before
    """
    with Session(engine) as session:
        # Get the transaction being investigated to find buyer_id and timestamp
        transaction_stmt = select(ResaleTransaction).where(
            ResaleTransaction.seller_id == seller_id,
            ResaleTransaction.ticket_id == ticket_id
        )
        transaction = session.execute(transaction_stmt).scalar_one_or_none()
        
        if not transaction:
            raise ValueError(f"Transaction not found for seller '{seller_id}' and ticket '{ticket_id}'")
        
        buyer_id = transaction.buyer_id
        transaction_timestamp = transaction.timestamp
        
        # 1. Check if this ticket_id appears more than once (duplicate ticket fraud)
        duplicate_count_stmt = select(func.count()).where(
            ResaleTransaction.ticket_id == ticket_id
        )
        duplicate_count = session.execute(duplicate_count_stmt).scalar()
        duplicate_ticket_found = duplicate_count > 1
        
        # 2. Check how many tickets this seller sold in the last 24 hours
        time_24h_ago = transaction_timestamp - timedelta(hours=24)
        tickets_last_24h_stmt = select(func.count()).where(
            ResaleTransaction.seller_id == seller_id,
            ResaleTransaction.timestamp >= time_24h_ago,
            ResaleTransaction.timestamp <= transaction_timestamp
        )
        tickets_sold_last_24h = session.execute(tickets_last_24h_stmt).scalar()
        
        # 3. Get seller's historical fraud rate from profiler agent
        try:
            seller_profile = get_user_trust_profile(seller_id)
            seller_historical_fraud_rate = seller_profile["fraud_rate"]
        except ValueError:
            # If seller not found in users table, default to 0
            seller_historical_fraud_rate = 0.0
        
        # 4. Check if buyer and seller have transacted before (collusion detection)
        repeat_pair_stmt = select(func.count()).where(
            ResaleTransaction.seller_id == seller_id,
            ResaleTransaction.buyer_id == buyer_id,
            ResaleTransaction.transaction_id != transaction.transaction_id
        )
        repeat_pair_count = session.execute(repeat_pair_stmt).scalar()
        repeat_buyer_seller_pair = repeat_pair_count > 0
        
        # Return investigation findings
        return {
            "duplicate_ticket_found": duplicate_ticket_found,
            "tickets_sold_last_24h": tickets_sold_last_24h,
            "seller_historical_fraud_rate": seller_historical_fraud_rate,
            "repeat_buyer_seller_pair": repeat_buyer_seller_pair,
        }


if __name__ == "__main__":
    # Test the function with a real flagged transaction from the database
    print("Finding a flagged transaction for investigation...\n")
    
    with Session(engine) as session:
        # Query for a flagged transaction (is_fraud=1)
        flagged_stmt = select(
            ResaleTransaction.seller_id,
            ResaleTransaction.ticket_id,
            ResaleTransaction.transaction_id
        ).where(
            ResaleTransaction.is_fraud == True
        ).limit(1)
        
        result = session.execute(flagged_stmt).first()
        
        if result:
            seller_id, ticket_id, transaction_id = result
            print(f"Investigating flagged transaction:")
            print(f"  Transaction ID: {transaction_id}")
            print(f"  Seller ID: {seller_id}")
            print(f"  Ticket ID: {ticket_id}")
            print()
            
            # Run the investigation
            findings = investigate_transaction(seller_id, ticket_id)
            
            print("Investigation Findings:")
            print(f"  Duplicate Ticket Found: {findings['duplicate_ticket_found']}")
            print(f"  Tickets Sold Last 24h: {findings['tickets_sold_last_24h']}")
            print(f"  Seller Historical Fraud Rate: {findings['seller_historical_fraud_rate'] * 100:.2f}%")
            print(f"  Repeat Buyer-Seller Pair: {findings['repeat_buyer_seller_pair']}")
        else:
            print("No flagged transactions found in the database.")
