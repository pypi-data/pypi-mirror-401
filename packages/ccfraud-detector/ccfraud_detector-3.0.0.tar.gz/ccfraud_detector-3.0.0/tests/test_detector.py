"""
Unit and Integration Tests for CCFraud Detector.

Authors: Aditya Patange, Ekta Bhatia
License: MIT
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from ccfraud_detector import (
    CCFraudDetector,
    FraudResult,
    FraudType,
    Transaction,
    __author__,
    __version__,
)

# =============================================================================
# Unit Tests
# =============================================================================


class TestTransaction:
    """Unit tests for Transaction dataclass."""

    def test_transaction_creation_minimal(self) -> None:
        """Test creating a transaction with minimal fields."""
        txn = Transaction(
            amount=100.00,
            merchant="Test Store",
            category="retail",
            timestamp="2026-01-10T12:00:00Z",
        )
        assert txn.amount == 100.00
        assert txn.merchant == "Test Store"
        assert txn.category == "retail"
        assert txn.location is None
        assert txn.is_online is False

    def test_transaction_creation_full(self) -> None:
        """Test creating a transaction with all fields."""
        txn = Transaction(
            amount=999.99,
            merchant="Online Shop",
            category="electronics",
            timestamp="2026-01-10T03:00:00Z",
            location="New York, NY",
            card_last_four="1234",
            is_online=True,
            ip_address="192.168.1.1",
            device_id="device-abc-123",
            metadata={"user_agent": "Mozilla/5.0"},
        )
        assert txn.amount == 999.99
        assert txn.is_online is True
        assert txn.ip_address == "192.168.1.1"
        assert txn.metadata["user_agent"] == "Mozilla/5.0"


class TestFraudResult:
    """Unit tests for FraudResult dataclass."""

    def test_fraud_result_creation(self) -> None:
        """Test creating a FraudResult."""
        result = FraudResult(
            is_fraud=True,
            fraud_type=FraudType.TRANSACTION,
            confidence=0.95,
            risk_score=87.5,
            details="Suspicious transaction pattern detected",
            recommendations=["Block transaction", "Contact cardholder"],
        )
        assert result.is_fraud is True
        assert result.fraud_type == FraudType.TRANSACTION
        assert result.confidence == 0.95
        assert result.risk_score == 87.5
        assert len(result.recommendations) == 2

    def test_fraud_result_to_dict(self) -> None:
        """Test converting FraudResult to dictionary."""
        result = FraudResult(
            is_fraud=False,
            fraud_type=FraudType.CLEAN,
            confidence=0.99,
            risk_score=5.0,
            details="No fraud detected",
        )
        d = result.to_dict()
        assert d["is_fraud"] is False
        assert d["fraud_type"] == "no_fraud_detected"
        assert d["confidence"] == 0.99
        assert d["risk_score"] == 5.0


class TestFraudType:
    """Unit tests for FraudType enum."""

    def test_all_fraud_types_exist(self) -> None:
        """Test that all expected fraud types are defined."""
        expected_types = [
            "TRANSACTION",
            "CARD_NUMBER",
            "CVV",
            "CARD_IMAGE",
            "PERSON_IMAGE",
            "FIELD_SIGNAL",
            "SCAM_PROSTITUTION",
            "SCAM_RACKET",
            "SCAM_BANK_LOOTING",
            "SCAM_DATA_MINING",
            "SCAM_PHISHING",
            "SCAM_IDENTITY_THEFT",
            "SCAM_CARD_SKIMMING",
            "SCAM_ACCOUNT_TAKEOVER",
            "CLEAN",
        ]
        for fraud_type in expected_types:
            assert hasattr(FraudType, fraud_type)

    def test_fraud_type_values(self) -> None:
        """Test fraud type string values."""
        assert FraudType.TRANSACTION.value == "transaction_fraud"
        assert FraudType.CLEAN.value == "no_fraud_detected"
        assert FraudType.SCAM_BANK_LOOTING.value == "bank_looting"


class TestCCFraudDetectorUnit:
    """Unit tests for CCFraudDetector (mocked API calls)."""

    @pytest.fixture
    def mock_detector(self) -> CCFraudDetector:
        """Create a detector with mocked Anthropic client."""
        with patch("ccfraud_detector.detector.anthropic.Anthropic"):
            detector = CCFraudDetector(api_key="test-key")
        return detector

    def test_detector_initialization(self, mock_detector: CCFraudDetector) -> None:
        """Test detector initializes correctly."""
        assert mock_detector.model == "claude-sonnet-4-20250514"

    def test_parse_response_fraud_detected(self, mock_detector: CCFraudDetector) -> None:
        """Test parsing a response indicating fraud."""
        response = """IS_FRAUD: true
FRAUD_TYPE: transaction_fraud
CONFIDENCE: 0.92
RISK_SCORE: 85.0
DETAILS: Unusual transaction pattern detected
RECOMMENDATIONS: Block card, Contact customer, Review account"""

        result = mock_detector._parse_response(response)
        assert result.is_fraud is True
        assert result.fraud_type == FraudType.TRANSACTION
        assert result.confidence == 0.92
        assert result.risk_score == 85.0
        assert len(result.recommendations) == 3

    def test_parse_response_no_fraud(self, mock_detector: CCFraudDetector) -> None:
        """Test parsing a response indicating no fraud."""
        response = """IS_FRAUD: false
