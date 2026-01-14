# Architecture

X-Ray is a decision-reasoning observability system for multi-step pipelines. It captures **why** decisions were made (candidates, filters, scores, reasoning), not just what functions ran.

## Database Schema

[View interactive diagram on dbdiagram.io](https://dbdiagram.io/d/XRAY-DIAGRAM-6960bf2fd6e030a0248dae71)

![XRAY DIAGRAM](https://private-user-images.githubusercontent.com/83394682/401589006-f68d05ce-85f6-499c-8f5c-8c5b35a42cb8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzY0NTY2MjUsIm5iZiI6MTczNjQ1NjMyNSwicGF0aCI6Ii84MzM5NDY4Mi80MDE1ODkwMDYtZjY4ZDA1Y2UtODVmNi00OTljLThmNWMtOGM1YjM1YTQyY2I4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAxMDklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMTA5VDE4MTg0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWVmMDFlNjY2ZmQxMTI0NmY5ZTY3M2JhNzlkNjEwNjZkYzYzZDQxMGY4NTQ5MDg0ZGQwMjNhY2JmN2VkNGQxNzcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.aE-mIQe-SYMBxfqDKsFpVJrGdwh27WzgB5gMtK_bJmw)

### Tables

| Table | Purpose |
|-------|---------|
| **Run** | Pipeline execution (id, pipeline_name, status, timestamps, metadata) |
| **Step** | Single processing step within a run (input/output counts, reasoning, timing) |
| **Payload** | Externalized large data (lists >100 items, strings >2KB) |

### Computed Fields

- `removed_ratio` = `(input_count - output_count) / input_count` — computed at query time
- `duration_ms` — stored in Step, computed at step end in SDK

---

## Data Flow

```
User Code → @step decorator → XRayClient → Transport (async buffer) → HTTP POST → API → DB
```

![Externalization Flow](https://private-user-images.githubusercontent.com/83394682/401589082-d26e08c8-baa4-4fbc-b16e-5a4d9f10f5b7.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzY0NTY2MjUsIm5iZiI6MTczNjQ1NjMyNSwicGF0aCI6Ii84MzM5NDY4Mi80MDE1ODkwODItZDI2ZTA4YzgtYmFhNC00ZmJjLWIxNmUtNWE0ZDlmMTBmNWI3LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAxMDklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMTA5VDE4MTg0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMxZTIwOWY3MTI2OGE1ZjgyNmJmZjRlZWYyMDE5YjVhMTE5NDc4NzA1OTA0NTRlODRiNGE4ZjJiYjMxZjRkMzMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.n8wKWKLW3nFnNJcMNNTb_z3aeqvxsQRYy-u1Sng86wU)

---

## Type System

### Enums (shared between SDK & API)

Located in `shared/types.py`:

**StepType**
| Value | Description |
|-------|-------------|
| `filter` | Removes candidates by criteria |
| `rank` | Orders candidates by score |
| `llm` | LLM/AI model call |
| `retrieval` | Fetches external data |
| `transform` | Data format changes |
| `other` | Catch-all |

**RunStatus / StepStatus**: `running`, `success`, `error`

**DetailLevel**: `summary` (counts + samples), `full` (complete data with truncation)

---

## SDK Components

### XRayClient
Entry point for the SDK. Manages Transport lifecycle and provides `start_run()` context manager.

```python
client = init_xray(XRayConfig(base_url="http://localhost:8000"))
with client.start_run("pipeline") as run:
    # Steps created here
```

### Run
Represents a pipeline execution. Creates Steps, manages context via `contextvars`.

### Step
Single processing step. Captures input/output, timing, and reasoning.

### Transport
Async buffered HTTP sender with **fail-open** semantics—network errors are logged but never crash the application.

### Decorators
- `@step(name, step_type)` — Instrument a function
- `@instrument_class(step_type)` — Instrument all public methods of a class
- `attach_reasoning(data)` — Add reasoning to current step
- `attach_candidates(candidates)` — Add candidate list to current step

---

## Payload Summarization

Large data is automatically summarized to keep event sizes manageable:

| Data Type | Threshold | Behavior |
|-----------|-----------|----------|
| Lists | < 100 items | Stored inline |
| Lists | ≥ 100 items | Externalized with preview |
| Strings | < 2KB | Stored inline |
| Strings | ≥ 2KB | Externalized with preview |
| Candidate lists | Any size | Always inline (id + score + reason only) |

### Externalization Flow

1. SDK `summarize_payload()` detects large data
2. Creates reference: `{"_ref": "p-000", "_type": "list", "_count": 500, "_preview": [...]}`
3. Event includes `_payloads: {"p-000": [full data]}`
4. API extracts payloads, stores in Payload table
5. Step stores summary only; Payload stores full data

---

## Event Types

### run_start / run_end
```json
{
  "event_type": "run_start",
  "id": "uuid",
  "pipeline_name": "my-pipeline",
  "status": "running",
  "started_at": "2024-01-01T00:00:00Z",
  "input_summary": {...},
  "metadata": {"user_id": "123"},
  "_payloads": {...}
}
```

### step_start / step_end
```json
{
  "event_type": "step_end",
  "id": "uuid",
  "run_id": "parent-run-uuid",
  "step_name": "filter_candidates",
  "step_type": "filter",
  "status": "success",
  "duration_ms": 150,
  "input_count": 100,
  "output_count": 25,
  "reasoning": {"threshold": 0.7, "removed": 75},
  "_payloads": null
}
```

---

## Configuration

### SDK (`xray.config.yaml`)
```yaml
sdk:
  base_url: http://localhost:8000
  api_key: your-api-key          # Optional
  buffer_size: 1000              # Max events to buffer
  flush_interval: 5.0            # Seconds between flushes
  default_detail: summary        # summary | full
```

### API
```yaml
api:
  database_url: postgresql+asyncpg://localhost:5432/xray
  debug: false
```

Config discovery searches upward from current directory for `xray.config.yaml`.

---

## Key Design Decisions

1. **Counts as columns** — `input_count`/`output_count` are indexed for efficient filtering
2. **Computed ratios** — `removed_ratio` computed at query time (allows formula changes)
3. **Payload externalization** — Large data stored separately, summaries inline
4. **Candidate preservation** — All candidate IDs captured, never truncated
5. **Fail-open SDK** — Network errors never crash the application
6. **Context managers** — Automatic cleanup on exceptions

---

## Project Structure

```
xray-logger/
├── shared/
│   ├── types.py          # StepType, RunStatus, DetailLevel
│   └── config.py         # Config discovery
├── sdk/
│   ├── client.py         # XRayClient, init_xray()
│   ├── run.py            # Run class
│   ├── step.py           # Step, PayloadCollector, summarize_payload()
│   ├── transport.py      # Async HTTP transport
│   ├── decorators.py     # @step, @instrument_class
│   ├── middleware.py     # FastAPI/Starlette middleware
│   └── config.py         # XRayConfig
├── api/
│   ├── main.py           # FastAPI app
│   ├── routes.py         # /ingest, /xray/runs, /xray/steps
│   ├── models.py         # SQLAlchemy ORM (Run, Step, Payload)
│   ├── schemas.py        # Pydantic schemas
│   ├── store.py          # Database operations
│   └── config.py         # APIConfig
└── examples/
    ├── competitor_pipeline/    # RAG pipeline example
    └── fastapi-middleware/     # HTTP instrumentation example
```
