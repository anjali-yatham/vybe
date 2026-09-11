import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.init_db import User

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from backend/.env")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create FastAPI app
app = FastAPI()


# Pydantic model for User response
class UserResponse(BaseModel):
    user_id: str
    role: str
    account_created_at: str
    trust_score: float
    verified_fan: bool

    class Config:
        from_attributes = True


@app.get("/users", response_model=List[UserResponse])
def get_users():
    """Get all users from the database."""
    with Session(engine) as session:
        stmt = select(User)
        users = session.execute(stmt).scalars().all()
        
        # Convert to list of dicts for JSON serialization
        return [
            {
                "user_id": user.user_id,
                "role": user.role,
                "account_created_at": user.account_created_at.isoformat(),
                "trust_score": float(user.trust_score),
                "verified_fan": user.verified_fan,
            }
            for user in users
        ]
