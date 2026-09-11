"""
TicketTrust Data Simulator
===========================
Generates a small relational dataset for the TicketTrust platform:
  1. users.csv                      - user accounts (buyers/sellers/admin-created)
  2. events.csv                     - events across movie/concert/sports
  3. primary_sale_transactions.csv  - Flow A: organiser -> first buyer (low fraud risk)
  4. resale_transactions.csv        - Flow B: user -> user resale (the ML training set)

Fixes applied vs the earlier version:
  - ticket_id is now a GUARANTEED-unique UUID-based ID -> no cross-event collisions
  - "duplicate_ticket" fraud rows are now REAL duplicates: the same ticket_id appears
    twice in resale_transactions.csv, sold to two different buyers, with overlapping
    or very close timestamps -> the is_duplicate_ticket_attempt flag is now always
    backed by an actual duplicate structure in the data (verified at the end of this
    script)
"""

import pandas as pd
import numpy as np
import uuid
import datetime as dt

RNG = np.random.default_rng(42)
N_USERS = 600
N_EVENTS = 150
CATEGORIES = ["movie", "concert", "sports"]
START_DATE = dt.datetime(2026, 1, 1)
END_DATE = dt.datetime(2026, 6, 30)

# ---------------------------------------------------------------------------
# 1. USERS
# ---------------------------------------------------------------------------
def gen_users(n=N_USERS):
    user_ids = [f"U{100000+i}" for i in range(n)]
    created = [START_DATE - dt.timedelta(days=float(d)) for d in
               RNG.exponential(scale=250, size=n).clip(0, 2200)]
    trust_score = RNG.normal(70, 15, size=n).clip(0, 100).round(1)
    verified_fan = RNG.choice([0, 1], size=n, p=[0.7, 0.3])
    role = ["admin"] + ["user"] * (n - 1)  # first user = the admin/organiser account

    df = pd.DataFrame({
        "user_id": user_ids,
        "role": role,
        "account_created_at": created,
        "trust_score": trust_score,
        "verified_fan": verified_fan,
    })
    return df

users = gen_users()

# ---------------------------------------------------------------------------
# 2. EVENTS
# ---------------------------------------------------------------------------
def gen_events(n=N_EVENTS):
    event_ids = [f"E{2000+i}" for i in range(n)]
    category = RNG.choice(CATEGORIES, size=n, p=[0.35, 0.4, 0.25])
    base_price = np.where(
        category == "concert", RNG.uniform(60, 400, n),
        np.where(category == "sports", RNG.uniform(40, 300, n),
                 RNG.uniform(8, 40, n))  # movies are cheap
    ).round(2)
    event_date = [START_DATE + dt.timedelta(days=float(d)) for d in
                  RNG.uniform(0, 200, n)]
    max_resale_multiplier = np.round(RNG.uniform(1.1, 1.5, n), 2)  # anti-scalping cap
    high_demand = RNG.choice([0, 1], size=n, p=[0.75, 0.25])
    total_tickets = RNG.integers(100, 5000, n)

    df = pd.DataFrame({
        "event_id": event_ids,
        "category": category,
        "face_value_price": base_price,
        "event_date": event_date,
        "max_resale_multiplier": max_resale_multiplier,
        "high_demand": high_demand,
        "total_tickets": total_tickets,
        "organizer_id": users.loc[0, "user_id"],
    })
    return df

events = gen_events()

# ---------------------------------------------------------------------------
# 3. PRIMARY SALE TRANSACTIONS (Flow A) + underlying tickets
# ---------------------------------------------------------------------------
def gen_primary_sales_and_tickets(n_tickets=20000):
    rows_tx = []
    rows_tickets = []
    real_users = users[users["role"] == "user"].reset_index(drop=True)

    for i in range(n_tickets):
        ev = events.iloc[RNG.integers(0, len(events))]
        buyer = real_users.iloc[RNG.integers(0, len(real_users))]
        ticket_id = f"T-{uuid.uuid4().hex[:10]}"
        purchase_time = ev["event_date"] - dt.timedelta(
            days=float(RNG.uniform(1, 120))
        )
        # light bot/bulk-buy signal for primary sale (rare)
        is_bulk_bot = 1 if RNG.random() < 0.015 else 0

        rows_tx.append({
            "primary_transaction_id": f"PTX{100000+i}",
            "timestamp": purchase_time,
            "ticket_id": ticket_id,
            "event_id": ev["event_id"],
            "buyer_id": buyer["user_id"],
            "face_value_price": ev["face_value_price"],
            "is_bulk_bot_suspected": is_bulk_bot,
        })
        rows_tickets.append({
            "ticket_id": ticket_id,
            "event_id": ev["event_id"],
            "category": ev["category"],
            "face_value_price": ev["face_value_price"],
            "current_owner_id": buyer["user_id"],
            "original_buyer_id": buyer["user_id"],
            "original_purchase_time": purchase_time,
            "status": "valid",
        })

    return pd.DataFrame(rows_tx), pd.DataFrame(rows_tickets)

