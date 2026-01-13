#!/usr/bin/env python3
"""
Example 1: Basic Transaction Analysis

Demonstrates how to analyze a simple credit card transaction for fraud.
This is the most common use case for the CCFraud Detector.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, Transaction

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Analyze a basic transaction for fraud indicators."""
    # Initialize the detector with API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    # Create a sample transaction
    transaction = Transaction(
        amount=125.99,
        merchant="Amazon.com",
        category="online_retail",
        timestamp="2026-01-10T14:30:00Z",
        location="Seattle, WA",
        card_last_four="4532",
        is_online=True,
    )

    print("=" * 60)
    print("CCFraud Detector - Basic Transaction Analysis")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)
    print(f"\nAnalyzing transaction: ${transaction.amount} at {transaction.merchant}")

    # Analyze the transaction
    result = detector.analyze_transaction(transaction)

    # Display results
    print(f"\n{'='*40}")
    print("ANALYSIS RESULTS")
    print(f"{'='*40}")
    print(f"Is Fraud:        {result.is_fraud}")
    print(f"Fraud Type:      {result.fraud_type.value}")
    print(f"Confidence:      {result.confidence:.2%}")
    print(f"Risk Score:      {result.risk_score}/100")
    print(f"Details:         {result.details}")
    print(f"Recommendations: {', '.join(result.recommendations) if result.recommendations else 'None'}")


if __name__ == "__main__":
    main()
