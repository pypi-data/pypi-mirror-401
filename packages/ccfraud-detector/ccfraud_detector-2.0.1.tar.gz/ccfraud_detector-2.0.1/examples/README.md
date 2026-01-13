# CCFraud Detector Examples

**Authors: Ekta Bhatia (Lead Developer) & Aditya Patange**

This directory contains 12 comprehensive examples demonstrating various use cases of the CCFraud Detector package.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your Anthropic API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Examples

| # | File | Description |
|---|------|-------------|
| 1 | `01_basic_transaction.py` | Basic transaction fraud analysis |
| 2 | `02_suspicious_transaction.py` | Detecting high-risk suspicious transactions |
| 3 | `03_card_validation.py` | Card number validation (Luhn + AI) |
| 4 | `04_cvv_validation.py` | CVV pattern analysis |
| 5 | `05_field_signals.py` | Form field and bot detection |
| 6 | `06_scam_detection.py` | Various scam type detection |
| 7 | `07_batch_analysis.py` | Batch processing multiple transactions |
| 8 | `08_full_analysis.py` | Comprehensive multi-factor analysis |
| 9 | `09_realtime_monitoring.py` | Real-time monitoring simulation |
| 10 | `10_geographic_analysis.py` | Geographic impossibility detection |
| 11 | `11_image_analysis.py` | Card and identity image analysis |
| 12 | `12_enterprise_integration.py` | Enterprise integration patterns |

## Running Examples

Run any example:
```bash
python 01_basic_transaction.py
```

Run all examples:
```bash
for f in *.py; do echo "Running $f..."; python "$f"; echo; done
```

## Test Images

For image analysis examples, place test images in the `test_images/` directory:
- `test_card.jpg` - Sample credit card image
- `test_person.jpg` - Sample identity photo

---

**Built by Ekta Bhatia (Lead Developer) & Aditya Patange**
