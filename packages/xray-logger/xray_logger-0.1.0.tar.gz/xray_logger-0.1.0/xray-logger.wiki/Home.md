# X-Ray Logger

**Decision-level observability for ML/LLM pipelines.**

X-Ray captures *why* decisions were made—candidates considered, filters applied, scores computed, and reasoning behind each step—not just what functions ran.

## Getting Started

**[Quick Start Guide](./Quick-Start)** - Get running in 5 minutes

## Documentation

| Page | Description |
|------|-------------|
| [Quick Start](./Quick-Start) | Installation and first pipeline |
| [Architecture](./Architecture) | System design, data flow, and internals |

## Quick Links

- [GitHub Repository](https://github.com/mohit-nagaraj/xray-logger)
- [PyPI Package](https://pypi.org/project/xray-logger/)
- [Docker Image](https://ghcr.io/mohit-nagaraj/xray-logger)
- [Examples](https://github.com/mohit-nagaraj/xray-logger/tree/main/examples)

## Key Features

- **Decision Transparency** - Capture candidates, scores, and reasoning
- **Lightweight SDK** - Simple decorators, fail-open design
- **FastAPI Middleware** - Automatic HTTP instrumentation
- **PostgreSQL/SQLite** - Flexible storage options
- **Query API** - Filter and analyze pipeline runs
