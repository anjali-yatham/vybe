import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")

# Get Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from backend/.env")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def explain_flagged_transaction(transaction_features: dict) -> str:
    """
    Explain why a transaction was flagged as suspicious using Groq's LLM.
    
    Args:
        transaction_features: Dictionary containing transaction feature values
                            (e.g., price_markup_ratio, seller_account_age_days, etc.)
    
    Returns:
        A plain English explanation (1-2 sentences) of why the transaction is suspicious
    """
    # Build the prompt with transaction feature details
    features_text = "\n".join([f"- {key}: {value}" for key, value in transaction_features.items()])
    
    prompt = f"""You are a fraud analyst assistant for a ticket resale platform.

A transaction has been flagged as suspicious with the following features:
{features_text}

Explain in plain English, in 1-2 sentences, why this transaction was flagged as suspicious. Reference the specific feature values that are concerning."""

    # Send request to Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-oss-120b",
        temperature=0.7,
        max_tokens=150,
    )
    
    # Extract and return the explanation
    explanation = chat_completion.choices[0].message.content.strip()
    return explanation


if __name__ == "__main__":
    # Test the function with example flagged transaction data
    print("Testing fraud explanation with example transaction...\n")
    
    example_transaction = {
        "price_markup_ratio": 3.2,
        "seller_account_age_days": 2,
        "seller_tickets_last_hour": 5,
        "payment_reuse_count": 0,
        "is_duplicate_ticket_attempt": 0,
    }
    
    explanation = explain_flagged_transaction(example_transaction)
    
    print("Transaction Features:")
    for key, value in example_transaction.items():
        print(f"  {key}: {value}")
    
    print(f"\nFraud Explanation:\n{explanation}")
