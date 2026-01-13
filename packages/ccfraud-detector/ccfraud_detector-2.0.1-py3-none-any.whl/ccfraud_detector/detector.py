"""
CCFraud Detector - AI-powered credit card fraud detection using Anthropic Claude.

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
License: MIT
"""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import anthropic


class FraudType(Enum):
    """Types of credit card fraud detected by the system."""

    TRANSACTION = "transaction_fraud"
    CARD_NUMBER = "invalid_card_number"
    CVV = "cvv_anomaly"
    CARD_IMAGE = "fake_card_image"
    PERSON_IMAGE = "fake_person_identity"
    FIELD_SIGNAL = "suspicious_field_pattern"
    SCAM_PROSTITUTION = "prostitution_scam"
    SCAM_RACKET = "organized_racket"
    SCAM_BANK_LOOTING = "bank_looting"
    SCAM_DATA_MINING = "data_mining_fraud"
    SCAM_PHISHING = "phishing_attack"
    SCAM_IDENTITY_THEFT = "identity_theft"
    SCAM_CARD_SKIMMING = "card_skimming"
    SCAM_ACCOUNT_TAKEOVER = "account_takeover"
    CLEAN = "no_fraud_detected"


@dataclass
class FraudResult:
    """Result of fraud detection analysis."""

    is_fraud: bool
    fraud_type: FraudType
    confidence: float
    risk_score: float
    details: str
    recommendations: list[str] = field(default_factory=list)
    raw_analysis: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "is_fraud": self.is_fraud,
            "fraud_type": self.fraud_type.value,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "details": self.details,
            "recommendations": self.recommendations,
        }


