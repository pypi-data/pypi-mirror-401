#!/usr/bin/env python3
"""
Example 4: CVV Validation

Demonstrates CVV/CVC validation for different card types,
detecting suspicious patterns like sequential or repeated digits.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Validate CVV codes for various card types."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    # Test CVV patterns
    test_cvvs = [
        ("123", "visa", "Sequential pattern"),
        ("742", "mastercard", "Random valid CVV"),
        ("1234", "amex", "Amex 4-digit CVV"),
        ("000", "visa", "All zeros - suspicious"),
        ("111", "visa", "Repeated digits"),
        ("999", "mastercard", "Repeated nines"),
    ]

    print("=" * 60)
    print("CCFraud Detector - CVV Validation")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    for cvv, card_type, description in test_cvvs:
        print(f"\n{'─'*50}")
        print(f"Testing: {description}")
        print(f"CVV:     {'*' * len(cvv)} ({len(cvv)} digits)")
        print(f"Card:    {card_type.upper()}")

        result = detector.validate_cvv(cvv, card_type=card_type)

        status = "SUSPICIOUS" if result.is_fraud else "OK"
        print(f"Status:  {status}")
        print(f"Risk:    {result.risk_score}/100")
        print(f"Details: {result.details}")


if __name__ == "__main__":
    main()
