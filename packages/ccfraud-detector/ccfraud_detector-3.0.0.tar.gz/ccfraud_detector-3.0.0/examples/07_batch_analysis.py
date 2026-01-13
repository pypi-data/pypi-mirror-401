#!/usr/bin/env python3
"""
Example 7: Batch Transaction Analysis

Demonstrates processing multiple transactions in batch,
useful for analyzing historical data or real-time streams.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, FraudType, Transaction

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Process a batch of transactions and generate summary report."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    # Batch of transactions to analyze
    transactions = [
        Transaction(
            amount=25.99,
            merchant="Starbucks",
            category="food_beverage",
            timestamp="2026-01-10T08:15:00Z",
            location="New York, NY",
            is_online=False,
        ),
        Transaction(
            amount=1500.00,
            merchant="Best Buy",
            category="electronics",
            timestamp="2026-01-10T12:30:00Z",
            location="New York, NY",
            is_online=False,
        ),
        Transaction(
            amount=9999.99,
            merchant="UNKNOWN_VENDOR",
            category="wire_transfer",
            timestamp="2026-01-10T03:00:00Z",
            location="Unknown",
            is_online=True,
            ip_address="185.220.101.45",
        ),
        Transaction(
            amount=42.50,
            merchant="Uber",
            category="transportation",
            timestamp="2026-01-10T19:45:00Z",
            location="New York, NY",
            is_online=True,
        ),
        Transaction(
            amount=5000.00,
            merchant="FOREX_TRADE_NOW",
            category="investment",
            timestamp="2026-01-10T04:30:00Z",
            location="Unknown",
            is_online=True,
        ),
    ]

    print("=" * 60)
    print("CCFraud Detector - Batch Transaction Analysis")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)
    print(f"\nProcessing {len(transactions)} transactions...")

    results = []
    flagged = []

    for i, txn in enumerate(transactions, 1):
        print(f"\n[{i}/{len(transactions)}] Analyzing: ${txn.amount} at {txn.merchant}")
        result = detector.analyze_transaction(txn)
        results.append((txn, result))

        status = "FLAGGED" if result.is_fraud else "OK"
        print(f"  Status: {status} | Risk: {result.risk_score}/100")

        if result.is_fraud or result.risk_score > 50:
            flagged.append((txn, result))

    # Summary Report
    print("\n" + "=" * 60)
    print("BATCH ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Transactions:  {len(transactions)}")
    print(f"Flagged for Review:  {len(flagged)}")
    print(f"Clean Transactions:  {len(transactions) - len(flagged)}")

    avg_risk = sum(r.risk_score for _, r in results) / len(results)
    print(f"Average Risk Score:  {avg_risk:.1f}/100")

    if flagged:
        print("\n" + "─" * 50)
        print("FLAGGED TRANSACTIONS")
        print("─" * 50)
        for txn, result in flagged:
            print(f"\n  ${txn.amount} at {txn.merchant}")
            print(f"  Risk: {result.risk_score}/100 | Type: {result.fraud_type.value}")
            print(f"  Reason: {result.details}")


if __name__ == "__main__":
    main()
