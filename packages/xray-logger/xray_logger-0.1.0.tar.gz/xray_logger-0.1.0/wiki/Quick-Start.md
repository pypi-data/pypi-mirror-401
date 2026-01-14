# Quick Start Guide

Get X-Ray Logger running in under 5 minutes.

## Prerequisites

- Docker (for the server)
- Python 3.12+ (for the SDK)

---

## Step 1: Start the X-Ray Server

### Option A: Docker (Simplest)

```bash
docker run -d \
  --name xray-api \
  -p 8000:8000 \
  -e XRAY_DATABASE_URL=sqlite+aiosqlite:///./data/xray.db \
  -v xray-data:/app/data \
  ghcr.io/mohit-nagaraj/xray-logger:latest
```

Verify it's running:
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### Option B: Docker Compose (With PostgreSQL)

```bash
git clone https://github.com/mohit-nagaraj/xray-logger.git
cd xray-logger
cp .env.example .env
docker-compose up -d
```

---

## Step 2: Install the SDK

```bash
pip install xray-logger
```

---

## Step 3: Instrument Your First Pipeline

Create a file `example.py`:

```python
from xray_logger import init_xray, step, attach_reasoning

# Connect to X-Ray server
client = init_xray(base_url="http://localhost:8000")

@step(step_type="filter")
def filter_products(products, min_price=10):
    """Filter products below minimum price."""
    result = [p for p in products if p["price"] >= min_price]

    attach_reasoning({
        "min_price": min_price,
        "input_count": len(products),
        "output_count": len(result),
        "filtered_out": len(products) - len(result)
    })

    return result

@step(step_type="rank")
def rank_by_rating(products):
    """Rank products by rating descending."""
    ranked = sorted(products, key=lambda p: p["rating"], reverse=True)

    attach_reasoning({
        "algorithm": "rating_desc",
        "top_product": ranked[0] if ranked else None
    })

    return ranked

# Sample data
products = [
    {"id": 1, "name": "Widget A", "price": 25, "rating": 4.5},
    {"id": 2, "name": "Widget B", "price": 5, "rating": 4.8},
    {"id": 3, "name": "Widget C", "price": 15, "rating": 3.9},
    {"id": 4, "name": "Widget D", "price": 30, "rating": 4.2},
]

# Run pipeline with X-Ray tracking
with client.start_run("product-recommendation", input_data={"user": "demo"}):
    filtered = filter_products(products, min_price=10)
    ranked = rank_by_rating(filtered)
    print(f"Top recommendation: {ranked[0]['name']}")

# Graceful shutdown
from xray_logger import shutdown_xray
shutdown_xray()
```

Run it:
```bash
python example.py
# Output: Top recommendation: Widget A
```

---

## Step 4: View Your Data

### List all runs
```bash
curl http://localhost:8000/xray/runs
```

### Get a specific run with steps
```bash
curl http://localhost:8000/xray/runs/{run_id}
```

### Query filter steps across all runs
```bash
curl "http://localhost:8000/xray/steps?step_type=filter"
```

---

## Configuration Options

### Using a Config File

Create `xray.config.yaml` in your project root:

```yaml
sdk:
  base_url: http://localhost:8000
  api_key: your-secret-key       # Optional
  buffer_size: 1000              # Events to buffer before flush
  flush_interval: 5.0            # Seconds between auto-flushes
  default_detail: summary        # summary | full
```

Then in your code:
```python
from xray_logger import init_xray, load_config

config = load_config()  # Auto-discovers xray.config.yaml
client = init_xray(config)
```

### Programmatic Configuration

```python
from xray_logger import init_xray, XRayConfig

client = init_xray(XRayConfig(
    base_url="http://localhost:8000",
    api_key="your-secret-key",
    buffer_size=500,
    flush_interval=2.0,
))
```

---

## FastAPI Integration

For web applications, use the middleware for automatic request instrumentation:

```python
from fastapi import FastAPI
from xray_logger import init_xray
from xray_logger.middleware import XRayMiddleware

app = FastAPI()

# Initialize on startup
@app.on_event("startup")
async def startup():
    init_xray(base_url="http://localhost:8000")

# Add middleware
app.add_middleware(XRayMiddleware)

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    # current_run() is automatically available
    # Use @step decorators in your business logic
    return {"recommendations": [...]}
```

---

## Available Step Types

| Type | When to Use |
|------|-------------|
| `filter` | Removing items based on criteria |
| `rank` | Sorting/ordering items by score |
| `llm` | LLM/AI model calls |
| `retrieval` | Fetching data (vector search, API calls, DB queries) |
| `transform` | Data format changes, enrichment |
| `other` | Anything else |

---

## Next Steps

- [Architecture](./Architecture) - Deep dive into how X-Ray works
- [Examples](https://github.com/mohit-nagaraj/xray-logger/tree/main/examples) - Full example pipelines
- [API Reference](./API-Reference) - Complete endpoint documentation

---

## Troubleshooting

### SDK not sending data?

1. Check server is running: `curl http://localhost:8000/health`
2. Ensure `shutdown_xray()` is called before exit (flushes buffer)
3. Check logs for connection errors

### High memory usage?

Reduce buffer size:
```python
client = init_xray(XRayConfig(base_url="...", buffer_size=100))
```

### Need API authentication?

Set `XRAY_API_KEY` on the server:
```bash
docker run -e XRAY_API_KEY=your-secret-key ...
```

And in SDK config:
```yaml
sdk:
  api_key: your-secret-key
```
