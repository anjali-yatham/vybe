from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


BACKEND_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_DIR / "data"
load_dotenv(BACKEND_DIR / ".env")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    account_created_at: Mapped[pd.Timestamp] = mapped_column(DateTime, nullable=False)
    trust_score: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    verified_fan: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Event(Base):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    face_value_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    event_date: Mapped[pd.Timestamp] = mapped_column(DateTime, nullable=False)
    max_resale_multiplier: Mapped[float] = mapped_column(Numeric(8, 3), nullable=False)
    high_demand: Mapped[bool] = mapped_column(Boolean, nullable=False)
    total_tickets: Mapped[int] = mapped_column(Integer, nullable=False)
    organizer_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)


class PrimarySaleTransaction(Base):
    __tablename__ = "primary_sale_transactions"

    primary_transaction_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    timestamp: Mapped[pd.Timestamp] = mapped_column(DateTime, nullable=False)
    ticket_id: Mapped[str] = mapped_column(String(32), nullable=False)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.event_id"), nullable=False)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    face_value_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    is_bulk_bot_suspected: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ResaleTransaction(Base):
    __tablename__ = "resale_transactions"

    transaction_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    timestamp: Mapped[pd.Timestamp] = mapped_column(DateTime, nullable=False)
    ticket_id: Mapped[str] = mapped_column(String(32), nullable=False)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.event_id"), nullable=False)
    event_category: Mapped[str] = mapped_column(String(64), nullable=False)
    seller_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    face_value_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    resale_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_markup_ratio: Mapped[float] = mapped_column(Numeric(10, 3), nullable=False)
    seller_account_age_days: Mapped[float] = mapped_column(Numeric(10, 1), nullable=False)
    buyer_account_age_days: Mapped[float] = mapped_column(Numeric(10, 1), nullable=False)
    hours_since_ticket_purchase: Mapped[float] = mapped_column(Numeric(10, 1), nullable=False)
    seller_tickets_last_hour: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_reuse_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_duplicate_ticket_attempt: Mapped[bool] = mapped_column(Boolean, nullable=False)
    fraud_archetypes: Mapped[str | None] = mapped_column(String(128), nullable=True)
    is_fraud: Mapped[bool] = mapped_column(Boolean, nullable=False)


def load_csv(model: type[Base], filename: str, engine) -> int:
    dataframe = pd.read_csv(DATA_DIR / filename)
    for column in dataframe.columns:
        if column in {"account_created_at", "event_date", "timestamp"}:
            dataframe[column] = pd.to_datetime(dataframe[column])
        elif column.startswith("is_") or column in {"verified_fan", "high_demand"}:
            dataframe[column] = dataframe[column].astype(bool)
    dataframe.to_sql(model.__tablename__, engine, if_exists="append", index=False)
    return len(dataframe)


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is missing from backend/.env")

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    counts = {
        User.__tablename__: load_csv(User, "users.csv", engine),
        Event.__tablename__: load_csv(Event, "events.csv", engine),
        PrimarySaleTransaction.__tablename__: load_csv(
            PrimarySaleTransaction, "primary_sale_transactions.csv", engine
        ),
        ResaleTransaction.__tablename__: load_csv(
            ResaleTransaction, "resale_transactions.csv", engine
        ),
    }
    print("Database initialized successfully.")
    for table_name, row_count in counts.items():
        print(f"{table_name}: {row_count} rows imported")


if __name__ == "__main__":
    main()