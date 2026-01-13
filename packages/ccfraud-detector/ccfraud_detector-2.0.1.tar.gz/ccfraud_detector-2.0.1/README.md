# CCFraud Detector

**AI-powered credit card fraud detection using Anthropic Claude**

[![PyPI version](https://badge.fury.io/py/ccfraud-detector.svg)](https://pypi.org/project/ccfraud-detector/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Python package for comprehensive credit card fraud detection powered by Anthropic's Claude AI models.

## Authors & Contributors

- **Ekta Bhatia** - Lead Developer - [ekta.bhatia@gmail.com](mailto:ekta.bhatia@gmail.com)
- **Aditya Patange** - Co-Developer - [contact.adityapatange@gmail.com](mailto:contact.adityapatange@gmail.com)

## Features

- **Transaction Analysis** - Detect fraudulent transactions using AI-powered pattern recognition
- **Card Number Validation** - Luhn algorithm + AI analysis for card number verification
- **CVV Validation** - Intelligent CVV format and pattern analysis
- **Card Image Analysis** - Detect fake, tampered, or manipulated card images
- **Person Image Analysis** - Identify synthetic faces, deepfakes, and stolen identities
- **Form Field Signals** - Detect bot submissions, copy-paste patterns, and suspicious data
- **Scam Detection** - Identify various fraud schemes including:
  - Prostitution/escort service disguised transactions
  - Organized crime rackets
  - Bank looting schemes
  - Data mining/harvesting fraud
  - Phishing attacks
  - Identity theft
  - Card skimming operations
  - Account takeover attempts

## Installation

```bash
pip install ccfraud-detector
```

For development:

```bash
pip install ccfraud-detector[dev]
```

## Quick Start

```python
from ccfraud_detector import CCFraudDetector, Transaction

# Initialize the detector
detector = CCFraudDetector(api_key="your-anthropic-api-key")

# Analyze a transaction
transaction = Transaction(
    amount=9999.99,
    merchant="Suspicious Electronics Store",
    category="electronics",
    timestamp="2026-01-10T03:45:00Z",
    location="Unknown Location",
    is_online=True,
    ip_address="185.220.101.1"
)

result = detector.analyze_transaction(transaction)

print(f"Is Fraud: {result.is_fraud}")
print(f"Fraud Type: {result.fraud_type.value}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Risk Score: {result.risk_score}/100")
print(f"Details: {result.details}")
print(f"Recommendations: {result.recommendations}")
```

## API Reference

### CCFraudDetector

The main class for fraud detection.

```python
from ccfraud_detector import CCFraudDetector

detector = CCFraudDetector(
    api_key="your-api-key",  # Optional: uses ANTHROPIC_API_KEY env var if not provided
    model="claude-sonnet-4-20250514"  # Optional: Claude model to use
)
```

### Methods

#### `analyze_transaction(transaction: Transaction) -> FraudResult`

Analyze a credit card transaction for fraud indicators.

```python
from ccfraud_detector import Transaction

txn = Transaction(
    amount=150.00,
    merchant="Online Store",
    category="retail",
    timestamp="2026-01-10T14:30:00Z",
    location="New York, NY",
    card_last_four="1234",
    is_online=True,
    ip_address="192.168.1.1",
    device_id="device-abc",
    metadata={"user_agent": "Mozilla/5.0"}
)

result = detector.analyze_transaction(txn)
```

#### `validate_card_number(card_number: str) -> FraudResult`

Validate a card number using Luhn algorithm and AI analysis.

```python
result = detector.validate_card_number("4111111111111111")
```

#### `validate_cvv(cvv: str, card_type: str = "unknown") -> FraudResult`

Validate CVV format and detect suspicious patterns.

```python
result = detector.validate_cvv("123", card_type="visa")
```

#### `analyze_card_image(image_path: str | Path) -> FraudResult`

Analyze a card image for signs of forgery or manipulation.

```python
result = detector.analyze_card_image("/path/to/card_image.jpg")
```

#### `analyze_person_image(image_path: str | Path) -> FraudResult`

Analyze a person's image for identity fraud indicators (synthetic faces, deepfakes).

```python
result = detector.analyze_person_image("/path/to/person_photo.jpg")
```

#### `analyze_field_signals(fields: dict) -> FraudResult`

Analyze form field data for suspicious patterns.

```python
result = detector.analyze_field_signals({
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-123-4567",
    "address": "123 Main St"
})
```

#### `detect_scam(...) -> FraudResult`

Detect various scam types in transaction or description.

```python
result = detector.detect_scam(
    transaction=txn,
    description="Wire transfer for investment",
    merchant_category="6012"
)
```

#### `full_analysis(...) -> dict[str, FraudResult]`

Perform comprehensive fraud analysis on all provided data.

```python
results = detector.full_analysis(
    transaction=txn,
    card_number="4111111111111111",
    cvv="123",
    card_image_path="/path/to/card.jpg",
    person_image_path="/path/to/person.jpg",
    form_fields={"name": "John Doe"}
)

for analysis_type, result in results.items():
    print(f"{analysis_type}: {result.is_fraud} (risk: {result.risk_score})")
```

### Data Classes

#### `Transaction`

```python
@dataclass
class Transaction:
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
```

#### `FraudResult`

```python
@dataclass
class FraudResult:
    is_fraud: bool
    fraud_type: FraudType
    confidence: float  # 0.0 to 1.0
    risk_score: float  # 0.0 to 100.0
    details: str
    recommendations: list[str]
    raw_analysis: str
```

#### `FraudType`

```python
class FraudType(Enum):
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
```

## Development

### Setup

```bash
git clone https://github.com/AdityaPatange1/creditcard_fraud_classifier.git
cd creditcard_fraud_classifier
make install-dev
```

### Commands

```bash
make lint          # Run linter
make format        # Format code
make typecheck     # Run type checking
make test          # Run unit tests
make test-integration  # Run integration tests (requires ANTHROPIC_API_KEY)
make test-all      # Run all tests
make coverage      # Generate coverage report
make build         # Build distribution
make clean         # Clean build artifacts
```

### Running Tests

Unit tests (no API key required):

```bash
make test-unit
```

Integration tests (requires `ANTHROPIC_API_KEY`):

```bash
export ANTHROPIC_API_KEY=your-key
make test-integration
```

## Dataset

This project includes analysis based on the [Kaggle Credit Card Fraud Detection Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/AdityaPatange1/creditcard_fraud_classifier/issues) page.

---

**Built with care by Ekta Bhatia (Lead Developer) & Aditya Patange**
