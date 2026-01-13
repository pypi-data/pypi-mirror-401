#!/usr/bin/env python3
"""
Example 2: Suspicious Transaction Detection

Demonstrates detection of a highly suspicious transaction with
multiple red flags: high amount, unusual time, unknown merchant.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, Transaction

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Detect a suspicious high-risk transaction."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    # Suspicious transaction with multiple red flags
    suspicious_txn = Transaction(
        amount=9999.99,
        merchant="UNKNOWN MERCHANT XYZ123",
        category="wire_transfer",
        timestamp="2026-01-10T03:45:00Z",  # Unusual time (3:45 AM)
        location="Unknown",
        card_last_four="1234",
        is_online=True,
        ip_address="185.220.101.1",  # Known suspicious IP range
        device_id="new-device-never-seen",
        metadata={
            "velocity": "5_transactions_in_10_minutes",
            "geo_mismatch": True,
            "new_device": True,
        },
    )

    print("=" * 60)
    print("CCFraud Detector - Suspicious Transaction Detection")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    print("\nTransaction Details:")
    print(f"  Amount:     ${suspicious_txn.amount}")
    print(f"  Merchant:   {suspicious_txn.merchant}")
    print(f"  Time:       {suspicious_txn.timestamp}")
    print(f"  IP Address: {suspicious_txn.ip_address}")
    print(f"  Metadata:   {suspicious_txn.metadata}")

    result = detector.analyze_transaction(suspicious_txn)

    print(f"\n{'='*40}")
    print("FRAUD ANALYSIS RESULTS")
    print(f"{'='*40}")
    print(f"FRAUD DETECTED: {result.is_fraud}")
    print(f"Fraud Type:     {result.fraud_type.value}")
    print(f"Confidence:     {result.confidence:.2%}")
    print(f"Risk Score:     {result.risk_score}/100")
    print(f"\nDetails: {result.details}")
    print(f"\nRecommendations:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"  {i}. {rec}")


if __name__ == "__main__":
    main()
