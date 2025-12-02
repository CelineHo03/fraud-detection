# Vietnamese Fraud Detection System

Week 1 foundation for fraud detection targeting Vietnamese phishing and scam messages.

## Status

**Week 1: COMPLETE ✅**

## Quick Start

### Prerequisites
- Python 3.8+
- Docker

### Setup
```bash
# 1. Clone repository
git clone git@github.com:yourusername/fraud-detection.git
cd fraud-detection

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Redis
docker run -d --name redis-fraud-detection -p 6379:6379 redis/redis-stack:latest

# 5. Run tests
python test_redis.py
python test_application.py
```

### Usage

Submit fraud detection request:
```bash
python cli/submit.py --text "Tài khoản của bạn sẽ bị khóa"
```

Check status:
```bash
python cli/check_status.py <application-id>
```

## Architecture
```
User → CLI → FastAPI → Redis Client → Redis Stack
                                        ├── Streams (queue)
                                        ├── JSON (storage)
                                        └── Vector Search (matching)
```

## Week 1 Deliverables

- [x] Redis Stack with Streams, JSON, Vector Search
- [x] FastAPI skeleton
- [x] Redis client wrapper
- [x] Application schema
- [x] CLI tools
- [x] Test suite

## Project Structure
```
fraud-detection/
├── app/
│   ├── config.py          # Configuration
│   ├── redis_client.py    # Redis wrapper
│   └── main.py           # FastAPI app
├── cli/
│   ├── submit.py         # Submit tool
│   └── check_status.py   # Status checker
├── test_redis.py         # Redis tests
├── test_application.py   # Application tests
└── requirements.txt
```

## Next Steps

- Week 2: OCR + DocAuth Agent
- Week 3: Embeddings + TextSimilarity Agent
- Week 4: Final scoring + API endpoints

## Competition

Agentic Startup Arena - December 30, 2025

## Branch: week1-foundation
This branch contains the Week 1 foundation work for review.
# Updated based on feedback