FRAUD_TYPE: no_fraud_detected
CONFIDENCE: 0.98
RISK_SCORE: 2.5
DETAILS: Transaction appears legitimate
RECOMMENDATIONS: Approve transaction"""

        result = mock_detector._parse_response(response)
        assert result.is_fraud is False
        assert result.fraud_type == FraudType.CLEAN
        assert result.confidence == 0.98
        assert result.risk_score == 2.5

    def test_parse_response_clamps_values(self, mock_detector: CCFraudDetector) -> None:
        """Test that confidence and risk_score are clamped to valid ranges."""
        response = """IS_FRAUD: true
FRAUD_TYPE: transaction_fraud
CONFIDENCE: 1.5
RISK_SCORE: 150.0
DETAILS: Test
RECOMMENDATIONS: Test"""

        result = mock_detector._parse_response(response)
        assert result.confidence == 1.0
        assert result.risk_score == 100.0

    def test_parse_response_handles_invalid_values(
        self, mock_detector: CCFraudDetector
    ) -> None:
        """Test parsing handles invalid/malformed values gracefully."""
        response = """IS_FRAUD: maybe
FRAUD_TYPE: unknown_type
CONFIDENCE: invalid
RISK_SCORE: bad
DETAILS: Test response"""

        result = mock_detector._parse_response(response)
        assert result.is_fraud is False
        assert result.fraud_type == FraudType.CLEAN
        assert result.confidence == 0.5
        assert result.risk_score == 0.0


class TestPackageMetadata:
    """Test package metadata."""

    def test_version(self) -> None:
        """Test package version is set."""
        assert __version__ == "1.1.0"

    def test_authors(self) -> None:
        """Test package authors are set correctly."""
        assert "Aditya Patange" in __author__
        assert "Ekta Bhatia" in __author__


# =============================================================================
# Integration Tests
# =============================================================================


@pytest.mark.integration
class TestCCFraudDetectorIntegration:
    """
    Integration tests for CCFraudDetector.

    These tests make real API calls and require ANTHROPIC_API_KEY to be set.
    Run with: pytest -m integration
    """

    @pytest.fixture
    def detector(self) -> CCFraudDetector | None:
        """Create a real detector if API key is available."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")
        return CCFraudDetector(api_key=api_key)

    def test_analyze_legitimate_transaction(
        self, detector: CCFraudDetector | None
    ) -> None:
        """Test analyzing a legitimate-looking transaction."""
        if detector is None:
            pytest.skip("Detector not available")

        txn = Transaction(
            amount=45.99,
            merchant="Local Grocery Store",
            category="groceries",
            timestamp="2026-01-10T14:30:00Z",
            location="San Francisco, CA",
            is_online=False,
        )
        result = detector.analyze_transaction(txn)
        assert isinstance(result, FraudResult)
        assert isinstance(result.is_fraud, bool)
        assert 0.0 <= result.confidence <= 1.0
        assert 0.0 <= result.risk_score <= 100.0

    def test_analyze_suspicious_transaction(
        self, detector: CCFraudDetector | None
    ) -> None:
        """Test analyzing a suspicious transaction."""
        if detector is None:
            pytest.skip("Detector not available")

        txn = Transaction(
            amount=9999.99,
            merchant="UNKNOWN MERCHANT XYZ",
            category="wire_transfer",
            timestamp="2026-01-10T03:45:00Z",
            location="Unknown",
            is_online=True,
            ip_address="185.220.101.1",  # Known Tor exit node range
        )
        result = detector.analyze_transaction(txn)
        assert isinstance(result, FraudResult)
        # Suspicious transaction should have higher risk
        assert result.risk_score > 0

    def test_validate_valid_card_number(
        self, detector: CCFraudDetector | None
    ) -> None:
        """Test validating a valid test card number."""
        if detector is None:
            pytest.skip("Detector not available")

        # Standard test card number (Luhn valid)
        result = detector.validate_card_number("4111111111111111")
        assert isinstance(result, FraudResult)
        assert isinstance(result.is_fraud, bool)

    def test_validate_invalid_card_number(
        self, detector: CCFraudDetector | None
    ) -> None:
        """Test validating an invalid card number."""
        if detector is None:
            pytest.skip("Detector not available")

        result = detector.validate_card_number("1234567890123456")
        assert isinstance(result, FraudResult)

    def test_validate_cvv(self, detector: CCFraudDetector | None) -> None:
        """Test CVV validation."""
        if detector is None:
            pytest.skip("Detector not available")

        result = detector.validate_cvv("123", card_type="visa")
        assert isinstance(result, FraudResult)
        assert isinstance(result.is_fraud, bool)

    def test_analyze_field_signals(self, detector: CCFraudDetector | None) -> None:
        """Test field signal analysis."""
        if detector is None:
            pytest.skip("Detector not available")

        fields = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "address": "123 Main St, New York, NY 10001",
        }
        result = detector.analyze_field_signals(fields)
        assert isinstance(result, FraudResult)

    def test_detect_scam(self, detector: CCFraudDetector | None) -> None:
        """Test scam detection."""
        if detector is None:
            pytest.skip("Detector not available")

        result = detector.detect_scam(
            description="Wire transfer to overseas account for investment opportunity",
            merchant_category="6012",
        )
        assert isinstance(result, FraudResult)


# =============================================================================
# Pytest Configuration
# =============================================================================


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
