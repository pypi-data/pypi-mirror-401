#!/usr/bin/env python3
"""
Example 5: Form Field Signal Analysis

Demonstrates detection of suspicious patterns in form submissions,
including bot detection, copy-paste patterns, and data anomalies.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Analyze form field signals for fraud indicators."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    # Legitimate form submission
    legitimate_fields = {
        "name": "John Michael Smith",
        "email": "john.smith@gmail.com",
        "phone": "+1-555-123-4567",
        "address": "123 Oak Street, Apt 4B",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94102",
        "country": "USA",
    }

    # Suspicious form submission (bot-like patterns)
    suspicious_fields = {
        "name": "asdfgh jklqwe",
        "email": "temp12345@tempmail.xyz",
        "phone": "1111111111",
        "address": "123",
        "city": "aaaa",
        "state": "XX",
        "zip": "00000",
        "country": "ZZ",
        "submission_time_ms": "47",  # Too fast for human
        "honeypot_field": "filled",  # Bot filled hidden field
    }

    print("=" * 60)
    print("CCFraud Detector - Form Field Signal Analysis")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    # Test legitimate submission
    print("\n" + "─" * 50)
    print("Test 1: Legitimate Form Submission")
    print("─" * 50)
    result1 = detector.analyze_field_signals(legitimate_fields)
    print(f"Suspicious: {result1.is_fraud}")
    print(f"Risk Score: {result1.risk_score}/100")
    print(f"Details:    {result1.details}")

    # Test suspicious submission
    print("\n" + "─" * 50)
    print("Test 2: Suspicious Bot-like Submission")
    print("─" * 50)
    result2 = detector.analyze_field_signals(suspicious_fields)
    print(f"Suspicious: {result2.is_fraud}")
    print(f"Risk Score: {result2.risk_score}/100")
    print(f"Details:    {result2.details}")
    if result2.recommendations:
        print("Recommendations:")
        for rec in result2.recommendations:
            print(f"  - {rec}")


if __name__ == "__main__":
    main()
