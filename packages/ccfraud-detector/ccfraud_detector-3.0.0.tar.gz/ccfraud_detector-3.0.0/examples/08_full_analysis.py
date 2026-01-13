#!/usr/bin/env python3
"""
Example 8: Comprehensive Full Analysis

Demonstrates the full_analysis() method that performs
all available fraud checks on provided data simultaneously.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, Transaction

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Perform comprehensive fraud analysis on all available data."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    print("=" * 60)
    print("CCFraud Detector - Comprehensive Full Analysis")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    # Create transaction
    transaction = Transaction(
        amount=2500.00,
        merchant="Electronics Outlet",
        category="electronics",
        timestamp="2026-01-10T15:30:00Z",
        location="Miami, FL",
        card_last_four="7890",
        is_online=True,
        ip_address="72.134.89.12",
        device_id="device-12345",
    )

    # Form data
    form_fields = {
        "billing_name": "Robert Johnson",
        "billing_email": "r.johnson@email.com",
        "billing_phone": "+1-305-555-0123",
        "billing_address": "456 Palm Avenue",
        "billing_city": "Miami",
        "billing_state": "FL",
        "billing_zip": "33101",
        "shipping_same": "true",
    }

    print("\nRunning comprehensive analysis...")
    print("  - Transaction analysis")
    print("  - Card number validation")
    print("  - CVV validation")
    print("  - Field signal analysis")
    print("  - Scam detection")

    # Run full analysis
    results = detector.full_analysis(
        transaction=transaction,
        card_number="4532015112830366",  # Test card
        cvv="789",
        form_fields=form_fields,
    )

    # Display results
    print("\n" + "=" * 60)
    print("COMPREHENSIVE ANALYSIS RESULTS")
    print("=" * 60)

    total_risk = 0
    fraud_detected = False

    for analysis_type, result in results.items():
        print(f"\n{'─'*50}")
        print(f"Analysis: {analysis_type.upper()}")
        print(f"{'─'*50}")
        print(f"  Fraud Detected: {result.is_fraud}")
        print(f"  Fraud Type:     {result.fraud_type.value}")
        print(f"  Confidence:     {result.confidence:.2%}")
        print(f"  Risk Score:     {result.risk_score}/100")
        print(f"  Details:        {result.details}")

        total_risk += result.risk_score
        if result.is_fraud:
            fraud_detected = True

    # Overall assessment
    avg_risk = total_risk / len(results)
    print("\n" + "=" * 60)
    print("OVERALL ASSESSMENT")
    print("=" * 60)
    print(f"Analyses Performed:    {len(results)}")
    print(f"Fraud Flags Raised:    {sum(1 for r in results.values() if r.is_fraud)}")
    print(f"Average Risk Score:    {avg_risk:.1f}/100")

    if fraud_detected:
        print("\nRECOMMENDATION: BLOCK TRANSACTION - Fraud indicators detected")
    elif avg_risk > 50:
        print("\nRECOMMENDATION: MANUAL REVIEW - Elevated risk score")
    else:
        print("\nRECOMMENDATION: APPROVE - Low risk transaction")


if __name__ == "__main__":
    main()
