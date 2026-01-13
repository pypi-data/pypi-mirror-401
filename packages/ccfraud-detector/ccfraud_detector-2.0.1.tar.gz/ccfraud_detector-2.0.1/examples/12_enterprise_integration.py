#!/usr/bin/env python3
"""
Example 12: Enterprise Integration Pattern

Demonstrates how to integrate CCFraud Detector into enterprise
systems with proper error handling, logging, and reporting.

This example shows patterns used by financial institutions,
payment processors, and security operations centers (SOC).

Authors: Ekta Bhatia (Lead Developer), Aditya Patange
"""

import json
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from ccfraud_detector import CCFraudDetector, FraudResult, FraudType, Transaction

load_dotenv(Path(__file__).parent / ".env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("FraudDetection")


@dataclass
class FraudAlert:
    """Structured fraud alert for enterprise systems."""

    alert_id: str
    timestamp: str
    transaction_id: str
    amount: float
    merchant: str
    fraud_type: str
    risk_score: float
    confidence: float
    action_taken: str
    details: str
    recommendations: list[str]

    def to_json(self) -> str:
        """Convert alert to JSON for API/webhook integration."""
        return json.dumps(asdict(self), indent=2)


class EnterprisefraudDetector:
    """
    Enterprise-grade fraud detection wrapper.

    Features:
    - Structured logging
    - Alert generation
    - Configurable thresholds
    - Audit trail
    - Integration-ready outputs

    Authors: Ekta Bhatia (Lead Developer), Aditya Patange
    """

    def __init__(
        self,
        api_key: str,
        block_threshold: float = 75.0,
        review_threshold: float = 40.0,
    ) -> None:
        self.detector = CCFraudDetector(api_key=api_key)
        self.block_threshold = block_threshold
        self.review_threshold = review_threshold
        self.alerts: list[FraudAlert] = []
        logger.info("Enterprise Fraud Detector initialized")
        logger.info(f"Block threshold: {block_threshold}, Review threshold: {review_threshold}")

    def process_transaction(
        self, transaction: Transaction, transaction_id: str
    ) -> tuple[str, FraudAlert | None]:
        """
        Process a transaction and return decision with optional alert.

        Returns:
            Tuple of (decision, alert) where decision is APPROVE/REVIEW/BLOCK
        """
        logger.info(f"Processing transaction {transaction_id}: ${transaction.amount}")

        try:
            result = self.detector.analyze_transaction(transaction)
        except Exception as e:
            logger.error(f"Analysis failed for {transaction_id}: {e}")
            return "ERROR", None

        # Determine action based on thresholds
        if result.is_fraud or result.risk_score >= self.block_threshold:
            action = "BLOCK"
            logger.warning(f"BLOCKED: {transaction_id} - Risk: {result.risk_score}")
        elif result.risk_score >= self.review_threshold:
            action = "REVIEW"
            logger.info(f"REVIEW: {transaction_id} - Risk: {result.risk_score}")
        else:
            action = "APPROVE"
            logger.info(f"APPROVED: {transaction_id} - Risk: {result.risk_score}")

        # Generate alert for non-approved transactions
        alert = None
        if action != "APPROVE":
            alert = FraudAlert(
                alert_id=f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{transaction_id}",
                timestamp=datetime.now().isoformat(),
                transaction_id=transaction_id,
                amount=transaction.amount,
                merchant=transaction.merchant,
                fraud_type=result.fraud_type.value,
                risk_score=result.risk_score,
                confidence=result.confidence,
                action_taken=action,
                details=result.details,
                recommendations=result.recommendations,
            )
            self.alerts.append(alert)

        return action, alert

    def get_session_report(self) -> dict[str, Any]:
        """Generate session summary report."""
        return {
            "session_end": datetime.now().isoformat(),
            "total_alerts": len(self.alerts),
            "alerts_by_type": self._count_by_type(),
            "alerts": [asdict(a) for a in self.alerts],
        }

    def _count_by_type(self) -> dict[str, int]:
        """Count alerts by fraud type."""
        counts: dict[str, int] = {}
        for alert in self.alerts:
            counts[alert.fraud_type] = counts.get(alert.fraud_type, 0) + 1
        return counts


def main() -> None:
    """Demonstrate enterprise integration pattern."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    print("=" * 60)
    print("CCFraud Detector - Enterprise Integration")
    print("Authors: Ekta Bhatia (Lead Developer), Aditya Patange")
    print("=" * 60)
    print()

    # Initialize enterprise detector
    fraud_system = EnterprisefraudDetector(
        api_key=api_key,
        block_threshold=75.0,
        review_threshold=40.0,
    )

    # Simulate incoming transactions
    test_transactions = [
        (
            "TXN-001",
            Transaction(
                amount=45.99,
                merchant="Local Coffee Shop",
                category="food",
                timestamp="2026-01-10T09:00:00Z",
                is_online=False,
            ),
        ),
        (
            "TXN-002",
            Transaction(
                amount=8500.00,
                merchant="UNKNOWN_MERCHANT",
                category="wire_transfer",
                timestamp="2026-01-10T03:30:00Z",
                is_online=True,
                ip_address="185.220.101.1",
            ),
        ),
        (
            "TXN-003",
            Transaction(
                amount=299.00,
                merchant="Amazon.com",
                category="electronics",
                timestamp="2026-01-10T14:15:00Z",
                is_online=True,
            ),
        ),
    ]

    print("Processing transactions...\n")

    decisions = []
    for txn_id, txn in test_transactions:
        decision, alert = fraud_system.process_transaction(txn, txn_id)
        decisions.append((txn_id, decision))

        if alert:
            print(f"\n{'='*50}")
            print("FRAUD ALERT GENERATED")
            print("=" * 50)
            print(alert.to_json())

    # Session summary
    print("\n" + "=" * 60)
    print("SESSION SUMMARY")
    print("=" * 60)
    for txn_id, decision in decisions:
        print(f"  {txn_id}: {decision}")

    report = fraud_system.get_session_report()
    print(f"\nTotal Alerts: {report['total_alerts']}")
    print(f"By Type: {report['alerts_by_type']}")


if __name__ == "__main__":
    main()