@dataclass
class Transaction:
    """Credit card transaction data."""

    amount: float
    merchant: str
    category: str
    timestamp: str
    location: str | None = None
    card_last_four: str | None = None
    is_online: bool = False
    ip_address: str | None = None
    device_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class CCFraudDetector:
    """
    AI-powered credit card fraud detection using Anthropic Claude.

    Detects various fraud types including transaction anomalies, fake cards,
    identity fraud, and organized scams.

    Authors: Ekta Bhatia (Lead Developer), Aditya Patange
    """

    FRAUD_DETECTION_PROMPT = """You are an expert credit card fraud detection system.
Analyze the provided data and determine if fraud is present.

Respond in this exact format:
IS_FRAUD: [true/false]
FRAUD_TYPE: [transaction_fraud|invalid_card_number|cvv_anomaly|fake_card_image|fake_person_identity|suspicious_field_pattern|prostitution_scam|organized_racket|bank_looting|data_mining_fraud|phishing_attack|identity_theft|card_skimming|account_takeover|no_fraud_detected]
CONFIDENCE: [0.0-1.0]
RISK_SCORE: [0.0-100.0]
DETAILS: [Brief explanation]
RECOMMENDATIONS: [Comma-separated list of recommended actions]"""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        """
        Initialize the fraud detector.

        Args:
            api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
            model: Claude model to use for analysis.
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def _parse_response(self, response: str) -> FraudResult:
        """Parse Claude's response into a FraudResult."""
        lines = response.strip().split("\n")
        result: dict[str, Any] = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip().upper()] = value.strip()

        is_fraud = result.get("IS_FRAUD", "false").lower() == "true"
        fraud_type_str = result.get("FRAUD_TYPE", "no_fraud_detected")

        try:
            fraud_type = FraudType(fraud_type_str)
        except ValueError:
            fraud_type = FraudType.CLEAN if not is_fraud else FraudType.TRANSACTION

        try:
            confidence = float(result.get("CONFIDENCE", "0.5"))
        except ValueError:
            confidence = 0.5

        try:
            risk_score = float(result.get("RISK_SCORE", "0.0"))
        except ValueError:
            risk_score = 0.0

        details = result.get("DETAILS", "Analysis complete.")
        recommendations_str = result.get("RECOMMENDATIONS", "")
        recommendations = [r.strip() for r in recommendations_str.split(",") if r.strip()]

        return FraudResult(
            is_fraud=is_fraud,
            fraud_type=fraud_type,
            confidence=min(max(confidence, 0.0), 1.0),
            risk_score=min(max(risk_score, 0.0), 100.0),
            details=details,
            recommendations=recommendations,
            raw_analysis=response,
        )

    def _analyze(self, prompt: str, image_data: str | None = None) -> FraudResult:
        """Send analysis request to Claude."""
        messages: list[dict[str, Any]] = []

        if image_data:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            })
        else:
            messages.append({"role": "user", "content": prompt})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.FRAUD_DETECTION_PROMPT,
            messages=messages,  # type: ignore[arg-type]
        )

        response_text = response.content[0].text  # type: ignore[union-attr]
        return self._parse_response(response_text)

    def analyze_transaction(self, transaction: Transaction) -> FraudResult:
        """
        Analyze a transaction for fraud indicators.

        Args:
            transaction: Transaction data to analyze.

        Returns:
            FraudResult with analysis details.
        """
        prompt = f"""Analyze this credit card transaction for fraud:

Amount: ${transaction.amount:.2f}
Merchant: {transaction.merchant}
Category: {transaction.category}
Timestamp: {transaction.timestamp}
Location: {transaction.location or 'Unknown'}
Card Last Four: {transaction.card_last_four or 'N/A'}
Online Transaction: {transaction.is_online}
IP Address: {transaction.ip_address or 'N/A'}
Device ID: {transaction.device_id or 'N/A'}
Additional Data: {transaction.metadata}

Look for: unusual amounts, suspicious merchants, velocity anomalies,
geographic impossibilities, and patterns indicating organized fraud."""

        return self._analyze(prompt)

    def validate_card_number(self, card_number: str) -> FraudResult:
        """
        Validate a card number using Luhn algorithm and AI analysis.

        Args:
            card_number: Credit card number to validate.

        Returns:
            FraudResult with validation details.
        """
        # Clean the card number
        cleaned = re.sub(r"\D", "", card_number)

        # Luhn algorithm check
        def luhn_check(num: str) -> bool:
            digits = [int(d) for d in num]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            total = sum(odd_digits)
            for d in even_digits:
                total += sum(divmod(d * 2, 10))
            return total % 10 == 0

        luhn_valid = luhn_check(cleaned) if len(cleaned) >= 13 else False

        prompt = f"""Analyze this credit card number for validity and fraud indicators:

Card Number (masked): {'*' * (len(cleaned) - 4) + cleaned[-4:] if len(cleaned) >= 4 else 'INVALID'}
Length: {len(cleaned)} digits
Luhn Check: {'PASS' if luhn_valid else 'FAIL'}
BIN (first 6): {cleaned[:6] if len(cleaned) >= 6 else 'N/A'}

Check for: invalid length, failed checksum, suspicious BIN ranges,
test card patterns, and known fraudulent number patterns."""

        return self._analyze(prompt)

    def validate_cvv(self, cvv: str, card_type: str = "unknown") -> FraudResult:
        """
        Validate CVV format and patterns.

        Args:
            cvv: CVV/CVC code to validate.
            card_type: Type of card (visa, mastercard, amex, etc.)

        Returns:
            FraudResult with validation details.
        """
        prompt = f"""Analyze this CVV/CVC for validity:

CVV Length: {len(cvv)} digits
Card Type: {card_type}
Pattern: {'Sequential' if cvv in ['123', '1234', '234', '345'] else 'Non-sequential'}
Repeating: {'Yes' if len(set(cvv)) == 1 else 'No'}

Check for: invalid length for card type, common test CVVs,
sequential patterns, and suspicious formats."""

        return self._analyze(prompt)

    def analyze_card_image(self, image_path: str | Path) -> FraudResult:
        """
        Analyze a card image for signs of forgery or manipulation.

        Args:
            image_path: Path to the card image file.

        Returns:
            FraudResult with image analysis details.
        """
        path = Path(image_path)
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        prompt = """Analyze this credit card image for fraud indicators:

Look for:
- Signs of physical tampering or alteration
- Inconsistent fonts or printing quality
- Missing or incorrect security features
- Signs of digital manipulation
- Misaligned embossing or text
- Invalid hologram appearance
- Suspicious card design elements"""

        return self._analyze(prompt, image_data)

    def analyze_person_image(self, image_path: str | Path) -> FraudResult:
        """
        Analyze a person's image for identity fraud indicators.

        Args:
            image_path: Path to the person's image file.

        Returns:
            FraudResult with identity analysis details.
        """
        path = Path(image_path)
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        prompt = """Analyze this person's image for identity fraud indicators:

Look for:
- Signs of AI-generated or synthetic faces
- Inconsistent lighting or shadows
- Unnatural skin texture or features
- Signs of photo manipulation
- Inconsistent background elements
- Signs this may be a deepfake
- Stock photo or stolen identity indicators"""

        return self._analyze(prompt, image_data)

    def analyze_field_signals(self, fields: dict[str, Any]) -> FraudResult:
        """
        Analyze form field data for suspicious patterns.

        Args:
            fields: Dictionary of form field names and values.

        Returns:
            FraudResult with field analysis details.
        """
        prompt = f"""Analyze these form fields for fraud signals:

Fields submitted:
{chr(10).join(f'- {k}: {v}' for k, v in fields.items())}

Look for:
- Copy-paste patterns (exact timestamps, identical formatting)
- Bot-like submission speed
- Inconsistent data (mismatched name/email patterns)
- Known fraud indicators in field values
- Suspicious email domains
- Invalid phone number formats
- Address inconsistencies"""

        return self._analyze(prompt)

    def detect_scam(
        self,
        transaction: Transaction | None = None,
        description: str | None = None,
        merchant_category: str | None = None,
    ) -> FraudResult:
        """
        Detect various scam types in transaction or description.

        Detects: prostitution, rackets, bank looting, data mining,
        phishing, identity theft, card skimming, account takeover.

        Args:
            transaction: Optional transaction to analyze.
            description: Optional text description to analyze.
            merchant_category: Optional merchant category code.

        Returns:
            FraudResult with scam detection details.
        """
        context_parts = []

        if transaction:
            context_parts.append(f"""Transaction Details:
- Amount: ${transaction.amount:.2f}
- Merchant: {transaction.merchant}
- Category: {transaction.category}
- Location: {transaction.location or 'Unknown'}""")

        if description:
            context_parts.append(f"Description: {description}")

        if merchant_category:
            context_parts.append(f"MCC: {merchant_category}")

        prompt = f"""Analyze for scam indicators:

{chr(10).join(context_parts)}

Detect these scam types:
- Prostitution/escort service disguised transactions
- Organized crime rackets
- Bank looting schemes
- Data mining/harvesting fraud
- Phishing attacks
- Identity theft patterns
- Card skimming operations
- Account takeover attempts

Identify the specific scam type if detected."""

        return self._analyze(prompt)

    def full_analysis(
        self,
        transaction: Transaction | None = None,
        card_number: str | None = None,
        cvv: str | None = None,
        card_image_path: str | Path | None = None,
        person_image_path: str | Path | None = None,
        form_fields: dict[str, Any] | None = None,
    ) -> dict[str, FraudResult]:
        """
        Perform comprehensive fraud analysis on all provided data.

        Args:
            transaction: Transaction to analyze.
            card_number: Card number to validate.
            cvv: CVV to validate.
            card_image_path: Path to card image.
            person_image_path: Path to person image.
            form_fields: Form field data.

        Returns:
            Dictionary mapping analysis type to FraudResult.
        """
        results: dict[str, FraudResult] = {}

        if transaction:
            results["transaction"] = self.analyze_transaction(transaction)
            results["scam"] = self.detect_scam(transaction=transaction)

        if card_number:
            results["card_number"] = self.validate_card_number(card_number)

        if cvv:
            results["cvv"] = self.validate_cvv(cvv)

        if card_image_path:
            results["card_image"] = self.analyze_card_image(card_image_path)

        if person_image_path:
            results["person_image"] = self.analyze_person_image(person_image_path)

        if form_fields:
            results["field_signals"] = self.analyze_field_signals(form_fields)

        return results


__all__ = ["CCFraudDetector", "FraudResult", "FraudType", "Transaction"]
