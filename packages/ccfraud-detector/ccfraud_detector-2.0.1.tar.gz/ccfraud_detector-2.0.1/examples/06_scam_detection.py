#!/usr/bin/env python3
"""
Example 6: Scam Detection

Demonstrates detection of various scam types including phishing,
identity theft, organized rackets, and financial fraud schemes.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, Transaction

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Detect various types of scams and fraud schemes."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    print("=" * 60)
    print("CCFraud Detector - Scam Detection Suite")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    # Test Case 1: Phishing scam
    print("\n" + "─" * 50)
    print("Test 1: Potential Phishing Scam")
    print("─" * 50)
    result1 = detector.detect_scam(
        description="Urgent: Your account has been compromised. "
        "Click here to verify your identity and enter your card details.",
        merchant_category="5999",
    )
    print(f"Scam Detected: {result1.is_fraud}")
    print(f"Type:          {result1.fraud_type.value}")
    print(f"Risk Score:    {result1.risk_score}/100")

    # Test Case 2: Investment scam
    print("\n" + "─" * 50)
    print("Test 2: Investment Fraud Scheme")
    print("─" * 50)
    investment_txn = Transaction(
        amount=50000.00,
        merchant="CRYPTO GUARANTEED RETURNS LLC",
        category="investment",
        timestamp="2026-01-10T02:30:00Z",
        is_online=True,
    )
    result2 = detector.detect_scam(
        transaction=investment_txn,
        description="Guaranteed 500% returns in 30 days. Limited time offer. "
        "Wire transfer required immediately.",
    )
    print(f"Scam Detected: {result2.is_fraud}")
    print(f"Type:          {result2.fraud_type.value}")
    print(f"Risk Score:    {result2.risk_score}/100")

    # Test Case 3: Romance/advance fee scam
    print("\n" + "─" * 50)
    print("Test 3: Advance Fee Scam")
    print("─" * 50)
    result3 = detector.detect_scam(
        description="I need $5000 to pay customs fees to release your inheritance. "
        "Please send via Western Union to Nigeria.",
        merchant_category="4829",  # Wire transfer
    )
    print(f"Scam Detected: {result3.is_fraud}")
    print(f"Type:          {result3.fraud_type.value}")
    print(f"Risk Score:    {result3.risk_score}/100")

    # Test Case 4: Legitimate transaction
    print("\n" + "─" * 50)
    print("Test 4: Legitimate Transaction (Control)")
    print("─" * 50)
    legit_txn = Transaction(
        amount=45.99,
        merchant="Whole Foods Market",
        category="grocery",
        timestamp="2026-01-10T18:30:00Z",
        location="Austin, TX",
        is_online=False,
    )
    result4 = detector.detect_scam(transaction=legit_txn)
    print(f"Scam Detected: {result4.is_fraud}")
    print(f"Type:          {result4.fraud_type.value}")
    print(f"Risk Score:    {result4.risk_score}/100")


if __name__ == "__main__":
    main()
