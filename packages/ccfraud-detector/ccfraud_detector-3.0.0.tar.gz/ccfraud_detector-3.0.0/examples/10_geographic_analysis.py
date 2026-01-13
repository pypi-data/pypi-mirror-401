#!/usr/bin/env python3
"""
Example 10: Geographic Velocity Analysis

Demonstrates detection of geographically impossible transactions,
such as purchases in different countries within minutes of each other.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, Transaction

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Detect geographic impossibility fraud patterns."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    print("=" * 60)
    print("CCFraud Detector - Geographic Velocity Analysis")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    # Scenario: Card used in NYC, then 10 minutes later in London
    # This is physically impossible
    print("\nScenario: Geographic Impossibility Detection")
    print("Card used in New York, then London 10 minutes apart\n")

    txn1 = Transaction(
        amount=150.00,
        merchant="Macy's Herald Square",
        category="retail",
        timestamp="2026-01-10T14:00:00Z",
        location="New York, NY, USA",
        card_last_four="4532",
        is_online=False,
        metadata={"geo_coordinates": "40.7505,-73.9877"},
    )

    txn2 = Transaction(
        amount=200.00,
        merchant="Harrods",
        category="retail",
        timestamp="2026-01-10T14:10:00Z",  # Only 10 min later
        location="London, UK",
        card_last_four="4532",  # Same card
        is_online=False,
        metadata={
            "geo_coordinates": "51.4994,-0.1632",
            "previous_transaction": "New York, 10 mins ago",
            "distance_km": "5571",
            "time_gap_minutes": "10",
        },
    )

    print("Transaction 1 (New York):")
    print(f"  Time:     {txn1.timestamp}")
    print(f"  Location: {txn1.location}")
    print(f"  Amount:   ${txn1.amount}")

    result1 = detector.analyze_transaction(txn1)
    print(f"  Risk:     {result1.risk_score}/100")
    print(f"  Status:   {'FLAGGED' if result1.is_fraud else 'OK'}")

    print("\nTransaction 2 (London - 10 minutes later):")
    print(f"  Time:     {txn2.timestamp}")
    print(f"  Location: {txn2.location}")
    print(f"  Amount:   ${txn2.amount}")
    print(f"  Distance: {txn2.metadata['distance_km']} km from previous")
    print(f"  Time Gap: {txn2.metadata['time_gap_minutes']} minutes")

    result2 = detector.analyze_transaction(txn2)
    print(f"  Risk:     {result2.risk_score}/100")
    print(f"  Status:   {'FLAGGED' if result2.is_fraud else 'OK'}")

    # Analysis
    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)
    print(f"Distance between locations: 5,571 km")
    print(f"Time between transactions:  10 minutes")
    print(f"Required speed:             33,426 km/h (impossile)")
    print(f"Fastest commercial flight:  ~900 km/h")
    print(f"\nConclusion: {result2.details}")

    if result2.is_fraud or result2.risk_score > 50:
        print("\nACTION: Card compromised. Block card and notify customer.")


if __name__ == "__main__":
    main()
