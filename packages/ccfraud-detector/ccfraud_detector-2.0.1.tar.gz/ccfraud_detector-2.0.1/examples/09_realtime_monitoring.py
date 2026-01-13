#!/usr/bin/env python3
"""
Example 9: Real-time Transaction Monitoring

Demonstrates a real-time monitoring system that analyzes
transactions as they come in and alerts on suspicious activity.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
import random
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, Transaction

load_dotenv(Path(__file__).parent / ".env")


def generate_mock_transaction() -> Transaction:
    """Generate a mock transaction for demonstration."""
    merchants = [
        ("Amazon.com", "online_retail", True),
        ("Walmart", "retail", False),
        ("Shell Gas Station", "fuel", False),
        ("SUSPICIOUS_VENDOR_XYZ", "unknown", True),
        ("Netflix", "subscription", True),
        ("Local Restaurant", "food", False),
        ("CRYPTO_EXCHANGE_ANON", "cryptocurrency", True),
        ("Apple Store", "electronics", False),
    ]

    merchant, category, is_online = random.choice(merchants)

    # Occasionally generate suspicious amounts
    if random.random() < 0.2:
        amount = round(random.uniform(5000, 15000), 2)
    else:
        amount = round(random.uniform(5, 500), 2)

    return Transaction(
        amount=amount,
        merchant=merchant,
        category=category,
        timestamp=datetime.now().isoformat() + "Z",
        location="Various" if is_online else "Local Store",
        is_online=is_online,
        ip_address="192.168.1.1" if is_online else None,
    )


def main() -> None:
    """Run real-time transaction monitoring simulation."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    print("=" * 60)
    print("CCFraud Detector - Real-time Monitoring System")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)
    print("\nStarting real-time transaction monitoring...")
    print("Processing 5 simulated transactions...\n")

    stats = {"total": 0, "flagged": 0, "approved": 0}

    # Simulate 5 transactions
    for i in range(5):
        txn = generate_mock_transaction()
        stats["total"] += 1

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Transaction #{i+1}")
        print(f"  Amount:   ${txn.amount}")
        print(f"  Merchant: {txn.merchant}")

        result = detector.analyze_transaction(txn)

        if result.is_fraud or result.risk_score > 70:
            stats["flagged"] += 1
            print(f"  Status:   BLOCKED (Risk: {result.risk_score}/100)")
            print(f"  Reason:   {result.fraud_type.value}")
            print(f"  Action:   Transaction blocked, alert sent to security team")
        elif result.risk_score > 40:
            stats["approved"] += 1
            print(f"  Status:   REVIEW (Risk: {result.risk_score}/100)")
            print(f"  Action:   Approved with manual review flag")
        else:
            stats["approved"] += 1
            print(f"  Status:   APPROVED (Risk: {result.risk_score}/100)")

        print()
        time.sleep(1)  # Brief pause between transactions

    # Summary
    print("=" * 60)
    print("MONITORING SESSION SUMMARY")
    print("=" * 60)
    print(f"Total Transactions:  {stats['total']}")
    print(f"Approved:            {stats['approved']}")
    print(f"Blocked/Flagged:     {stats['flagged']}")
    print(f"Block Rate:          {stats['flagged']/stats['total']*100:.1f}%")


if __name__ == "__main__":
    main()
