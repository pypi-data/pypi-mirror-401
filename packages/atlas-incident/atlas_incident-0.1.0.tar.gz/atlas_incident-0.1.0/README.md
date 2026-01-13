# ATLAS — Deterministic Incident Analysis & Root Cause System

ATLAS is a **production‑grade, deterministic incident analysis system** designed for SREs and DevOps engineers.
It analyzes real production logs, classifies incidents, determines root cause, and suggests concrete actions — **without AI, ML, or probabilistic logic**.

> Built for 3‑AM incidents. Explainable, testable, and deployable today.

---

## Why ATLAS?

Most incident tools rely on black‑box AI or heuristics that cannot be trusted under pressure. ATLAS takes the opposite approach:

* 🔒 **Zero‑AI** (no LLMs, no ML, no embeddings)
* 🧠 **Fully deterministic** (same input → same output)
* 🧾 **Explainable decisions** (rule‑based logic)
* 🧪 **100% testable** core pipeline
* ⚙️ **Real‑world workflow** (file‑based CLI + JSON output)

---

## What ATLAS Does

1. Parses raw production logs
2. Normalizes them into a canonical incident schema
3. Classifies the incident (DB, Network, Auth, etc.)
4. Infers probable root cause via rule chains
5. Suggests concrete remediation actions
6. Persists incident history for audit & comparison

---

## High‑Level Architecture

```mermaid
flowchart TD
    A[Log File] --> B[Log Parsing Engine]
    B --> C[Incident Normalization]
    C --> D[Rule‑Based Classification]
    D --> E[Root Cause Analysis]
    E --> F[Recommendation Engine]
    F --> G[Final JSON Report]
    G --> H[Incident History (JSONL)]
```

---

## Directory Structure

```text
atlas/
├── atlas/
│   ├── cli/              # CLI entry point (file‑based)
│   ├── parsing/          # Log parsing engine
│   ├── normalization/    # Incident normalization
│   ├── classification/   # Rule‑based classifier
│   ├── rca/              # Root cause analysis engine
│   ├── recommendations/ # Action / remediation engine
│   ├── history/          # Incident persistence (JSONL)
│   ├── orchestrator/     # Pipeline orchestration
│   ├── io/               # JSON I/O helpers
│   ├── schemas/          # Shared data contracts
│   └── __main__.py       # `python -m atlas`
│
├── tests/                # pytest test suite
├── output/               # Generated reports
├── incident_history.jsonl   # Append‑only incident history
├── README.md
└── pyproject.toml
```

---

## Installation

```bash
python3 -m venv env
source env/bin/activate
```

(Only `pytest` is required for testing.)

---

## Usage (Real‑World Workflow)

### 1️⃣ Create a production‑like log file

```text
2024-10-12T09:14:01Z INFO  payments-api Starting service
2024-10-12T09:14:05Z INFO  payments-api Connected to postgres
2024-10-12T09:15:22Z WARN  payments-api Slow query detected
2024-10-12T09:16:10Z ERROR payments-api Database connection timeout
2024-10-12T09:16:15Z ERROR payments-api Retries exhausted
```

### 2️⃣ Run ATLAS

```bash
python -m atlas prod_payments.log payments-api prod
```

### 3️⃣ Example Output (JSON)

```json
{
  "service": "payments-api",
  "environment": "prod",
  "severity": "HIGH",
  "category": "DATABASE",
  "root_cause": "Connection pool exhausted",
  "actions": [
    "Increase database connection pool size",
    "Restart affected service",
    "Monitor latency for 15 minutes"
  ],
  "confidence": 1.0
}
```

---

## Incident History (Persistence)

Each run is appended to `incident_history.jsonl`:

```json
{"service":"payments-api","environment":"prod","severity":"HIGH","category":"DATABASE","root_cause":"Connection pool exhausted",...}
```

* Append‑only
* Audit‑friendly
* Replayable for future analysis

---

## Testing

Run the full test suite:

```bash
pytest -v
```

All core modules are covered with deterministic tests.

---

## Design Principles

* Determinism over intelligence
* Rules over models
* Schemas over guesses
* Clarity over cleverness
* Production realism over demos

---


## License

MIT