primary_sales, tickets = gen_primary_sales_and_tickets()
tickets = tickets.merge(
    events[["event_id", "max_resale_multiplier"]], on="event_id", how="left"
)

# ---------------------------------------------------------------------------
# 4. RESALE TRANSACTIONS (Flow B) -- the main ML dataset
# ---------------------------------------------------------------------------
FRAUD_ARCHETYPES = ["scalping", "bot_bulk_resale", "new_account_flip",
                     "payment_mule", "duplicate_ticket"]

def pick_buyer(exclude_id, real_users):
    b = real_users.iloc[RNG.integers(0, len(real_users))]
    while b["user_id"] == exclude_id:
        b = real_users.iloc[RNG.integers(0, len(real_users))]
    return b

def gen_resale_transactions(n_resales=25000, resellable_tickets=None):
    real_users = users[users["role"] == "user"].reset_index(drop=True)
    users_by_id = users.set_index("user_id")
    rows = []
    tx_counter = 0

    # pool of tickets eligible for resale (already primary-sold)
    pool = resellable_tickets.sample(
        n=min(n_resales, len(resellable_tickets)), replace=True, random_state=1
    ).reset_index(drop=True)

    # decide which rows will be forced genuine "duplicate_ticket" fraud pairs
    n_duplicate_fraud_pairs = 180
    duplicate_pair_indices = RNG.choice(
        len(pool), size=n_duplicate_fraud_pairs, replace=False
    )

    for idx in range(len(pool)):
        t = pool.iloc[idx]
        seller = users_by_id.loc[t["current_owner_id"]] if t["current_owner_id"] in users_by_id.index else real_users.iloc[0]
        seller_id = t["current_owner_id"]
        buyer_row = pick_buyer(seller_id, real_users)
        buyer_id = buyer_row["user_id"]

        base_time = t["original_purchase_time"] if not pd.isna(t["original_purchase_time"]) else START_DATE
        resale_time = base_time + dt.timedelta(hours=float(RNG.exponential(180)))
        resale_time = min(resale_time, END_DATE)
        hours_since_purchase = max((resale_time - base_time).total_seconds() / 3600, 0)

        seller_created = users_by_id.loc[seller_id, "account_created_at"] if seller_id in users_by_id.index else START_DATE
        seller_age_days = max((resale_time - seller_created).total_seconds() / 86400, 0)
        buyer_age_days = max((resale_time - buyer_row["account_created_at"]).total_seconds() / 86400, 0)

        face_value = t["face_value_price"]
        cap = t["max_resale_multiplier"]

        # ---- decide fraud / legit ----
        is_forced_duplicate = idx in duplicate_pair_indices
        fraud_roll = RNG.random()
        archetypes = []

        if is_forced_duplicate:
            archetypes.append("duplicate_ticket")

        # independent probabilistic fraud signals (can stack)
        if seller_age_days < 3 and RNG.random() < 0.35:
            archetypes.append("new_account_flip")
        if RNG.random() < 0.02:
            archetypes.append("bot_bulk_resale")
        if RNG.random() < 0.015:
            archetypes.append("payment_mule")
        if RNG.random() < 0.02 and "duplicate_ticket" not in archetypes:
            archetypes.append("scalping")

        is_fraud = 1 if len(archetypes) > 0 else 0

        # price markup: fraud -> higher markup; legit -> hovers near 1.0, capped
        if is_fraud and ("scalping" in archetypes or "duplicate_ticket" in archetypes):
            markup = RNG.uniform(1.8, 4.5)
        elif is_fraud:
            markup = RNG.uniform(1.1, 2.2)
        else:
            markup = RNG.normal(1.02, 0.08)
            markup = np.clip(markup, 0.6, cap)  # legit sellers mostly respect the cap

        resale_price = round(face_value * markup, 2)
        markup_ratio = round(resale_price / face_value, 3)

        seller_tickets_last_hour = (
            RNG.integers(3, 12) if "bot_bulk_resale" in archetypes else RNG.integers(0, 2)
        )
        payment_reuse_count = (
            RNG.integers(2, 6) if "payment_mule" in archetypes else RNG.integers(0, 2)
        )

        tx_counter += 1
        rows.append({
            "transaction_id": f"RTX{100000+tx_counter}",
            "timestamp": resale_time,
            "ticket_id": t["ticket_id"],
            "event_id": t["event_id"],
            "event_category": t["category"],
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "face_value_price": face_value,
            "resale_price": resale_price,
            "price_markup_ratio": markup_ratio,
            "seller_account_age_days": round(seller_age_days, 1),
            "buyer_account_age_days": round(buyer_age_days, 1),
            "hours_since_ticket_purchase": round(hours_since_purchase, 1),
            "seller_tickets_last_hour": int(seller_tickets_last_hour),
            "payment_reuse_count": int(payment_reuse_count),
            "is_duplicate_ticket_attempt": 1 if "duplicate_ticket" in archetypes else 0,
            "fraud_archetypes": ",".join(archetypes) if archetypes else "",
            "is_fraud": is_fraud,
        })

        # if this is a forced duplicate pair, immediately create the SECOND
        # sale of the SAME ticket_id to a DIFFERENT buyer, close in time
        if is_forced_duplicate:
            buyer2_row = pick_buyer(seller_id, real_users)
            while buyer2_row["user_id"] == buyer_id:
                buyer2_row = pick_buyer(seller_id, real_users)
            resale_time_2 = resale_time + dt.timedelta(minutes=float(RNG.uniform(5, 240)))
            markup2 = RNG.uniform(1.8, 4.5)
            resale_price_2 = round(face_value * markup2, 2)
            tx_counter += 1
            rows.append({
                "transaction_id": f"RTX{100000+tx_counter}",
                "timestamp": resale_time_2,
                "ticket_id": t["ticket_id"],           # SAME ticket_id -> real duplicate
                "event_id": t["event_id"],
                "event_category": t["category"],
                "seller_id": seller_id,
                "buyer_id": buyer2_row["user_id"],
                "face_value_price": face_value,
                "resale_price": resale_price_2,
                "price_markup_ratio": round(resale_price_2 / face_value, 3),
                "seller_account_age_days": round(seller_age_days, 1),
                "buyer_account_age_days": round(
                    (resale_time_2 - buyer2_row["account_created_at"]).total_seconds() / 86400, 1
                ),
                "hours_since_ticket_purchase": round(hours_since_purchase, 1),
                "seller_tickets_last_hour": int(RNG.integers(2, 8)),
                "payment_reuse_count": int(RNG.integers(0, 3)),
                "is_duplicate_ticket_attempt": 1,
                "fraud_archetypes": "duplicate_ticket",
                "is_fraud": 1,
            })

    return pd.DataFrame(rows)

