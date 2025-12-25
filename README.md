# Kasparro Backend & ETL System

This project implements a production-grade backend and ETL system designed to ingest,
normalize, store, and serve cryptocurrency market data from multiple heterogeneous sources.

The system is fully Dockerized, cloud-deployable, and designed with reliability,
observability, and recoverability in mind.

---

## High-Level Architecture

The system consists of the following components:

- Data ingestion layer (CoinGecko, CoinPaprika)
- ETL processing & normalization layer
- PostgreSQL storage using JSONB
- FastAPI backend service
- Dockerized runtime environment
- Cloud deployment with scheduled ETL execution

---

## Data Sources

### CoinGecko
- Endpoint: `/coins/markets`
- Pricing field: `current_price`
- No authentication required

### CoinPaprika
- Endpoint: `/v1/tickers`
- Pricing field: `quotes.USD.price`
- API key authentication via Authorization header

Each source has a different schema and nesting structure, which is handled explicitly
during normalization.

---

## Unified Data Model

All ingested assets are normalized into the following unified schema:

- asset_id (string)
- name (string)
- symbol (string)
- price_usd (float)
- source (string)

Raw source payloads are stored as JSONB in PostgreSQL for flexibility and traceability.

---

## Database Design

### raw_assets
Stores normalized asset records.

- id (TEXT, PRIMARY KEY)
- data (JSONB)

Idempotent inserts ensure no duplicate processing:
ON CONFLICT (id) DO NOTHING

### etl_runs
Tracks ETL execution metadata.

- run_id (UUID)
- source (TEXT)
- started_at (TIMESTAMP)
- finished_at (TIMESTAMP)
- status (TEXT)
- records_processed (INT)

---

## ETL Pipeline

1. Fetch raw data from each source
2. Validate and normalize using Pydantic
3. Perform source-aware price extraction
4. Insert data idempotently into PostgreSQL
5. Log execution metrics and errors

ETL can be triggered:
- Automatically (via cron)
- Manually via API endpoint

---

## API Endpoints

### GET /health
Returns system health status.

Example response:
{
  "db": "ok",
  "etl": "running"
}

---

### GET /data
Returns paginated asset data.

Query parameters:
- limit
- offset

Response includes request metadata.

---

### POST /etl/run
Manually triggers ETL execution.

Used for recovery, debugging, and reprocessing.

---

## Authentication & Security

- API keys are provided via environment variables
- No secrets are hard-coded
- `.env` files are excluded from version control

---

## Docker Usage

### Build and Run
docker compose up --build

### Stop
docker compose down

The system automatically initializes the database schema and exposes API endpoints.

---

## Cloud Deployment

The system is deployed on a cloud VM using Docker.

Features:
- Public API endpoint
- Scheduled ETL execution using cron
- Logs accessible via cloud console
- Fully reproducible from Docker image

---

## Testing

Automated tests cover:
- ETL normalization logic
- Incremental ingestion
- API correctness
- Failure recovery scenarios

Tests are implemented using pytest and can be run via:
make test

---

## Design Decisions & Tradeoffs

- JSONB storage allows flexible schema evolution
- Source-aware normalization avoids brittle assumptions
- Manual ETL trigger enables recovery and observability
- Docker-first design ensures portability

---

## How to Run Locally

1. Clone repository
2. Run:
   docker compose up --build
3. Access API at:
   http://localhost:8000

---

## Author

Yuvraj Singh
