"""
CCFraud Detector - AI-powered credit card fraud detection using Anthropic Claude.

A production-ready Python package for detecting credit card fraud using
advanced AI analysis powered by Anthropic's Claude models.

Features:
    - Transaction fraud detection
    - Card number validation (Luhn + AI)
    - CVV validation
    - Card image analysis (fake card detection)
    - Person image analysis (identity fraud)
    - Form field signal analysis
    - Scam detection (prostitution, rackets, bank looting, data mining, etc.)

Example:
    >>> from ccfraud_detector import CCFraudDetector, Transaction
    >>> detector = CCFraudDetector(api_key="your-api-key")
    >>> transaction = Transaction(
    ...     amount=9999.99,
    ...     merchant="Suspicious Store",
    ...     category="electronics",
    ...     timestamp="2026-01-10T03:45:00Z"
    ... )
    >>> result = detector.analyze_transaction(transaction)
    >>> print(result.is_fraud, result.risk_score)

Authors:
    Aditya Patange <contact.adityapatange@gmail.com>
    Ekta Bhatia

License:
    MIT License

Repository:
    https://github.com/AdityaPatange1/creditcard_fraud_classifier
"""

from ccfraud_detector.detector import (
    CCFraudDetector,
    FraudResult,
    FraudType,
    Transaction,
)

__version__ = "2.0.1"
__author__ = "Ekta Bhatia (Lead Developer), Aditya Patange"
__email__ = "ekta.bhatia@gmail.com"
__license__ = "MIT"

__all__ = [
    "CCFraudDetector",
    "FraudResult",
    "FraudType",
    "Transaction",
    "__version__",
    "__author__",
]