resale = gen_resale_transactions(resellable_tickets=tickets)
resale = resale.sort_values("timestamp").reset_index(drop=True)

# ---------------------------------------------------------------------------
# SAVE ALL FILES
# ---------------------------------------------------------------------------
OUT = "/mnt/user-data/outputs"
users.to_csv(f"{OUT}/users.csv", index=False)
events.to_csv(f"{OUT}/events.csv", index=False)
primary_sales.to_csv(f"{OUT}/primary_sale_transactions.csv", index=False)
resale.to_csv(f"{OUT}/resale_transactions.csv", index=False)

print("Saved: users.csv, events.csv, primary_sale_transactions.csv, resale_transactions.csv")
print("\nresale_transactions shape:", resale.shape)
print("Fraud ratio:", resale['is_fraud'].mean().round(4))

# ---------------------------------------------------------------------------
# VERIFICATION -- confirm both bugs are fixed
# ---------------------------------------------------------------------------
print("\n--- VERIFICATION ---")

# Bug 1 check: ticket_id -> consistent face_value_price / event_id
fv_check = resale.groupby("ticket_id")["face_value_price"].nunique()
print("Tickets with inconsistent face_value_price (should be 0):", (fv_check > 1).sum())
ev_check = resale.groupby("ticket_id")["event_id"].nunique()
print("Tickets with inconsistent event_id (should be 0):", (ev_check > 1).sum())

# Bug 2 check: every is_duplicate_ticket_attempt=1 row must have a ticket_id
# that appears >1 times in the dataset
dup_ticket_ids = resale["ticket_id"].value_counts()
flagged = resale[resale["is_duplicate_ticket_attempt"] == 1]
backed = flagged["ticket_id"].isin(dup_ticket_ids[dup_ticket_ids > 1].index).sum()
print(f"Duplicate-flagged rows backed by an actual repeated ticket_id: {backed} / {len(flagged)}")

print("\nFraud archetype counts:\n", resale["fraud_archetypes"].replace("", "none").value_counts().head(10))
