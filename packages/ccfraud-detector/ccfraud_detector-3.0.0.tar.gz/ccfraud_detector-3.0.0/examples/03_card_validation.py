#!/usr/bin/env python3
"""
Example 3: Card Number Validation

Demonstrates card number validation using Luhn algorithm
combined with AI-powered pattern analysis.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Validate multiple card numbers."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    # Test card numbers (these are standard test numbers, not real cards)
    test_cards = [
        ("4111111111111111", "Visa Test Card"),
        ("5500000000000004", "Mastercard Test Card"),
        ("340000000000009", "Amex Test Card"),
        ("1234567890123456", "Invalid Card (Luhn fails)"),
        ("0000000000000000", "Suspicious Pattern"),
    ]

    print("=" * 60)
    print("CCFraud Detector - Card Number Validation")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    for card_number, description in test_cards:
        print(f"\n{'─'*50}")
        print(f"Testing: {description}")
        print(f"Card:    {'*' * 12}{card_number[-4:]}")

        result = detector.validate_card_number(card_number)

        status = "INVALID/SUSPICIOUS" if result.is_fraud else "VALID"
        print(f"Status:  {status}")
        print(f"Risk:    {result.risk_score}/100")
        print(f"Details: {result.details}")


if __name__ == "__main__":
    main()
