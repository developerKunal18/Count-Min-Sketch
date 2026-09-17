# Count-Min Sketch

A Flask service demonstrating a Count-Min Sketch for memory-efficient approximate frequency counting.

## Features

- Approximate frequency counting
- Multiple hash rows
- Configurable width and depth
- Batch event ingestion
- Thread-safe updates and reads
- Counter statistics
- Health endpoint
- Pytest test suite

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/events` | Add an event/count |
| POST | `/api/events/batch` | Add multiple events |
| GET | `/api/count/<value>` | Estimate frequency |
| GET | `/api/stats` | Sketch statistics |

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Windows:

```powershell
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Run tests:

```bash
pytest -q
```

## Example

```bash
curl -X POST http://localhost:5000/api/events -H "Content-Type: application/json" -d '{"value":"login","count":5}'
curl http://localhost:5000/api/count/login
```

## Learning Goals

Probabilistic data structures, frequency estimation, hashing collisions, memory-efficient analytics, streaming data, and large-scale counting systems.
