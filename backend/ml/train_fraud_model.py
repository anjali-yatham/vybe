from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Set up paths
BACKEND_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_DIR / "data"
ML_DIR = BACKEND_DIR / "ml"

# Feature columns to use for training
FEATURE_COLUMNS = [
    "price_markup_ratio",
    "seller_account_age_days",
    "buyer_account_age_days",
    "hours_since_ticket_purchase",
    "seller_tickets_last_hour",
    "payment_reuse_count",
    "is_duplicate_ticket_attempt",
]


def main():
    print("Loading resale transactions data...")
    df = pd.read_csv(DATA_DIR / "resale_transactions.csv")
    
    # Sort by timestamp (ascending)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    print(f"Total rows: {len(df)}")
    
    # Select features and target
    X = df[FEATURE_COLUMNS].copy()
    y = df["is_fraud"].copy()
    
    # Split 80/20 by TIME (not random)
    split_idx = int(len(df) * 0.8)
    X_train = X.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]
    
    print(f"Training set: {len(X_train)} rows")
    print(f"Test set: {len(X_test)} rows")
    
    # Scale the features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train IsolationForest model
    print("\nTraining IsolationForest model...")
    model = IsolationForest(contamination=0.08, random_state=42)
    model.fit(X_train_scaled)
    
    # Predict on test set
    print("\nPredicting on test set...")
    predictions = model.predict(X_test_scaled)
    
    # Convert IsolationForest's -1/1 output to 1/0 (1 = fraud, 0 = legit)
    # IsolationForest: -1 = outlier (fraud), 1 = inlier (legit)
    predictions_binary = (predictions == -1).astype(int)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, predictions_binary, target_names=["Legit", "Fraud"]))
    
    # Save the trained model and scaler
    print("\nSaving model and scaler...")
    ML_DIR.mkdir(exist_ok=True)
    joblib.dump(model, ML_DIR / "fraud_model.pkl")
    joblib.dump(scaler, ML_DIR / "scaler.pkl")
    
    print(f"\nModel saved to: {ML_DIR / 'fraud_model.pkl'}")
    print(f"Scaler saved to: {ML_DIR / 'scaler.pkl'}")
    print("\nTraining complete!")


if __name__ == "__main__":
    main()
