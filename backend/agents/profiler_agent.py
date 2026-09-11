import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from database.init_db import ResaleTransaction, User

# Load environment variables from .env
BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")

# Get database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from backend/.env")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)


def get_user_trust_profile(user_id: str) -> dict:
    """
    Get a comprehensive trust profile for a user.
    
    Args:
        user_id: The user ID to look up
    
    Returns:
        Dictionary containing user trust information including:
        - user_id: The user's ID
        - trust_score: The user's trust score
        - account_created_at: When the account was created
        - verified_fan: Whether the user is a verified fan
        - total_resales: Total number of resale transactions as seller
        - fraud_count: Number of fraudulent resale transactions
        - fraud_rate: Percentage of fraudulent transactions (0-1)
    """
    with Session(engine) as session:
        # Query the users table for this user
        user_stmt = select(User).where(User.user_id == user_id)
        user = session.execute(user_stmt).scalar_one_or_none()
        
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")
        
        # Query resale_transactions table to count resales by this seller
        total_resales_stmt = select(func.count()).where(
            ResaleTransaction.seller_id == user_id
        )
        total_resales = session.execute(total_resales_stmt).scalar()
        
        # Count how many of those resales were fraud
        fraud_count_stmt = select(func.count()).where(
            ResaleTransaction.seller_id == user_id,
            ResaleTransaction.is_fraud == True
        )
        fraud_count = session.execute(fraud_count_stmt).scalar()
        
        # Calculate fraud rate
        fraud_rate = fraud_count / total_resales if total_resales > 0 else 0.0
        
        # Build and return the trust profile
        return {
            "user_id": user.user_id,
            "trust_score": float(user.trust_score),
            "account_created_at": user.account_created_at.isoformat(),
            "verified_fan": user.verified_fan,
            "total_resales": total_resales,
            "fraud_count": fraud_count,
            "fraud_rate": round(fraud_rate, 4),
        }


if __name__ == "__main__":
    # Test the function with a real user ID from the database
    print("Fetching trust profile for user U100001...\n")
    
    try:
        profile = get_user_trust_profile("U100001")
        
        print("User Trust Profile:")
        print(f"  User ID: {profile['user_id']}")
        print(f"  Trust Score: {profile['trust_score']}")
        print(f"  Account Created: {profile['account_created_at']}")
        print(f"  Verified Fan: {profile['verified_fan']}")
        print(f"  Total Resales: {profile['total_resales']}")
        print(f"  Fraud Count: {profile['fraud_count']}")
        print(f"  Fraud Rate: {profile['fraud_rate'] * 100:.2f}%")
    except ValueError as e:
        print(f"Error: {e}")
