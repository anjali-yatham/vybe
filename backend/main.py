import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from agents.orchestrator import evaluate_transaction
from database.init_db import Event, PrimarySaleTransaction, ResaleTransaction, User

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

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for User response
class UserResponse(BaseModel):
    user_id: str
    role: str
    account_created_at: str
    trust_score: float
    verified_fan: bool

    class Config:
        from_attributes = True


# Pydantic model for Event response
class EventResponse(BaseModel):
    event_id: str
    category: str
    face_value_price: float
    event_date: str
    max_resale_multiplier: float
    high_demand: bool
    total_tickets: int
    organizer_id: str

    class Config:
        from_attributes = True


# Pydantic model for PrimarySaleTransaction response
class PrimarySaleTransactionResponse(BaseModel):
    primary_transaction_id: str
    timestamp: str
    ticket_id: str
    event_id: str
    buyer_id: str
    face_value_price: float
    is_bulk_bot_suspected: bool

    class Config:
        from_attributes = True


# Pydantic model for ResaleTransaction response
class ResaleTransactionResponse(BaseModel):
    transaction_id: str
    timestamp: str
    ticket_id: str
    event_id: str
    event_category: str
    seller_id: str
    buyer_id: str
    face_value_price: float
    resale_price: float
    price_markup_ratio: float
    seller_account_age_days: float
    buyer_account_age_days: float
    hours_since_ticket_purchase: float
    seller_tickets_last_hour: int
    payment_reuse_count: int
    is_duplicate_ticket_attempt: bool
    fraud_archetypes: str | None
    is_fraud: bool

    class Config:
        from_attributes = True


# Pydantic model for transaction evaluation request
class EvaluateTransactionRequest(BaseModel):
    transaction_id: str
    seller_id: str
    buyer_id: str
    ticket_id: str
    price_markup_ratio: float
    seller_account_age_days: float
    buyer_account_age_days: float
    hours_since_ticket_purchase: float
    seller_tickets_last_hour: int
    payment_reuse_count: int
    is_duplicate_ticket_attempt: int


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


@app.get("/events", response_model=List[EventResponse])
def get_events():
    """Get all events from the database."""
    with Session(engine) as session:
        stmt = select(Event)
        events = session.execute(stmt).scalars().all()
        
        # Convert to list of dicts for JSON serialization
        return [
            {
                "event_id": event.event_id,
                "category": event.category,
                "face_value_price": float(event.face_value_price),
                "event_date": event.event_date.isoformat(),
                "max_resale_multiplier": float(event.max_resale_multiplier),
                "high_demand": event.high_demand,
                "total_tickets": event.total_tickets,
                "organizer_id": event.organizer_id,
            }
            for event in events
        ]


@app.get("/primary-sales", response_model=List[PrimarySaleTransactionResponse])
def get_primary_sales():
    """Get all primary sale transactions from the database."""
    with Session(engine) as session:
        stmt = select(PrimarySaleTransaction)
        transactions = session.execute(stmt).scalars().all()
        
        # Convert to list of dicts for JSON serialization
        return [
            {
                "primary_transaction_id": txn.primary_transaction_id,
                "timestamp": txn.timestamp.isoformat(),
                "ticket_id": txn.ticket_id,
                "event_id": txn.event_id,
                "buyer_id": txn.buyer_id,
                "face_value_price": float(txn.face_value_price),
                "is_bulk_bot_suspected": txn.is_bulk_bot_suspected,
            }
            for txn in transactions
        ]


@app.get("/resale-transactions", response_model=List[ResaleTransactionResponse])
def get_resale_transactions():
    """Get all resale transactions from the database."""
    with Session(engine) as session:
        stmt = select(ResaleTransaction)
        transactions = session.execute(stmt).scalars().all()
        
        # Convert to list of dicts for JSON serialization
        return [
            {
                "transaction_id": txn.transaction_id,
                "timestamp": txn.timestamp.isoformat(),
                "ticket_id": txn.ticket_id,
                "event_id": txn.event_id,
                "event_category": txn.event_category,
                "seller_id": txn.seller_id,
                "buyer_id": txn.buyer_id,
                "face_value_price": float(txn.face_value_price),
                "resale_price": float(txn.resale_price),
                "price_markup_ratio": float(txn.price_markup_ratio),
                "seller_account_age_days": float(txn.seller_account_age_days),
                "buyer_account_age_days": float(txn.buyer_account_age_days),
                "hours_since_ticket_purchase": float(txn.hours_since_ticket_purchase),
                "seller_tickets_last_hour": txn.seller_tickets_last_hour,
                "payment_reuse_count": txn.payment_reuse_count,
                "is_duplicate_ticket_attempt": txn.is_duplicate_ticket_attempt,
                "fraud_archetypes": txn.fraud_archetypes,
                "is_fraud": txn.is_fraud,
            }
            for txn in transactions
        ]


@app.post("/evaluate-transaction")
def evaluate_transaction_endpoint(request: EvaluateTransactionRequest):
    """
    Evaluate a transaction through the fraud detection pipeline.
    
    Runs the complete pipeline including:
    - Profiler Agent (trust profile)
    - Anomaly Detection (IsolationForest)
    - Investigation Agent (if flagged)
    - Decision & Explanation Agent (if flagged)
    
    Returns a comprehensive evaluation result.
    """
    try:
        # Convert Pydantic model to dictionary for orchestrator
        transaction_dict = {
            "transaction_id": request.transaction_id,
            "seller_id": request.seller_id,
            "buyer_id": request.buyer_id,
            "ticket_id": request.ticket_id,
            "price_markup_ratio": request.price_markup_ratio,
            "seller_account_age_days": request.seller_account_age_days,
            "buyer_account_age_days": request.buyer_account_age_days,
            "hours_since_ticket_purchase": request.hours_since_ticket_purchase,
            "seller_tickets_last_hour": request.seller_tickets_last_hour,
            "payment_reuse_count": request.payment_reuse_count,
            "is_duplicate_ticket_attempt": request.is_duplicate_ticket_attempt,
        }
        
        # Run the fraud detection pipeline
        result = evaluate_transaction(transaction_dict)
        
        return result
        
    except Exception as e:
        # Return a 500 error with clear error message if anything fails
        raise HTTPException(
            status_code=500,
            detail=f"Failed to evaluate transaction: {str(e)}"
        )
