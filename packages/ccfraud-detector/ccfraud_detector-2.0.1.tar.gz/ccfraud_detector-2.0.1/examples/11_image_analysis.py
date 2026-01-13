#!/usr/bin/env python3
"""
Example 11: Card and Identity Image Analysis

Demonstrates analysis of card images and person photos to detect
fake cards, manipulated images, and synthetic identities.

Note: This example uses sample test images. In production,
you would analyze actual card/identity verification images.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector

load_dotenv(Path(__file__).parent / ".env")


def main() -> None:
    """Demonstrate image-based fraud detection capabilities."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    detector = CCFraudDetector(api_key=api_key)

    print("=" * 60)
    print("CCFraud Detector - Image Analysis Suite")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)

    examples_dir = Path(__file__).parent
    test_images_dir = examples_dir / "test_images"

    # Check for test images
    card_image = test_images_dir / "test_card.jpg"
    person_image = test_images_dir / "test_person.jpg"

    print("\nImage Analysis Capabilities:")
    print("─" * 50)
    print("1. Card Image Analysis")
    print("   - Detect physical tampering")
    print("   - Identify fake/counterfeit cards")
    print("   - Check security features")
    print("   - Detect digital manipulation")
    print()
    print("2. Person Image Analysis")
    print("   - Detect AI-generated faces")
    print("   - Identify deepfakes")
    print("   - Check for photo manipulation")
    print("   - Detect stock photo usage")

    if card_image.exists():
        print(f"\n{'─'*50}")
        print("Analyzing Card Image...")
        print(f"{'─'*50}")
        result = detector.analyze_card_image(card_image)
        print(f"Fake/Tampered: {result.is_fraud}")
        print(f"Fraud Type:    {result.fraud_type.value}")
        print(f"Confidence:    {result.confidence:.2%}")
        print(f"Risk Score:    {result.risk_score}/100")
        print(f"Details:       {result.details}")
    else:
        print(f"\nNote: No test card image found at {card_image}")
        print("To test card analysis, place a card image at the path above.")

    if person_image.exists():
        print(f"\n{'─'*50}")
        print("Analyzing Person Image...")
        print(f"{'─'*50}")
        result = detector.analyze_person_image(person_image)
        print(f"Fake/Synthetic: {result.is_fraud}")
        print(f"Fraud Type:     {result.fraud_type.value}")
        print(f"Confidence:     {result.confidence:.2%}")
        print(f"Risk Score:     {result.risk_score}/100")
        print(f"Details:        {result.details}")
    else:
        print(f"\nNote: No test person image found at {person_image}")
        print("To test identity analysis, place a person image at the path above.")

    # Usage example
    print("\n" + "=" * 60)
    print("USAGE IN YOUR CODE")
    print("=" * 60)
    print("""
from ccfraud_detector import CCFraudDetector

detector = CCFraudDetector(api_key="your-key")

# Analyze a card image
card_result = detector.analyze_card_image("/path/to/card.jpg")
if card_result.is_fraud:
    print("Fake card detected!")

# Analyze identity photo
person_result = detector.analyze_person_image("/path/to/photo.jpg")
if person_result.is_fraud:
    print("Synthetic/fake identity detected!")
""")


if __name__ == "__main__":
    main()
