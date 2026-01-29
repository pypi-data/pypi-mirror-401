# AegisLog SDK

[![Tests](https://github.com/prolixo-defense/AegisLog-infra/actions/workflows/test.yml/badge.svg)](https://github.com/prolixo-defense/AegisLog-infra/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/prolixo-defense/AegisLog-infra/graph/badge.svg)](https://codecov.io/gh/prolixo-defense/AegisLog-infra)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fire-and-Forget Evidence Logging for EU AI Act Compliance.

## Installation

```bash
pip install aegislog

# For async support
pip install aegislog[async]
```

## Quick Start

```python
from aegislog import AegisLog

# Initialize client
log = AegisLog(
    endpoint="https://xxx.execute-api.us-east-1.amazonaws.com/prod",
    tenant_id="my-company",
    api_key="your-api-key"
)

# Fire-and-forget (non-blocking)
event_id = log.record("model_inference", {
    "model_id": "gpt-4",
    "input_tokens": 150,
    "output_tokens": 200,
    "latency_ms": 1234
})

# Synchronous (blocking, returns receipt)
receipt = log.record_sync("critical_decision", {
    "decision_type": "loan_approval",
    "outcome": "approved",
    "confidence": 0.95
})
print(f"Recorded: {receipt.event_id}")
print(f"Digest: {receipt.digest_b64url}")

# Verify evidence
result = log.verify(event_id)
print(f"Status: {result.status}")
print(f"KMS Signature Valid: {result.kms_signature_valid}")
```

## EU AI Act Compliance Features

AegisLog provides built-in support for EU AI Act Articles 12 and 14 compliance through structured schema objects.

### Time Machine Defense (PolicyContext)

Capture the exact policy/ruleset active at the moment of inference. If sued in 2028 for a decision made in 2025, you can cryptographically prove what "Standard of Care" was in effect.

```python
from aegislog import AegisLog, PolicyContext
import hashlib

# Hash your policy configuration file
with open("policies/content_moderation.yaml", "rb") as f:
    policy_hash = hashlib.sha256(f.read()).hexdigest()

log = AegisLog(endpoint="...", tenant_id="...", api_key="...")

receipt = log.record_sync(
    "content_moderation",
    {"input": "user message", "output": "response", "flagged": False},
    policy_context=PolicyContext(
        policy_name="content_moderation_rules",
        policy_version="2.1.0",
        policy_hash=f"sha256:{policy_hash}"
    )
)
```

### Data Provenance (EU AI Act Article 12)

Track what data sources were used for an AI inference, enabling full audit trail as required by European AI regulations.

```python
from aegislog import AegisLog, DataProvenance

log = AegisLog(endpoint="...", tenant_id="...", api_key="...")

# RAG-based inference with data lineage
receipt = log.record_sync(
    "rag_inference",
    {
        "query": "What is the return policy?",
        "response": "Our return policy allows...",
        "sources_used": 3
    },
    data_provenance=DataProvenance(
        reference_databases=["knowledge-base-v3", "product-catalog-2026"],
        data_version="2026-01-11",
        lineage="s3://data-lake/processed/kb-v3/"
    )
)
```

### Human Intervention (EU AI Act Article 14)

Record when humans review or override AI decisions for human-in-the-loop compliance.

```python
from aegislog import AegisLog, HumanIntervention
import time

log = AegisLog(endpoint="...", tenant_id="...", api_key="...")

# AI decision that required human review
receipt = log.record_sync(
    "loan_decision",
    {
        "applicant_id": "A123456",
        "ai_recommendation": "approve",
        "final_decision": "approve",
        "loan_amount": 50000
    },
    human_intervention=HumanIntervention(
        required=True,
        reason="Loan amount exceeds $25,000 threshold",
        reviewer="loan_officer_42",
        reviewed_at=int(time.time())
    )
)
```

### Model Context (ISO 42001 / Article 12)

Track which AI model made a decision, enabling full traceability and model version auditing.

```python
from aegislog import AegisLog, ModelContext

log = AegisLog(endpoint="...", tenant_id="...", api_key="...")

receipt = log.record_sync(
    "classification",
    {"input": "customer inquiry", "output": "billing", "score": 0.95},
    model_context=ModelContext(
        model_id="intent-classifier-v2",
        model_version="2.3.1",
        model_type="classifier",
        deployment_id="prod-us-east-1"
    )
)
```

### Session Context (Article 12 Usage Periods)

Record start and end times of AI system usage sessions, as explicitly required by Article 12.

```python
from aegislog import AegisLog, SessionContext
import time

log = AegisLog(endpoint="...", tenant_id="...", api_key="...")

session_start = int(time.time())
# ... AI system processes requests ...
session_end = int(time.time())

receipt = log.record_sync(
    "session_complete",
    {"requests_processed": 47, "errors": 0},
    session_context=SessionContext(
        session_id="sess_abc123",
        started_at=session_start,
        ended_at=session_end
    )
)
```

### Performance Metrics (Post-Market Monitoring)

Capture performance metrics and anomaly flags for post-market monitoring requirements.

```python
from aegislog import AegisLog, PerformanceMetrics

log = AegisLog(endpoint="...", tenant_id="...", api_key="...")

receipt = log.record_sync(
    "inference",
    {"input": "What is the weather?", "output": "The weather is sunny."},
    performance_metrics=PerformanceMetrics(
        latency_ms=234,
        confidence_score=0.92,
        input_tokens=8,
        output_tokens=6,
        anomaly_flags=["high_latency"]  # Optional: flags for anomalies
    )
)
```

### Full Compliance Example

Combine all compliance features for maximum legal protection:

```python
from aegislog import (
    AegisLog,
    PolicyContext,
    DataProvenance,
    HumanIntervention,
    ModelContext,
    SessionContext,
    PerformanceMetrics
)
import hashlib
import time

log = AegisLog(
    endpoint="https://60yvfcmx35.execute-api.us-east-1.amazonaws.com/prod",
    tenant_id="my-company",
    api_key="your-api-key"
)

# Full compliance record for high-stakes AI decision
receipt = log.record_sync(
    "high_risk_ai_decision",
    {
        "input": {"customer_id": "C789", "request_type": "credit_increase"},
        "output": {"approved": True, "new_limit": 10000}
    },
    # Time Machine Defense
    policy_context=PolicyContext(
        policy_name="credit_risk_policy",
        policy_version="4.2.1",
        policy_hash="sha256:e3b0c44298fc1c149afbf4c8996fb924..."
    ),
    # EU AI Act Article 12 - Data Traceability
    data_provenance=DataProvenance(
        reference_databases=["credit-bureau-experian", "transaction-history"],
        training_datasets=["risk-model-training-2025-q4"],
        data_version="2026-01-11",
        lineage="mlflow://experiments/risk-v4/run-123"
    ),
    # EU AI Act Article 14 - Human Oversight
    human_intervention=HumanIntervention(
        required=False  # No human review needed for this decision
    ),
    # ISO 42001 / Article 12 - Model Identification
    model_context=ModelContext(
        model_id="risk-assessment-v4",
        model_version="4.2.0",
        model_type="classifier",
        deployment_id="prod-us-east-1"
    ),
    # Article 12 - Usage Period Tracking
    session_context=SessionContext(
        session_id="sess_credit_review_123",
        started_at=int(time.time()) - 60,
        ended_at=int(time.time())
    ),
    # Post-Market Monitoring
    performance_metrics=PerformanceMetrics(
        latency_ms=234,
        confidence_score=0.89,
        input_tokens=150,
        output_tokens=50
    )
)

print(f"Evidence ID: {receipt.event_id}")
print(f"Cryptographic Digest: {receipt.digest_b64url}")
```

### Verification with Compliance Check

When you verify an event, the response includes detailed compliance status:

```python
result = log.verify(receipt.event_id)

# The API response includes:
# {
#   "status": "verified",
#   "compliance": {
#     "eu_ai_act_article_12": true,
#     "eu_ai_act_article_14_human_oversight": false,
#     "time_machine_defense": true,
#     "full_traceability": true,
#     "immutable_record": true,
#     "non_repudiation": true,
#     "fields_present": {
#       "policy_context": {"policy_hash": true, "policy_version": true},
#       "data_provenance": {"reference_databases": true, ...},
#       "human_intervention": {"required": true, "reviewer": false}
#     }
#   }
# }
```

## Async Usage

```python
import asyncio
from aegislog import AegisLogAsync, PolicyContext, DataProvenance

async def main():
    async with AegisLogAsync(
        endpoint="https://xxx.execute-api.us-east-1.amazonaws.com/prod",
        tenant_id="my-company",
        api_key="your-api-key"
    ) as log:
        receipt = await log.record(
            "model_inference",
            {"model_id": "claude-3", "tokens": 500},
            policy_context=PolicyContext(
                policy_name="inference_rules",
                policy_version="1.0.0",
                policy_hash="sha256:abc123..."
            ),
            data_provenance=DataProvenance(
                reference_databases=["docs-v2"],
                data_version="2026-01-11"
            )
        )
        print(f"Event ID: {receipt.event_id}")

asyncio.run(main())
```

## Decorator Pattern (Coming Soon)

```python
from aegislog import aegislog_trace

@aegislog_trace(
    policy_name="inference_policy",
    policy_version="1.0.0"
)
def my_ai_function(input_text: str) -> str:
    # Your AI logic here
    return result
```

## Features

- **Fire-and-Forget**: Non-blocking logging with background batching
- **Cryptographic Proof**: ECDSA P-256 signatures via AWS KMS (HSM-backed)
- **Merkle Tree Integrity**: Daily aggregation with signed roots
- **Time Machine Defense**: Policy snapshots for future litigation protection
- **EU AI Act Compliant**: Articles 12 (traceability) and 14 (human oversight)
- **Zero Dependencies**: Core SDK uses only Python stdlib
- **Async Support**: Optional aiohttp for async operations

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `endpoint` | Required | AegisLog API endpoint |
| `tenant_id` | `"default"` | Your tenant identifier |
| `api_key` | `None` | API key for authentication |
| `batch_size` | `10` | Events per batch |
| `flush_interval` | `5.0` | Seconds between flushes |
| `max_queue_size` | `1000` | Max queue before blocking |
| `timeout` | `10` | HTTP timeout in seconds |

## Compliance Schema Reference

### PolicyContext

| Field | Type | Description |
|-------|------|-------------|
| `policy_name` | `str` | Name of the policy/ruleset |
| `policy_version` | `str` | Semantic version (e.g., "2.1.0") |
| `policy_hash` | `str` | SHA-256 hash of policy config file |

### DataProvenance

| Field | Type | Description |
|-------|------|-------------|
| `reference_databases` | `list[str]` | RAG/retrieval source identifiers |
| `training_datasets` | `list[str]` | Training data identifiers |
| `data_version` | `str` | Version of reference data |
| `lineage` | `str` | Data pipeline URI (S3, MLflow, etc.) |

### HumanIntervention

| Field | Type | Description |
|-------|------|-------------|
| `required` | `bool` | Whether human review was required |
| `reason` | `str` | Reason for human intervention |
| `reviewer` | `str` | Identifier of human reviewer |
| `reviewed_at` | `int` | Unix timestamp of review |

### ModelContext

| Field | Type | Description |
|-------|------|-------------|
| `model_id` | `str` | **Required.** Unique identifier for the model |
| `model_version` | `str` | **Required.** Semantic version of the model |
| `model_type` | `str` | Type of model (llm, classifier, rag, embedding) |
| `deployment_id` | `str` | Deployment/environment identifier |

### SessionContext

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | `str` | **Required.** Unique session identifier |
| `started_at` | `int` | **Required.** Unix timestamp when session started |
| `ended_at` | `int` | Unix timestamp when session ended (None if ongoing) |

### PerformanceMetrics

| Field | Type | Description |
|-------|------|-------------|
| `latency_ms` | `int` | Response latency in milliseconds |
| `confidence_score` | `float` | Model confidence (0.0-1.0) |
| `input_tokens` | `int` | Number of input tokens processed |
| `output_tokens` | `int` | Number of output tokens generated |
| `anomaly_flags` | `list[str]` | Detected anomalies (e.g., "low_confidence", "drift_detected") |

## Context Manager

```python
with AegisLog(endpoint="...", tenant_id="...", api_key="...") as log:
    log.record("event", {"data": "value"})
# Automatically flushes on exit
```

## Best Practices

1. **Always include PolicyContext** for high-risk AI decisions
2. **Hash your policy files** and store the hash with each inference
3. **Track data provenance** for RAG and retrieval-augmented systems
4. **Record human interventions** with reviewer IDs and timestamps
5. **Use `record_sync()`** for critical decisions that need confirmation
6. **Use `record()`** (fire-and-forget) for high-volume, non-critical logging

## License

MIT
