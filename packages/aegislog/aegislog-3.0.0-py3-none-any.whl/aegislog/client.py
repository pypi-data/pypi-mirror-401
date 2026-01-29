"""
AegisLog Client - Fire-and-Forget Evidence Logging

Usage:
    from aegislog import AegisLog

    log = AegisLog(
        endpoint="https://xxx.execute-api.us-east-1.amazonaws.com/prod",
        tenant_id="my-company"
    )

    # Fire-and-forget: non-blocking, queued for batch upload
    log.record("model_inference", {
        "model_id": "gpt-4",
        "input_tokens": 150,
        "output_tokens": 200,
        "latency_ms": 1234
    })

    # Synchronous: wait for confirmation
    receipt = log.record_sync("critical_decision", {
        "decision_type": "loan_approval",
        "outcome": "approved",
        "confidence": 0.95
    })
    print(receipt.event_id)

    # Async context manager
    async with AegisLogAsync(endpoint="...", tenant_id="...") as log:
        await log.record("event_type", {"data": "value"})
"""

from __future__ import annotations

import atexit
import json
import logging
import queue
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from .exceptions import AegisLogError, AegisLogAPIError

logger = logging.getLogger("aegislog")


@dataclass
class PolicyContext:
    """
    Time Machine Defense: Captures policy state at moment of inference.

    Use this to prove what safety rules were active when an AI decision was made.
    In litigation, this provides cryptographic proof of your 2025 "Standard of Care".

    Args:
        policy_name: Name of the policy/ruleset (e.g., "content_moderation_v2")
        policy_version: Semantic version (e.g., "2.1.0")
        policy_hash: SHA-256 hash of your policy configuration file
    """
    policy_name: Optional[str] = None
    policy_version: Optional[str] = None
    policy_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "policy_name": self.policy_name,
            "policy_version": self.policy_version,
            "policy_hash": self.policy_hash,
        }.items() if v is not None}


@dataclass
class DataProvenance:
    """
    EU AI Act Article 12: Data lineage tracking for traceability.

    Records what data sources were used for an AI inference, enabling
    full audit trail of data usage as required by European AI regulations.

    Args:
        reference_databases: List of RAG/retrieval source identifiers
        training_datasets: List of training data identifiers
        data_version: Version of reference data used
        lineage: Data pipeline lineage URI or identifier
    """
    reference_databases: Optional[list] = None
    training_datasets: Optional[list] = None
    data_version: Optional[str] = None
    lineage: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "reference_databases": self.reference_databases,
            "training_datasets": self.training_datasets,
            "data_version": self.data_version,
            "lineage": self.lineage,
        }.items() if v is not None}


@dataclass
class HumanIntervention:
    """
    EU AI Act Article 14: Human oversight tracking.

    Records when a human reviewed or overrode an AI decision,
    providing audit trail for human-in-the-loop requirements.

    Args:
        required: Whether human review was required for this decision
        reason: Reason for human intervention
        reviewer: Identifier of the human reviewer
        reviewed_at: Unix timestamp of when review occurred
    """
    required: Optional[bool] = None
    reason: Optional[str] = None
    reviewer: Optional[str] = None
    reviewed_at: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "required": self.required,
            "reason": self.reason,
            "reviewer": self.reviewer,
            "reviewed_at": self.reviewed_at,
        }.items() if v is not None}


@dataclass
class ModelContext:
    """
    ISO 42001 / EU AI Act Article 12: Model identification.

    Tracks which AI model made a decision, enabling full traceability
    and model version auditing as required by regulations.

    Args:
        model_id: Unique identifier for the model (e.g., "gpt-4", "risk-model-v2")
        model_version: Semantic version of the model (e.g., "1.0.0", "2024-01-15")
        model_type: Type of model (e.g., "llm", "classifier", "rag", "embedding")
        deployment_id: Optional deployment/environment identifier
    """
    model_id: str
    model_version: str
    model_type: Optional[str] = None
    deployment_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "model_id": self.model_id,
            "model_version": self.model_version,
            "model_type": self.model_type,
            "deployment_id": self.deployment_id,
        }.items() if v is not None}


@dataclass
class SessionContext:
    """
    EU AI Act Article 12: Usage period tracking.

    Records the start and end times of AI system usage sessions,
    as explicitly required by Article 12 for high-risk systems.

    Args:
        session_id: Unique session identifier
        started_at: Unix timestamp when session started
        ended_at: Unix timestamp when session ended (None if ongoing)
    """
    session_id: str
    started_at: int
    ended_at: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
        }.items() if v is not None}


@dataclass
class PerformanceMetrics:
    """
    Post-market monitoring: Performance and anomaly tracking.

    Captures performance metrics and risk flags to support
    post-market monitoring requirements under EU AI Act.

    Args:
        latency_ms: Response latency in milliseconds
        confidence_score: Model confidence (0.0-1.0)
        input_tokens: Number of input tokens processed
        output_tokens: Number of output tokens generated
        anomaly_flags: List of detected anomalies (e.g., ["low_confidence", "drift_detected"])
    """
    latency_ms: Optional[int] = None
    confidence_score: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    anomaly_flags: Optional[list] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "latency_ms": self.latency_ms,
            "confidence_score": self.confidence_score,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "anomaly_flags": self.anomaly_flags,
        }.items() if v is not None}


@dataclass
class Receipt:
    """Evidence receipt from AegisLog."""
    ok: bool
    event_id: str
    trace_id: str
    tenant_id: str
    digest_b64url: str
    signing_alg: str

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> "Receipt":
        return cls(
            ok=data.get("ok", False),
            event_id=data.get("event_id", ""),
            trace_id=data.get("trace_id", ""),
            tenant_id=data.get("tenant_id", ""),
            digest_b64url=data.get("digest_b64url", ""),
            signing_alg=data.get("signing_alg", ""),
        )


@dataclass
class VerificationResult:
    """Verification result from AegisLog."""
    status: str
    event_id: str
    tenant_id: str
    kms_signature_valid: Optional[bool]
    merkle_root: Optional[str]
    verified_at: str

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> "VerificationResult":
        proof = data.get("cryptographic_proof", {})
        linkage = data.get("merkle_linkage") or {}
        event = data.get("event", {})
        return cls(
            status=data.get("status", "unknown"),
            event_id=event.get("event_id", ""),
            tenant_id=event.get("tenant_id", ""),
            kms_signature_valid=proof.get("kms_signature_valid"),
            merkle_root=linkage.get("global_root_hash"),
            verified_at=data.get("verified_at", ""),
        )


class AegisLog:
    """
    Fire-and-Forget Evidence Logger.

    Provides non-blocking evidence collection with background batching.
    All events are cryptographically signed and immutably stored.

    Args:
        endpoint: AegisLog API endpoint (e.g., https://xxx.execute-api.us-east-1.amazonaws.com/prod)
        tenant_id: Your tenant identifier
        api_key: Optional API key for authentication
        batch_size: Number of events to batch before sending (default: 10)
        flush_interval: Seconds between automatic flushes (default: 5.0)
        max_queue_size: Maximum queue size before blocking (default: 1000)
        timeout: HTTP request timeout in seconds (default: 10)
    """

    def __init__(
        self,
        endpoint: str,
        tenant_id: str = "default",
        api_key: Optional[str] = None,
        batch_size: int = 10,
        flush_interval: float = 5.0,
        max_queue_size: int = 1000,
        timeout: int = 10,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.tenant_id = tenant_id
        self.api_key = api_key
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.timeout = timeout

        self._queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._started = False
        self._lock = threading.Lock()

        # Auto-start background worker
        self._start_worker()

        # Register cleanup on exit
        atexit.register(self.close)

    def _start_worker(self) -> None:
        """Start the background worker thread."""
        with self._lock:
            if self._started:
                return
            self._started = True
            self._worker_thread = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name="aegislog-worker"
            )
            self._worker_thread.start()

    def _worker_loop(self) -> None:
        """Background worker that batches and sends events."""
        batch: list = []
        last_flush = time.time()

        while not self._stop_event.is_set():
            try:
                # Wait for events with timeout
                try:
                    event = self._queue.get(timeout=0.1)
                    batch.append(event)
                except queue.Empty:
                    pass

                # Flush if batch is full or interval elapsed
                now = time.time()
                should_flush = (
                    len(batch) >= self.batch_size or
                    (batch and now - last_flush >= self.flush_interval)
                )

                if should_flush:
                    self._send_batch(batch)
                    batch = []
                    last_flush = now

            except Exception as e:
                logger.exception(f"AegisLog worker error: {e}")

        # Final flush on shutdown
        if batch:
            self._send_batch(batch)

    def _send_batch(self, batch: list) -> None:
        """Send a batch of events to the API."""
        for event_data in batch:
            try:
                self._send_single(event_data)
            except Exception as e:
                logger.warning(f"Failed to send event: {e}")

    def _send_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a single event to the API."""
        url = f"{self.endpoint}/ingest"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        body = json.dumps(data).encode("utf-8")
        req = Request(url, data=body, headers=headers, method="POST")

        try:
            with urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            raise AegisLogAPIError(
                f"API error: {e.code}",
                status_code=e.code,
                response={"error": str(e)}
            )
        except URLError as e:
            raise AegisLogAPIError(f"Network error: {e.reason}")

    def record(
        self,
        event_type: str,
        payload: Dict[str, Any],
        trace_id: Optional[str] = None,
        event_id: Optional[str] = None,
        policy_context: Optional[PolicyContext] = None,
        data_provenance: Optional[DataProvenance] = None,
        human_intervention: Optional[HumanIntervention] = None,
        model_context: Optional[ModelContext] = None,
        session_context: Optional[SessionContext] = None,
        performance_metrics: Optional[PerformanceMetrics] = None,
    ) -> str:
        """
        Record an evidence event (fire-and-forget).

        This method is non-blocking. Events are queued and sent in background.

        Args:
            event_type: Type of event (e.g., "model_inference", "decision")
            payload: Event data to record
            trace_id: Optional trace ID for correlation
            event_id: Optional event ID (auto-generated if not provided)
            policy_context: Time Machine Defense - captures policy state at inference
            data_provenance: EU AI Act Article 12 - data lineage tracking
            human_intervention: EU AI Act Article 14 - human oversight tracking
            model_context: ISO 42001 / Article 12 - model identification and versioning
            session_context: Article 12 - usage period tracking (start/end times)
            performance_metrics: Post-market monitoring - latency, confidence, anomaly flags

        Returns:
            The event_id for this record
        """
        event_id = event_id or str(uuid.uuid4())
        trace_id = trace_id or str(uuid.uuid4())

        data = {
            "tenant_id": self.tenant_id,
            "event_type": event_type,
            "event_id": event_id,
            "trace_id": trace_id,
            **payload,
        }

        # Add compliance fields if provided
        if policy_context:
            data["policy_context"] = policy_context.to_dict()
        if data_provenance:
            data["data_provenance"] = data_provenance.to_dict()
        if human_intervention:
            data["human_intervention"] = human_intervention.to_dict()
        if model_context:
            data["model_context"] = model_context.to_dict()
        if session_context:
            data["session_context"] = session_context.to_dict()
        if performance_metrics:
            data["performance_metrics"] = performance_metrics.to_dict()

        try:
            self._queue.put_nowait(data)
        except queue.Full:
            logger.warning("AegisLog queue full, dropping event")

        return event_id

    def record_sync(
        self,
        event_type: str,
        payload: Dict[str, Any],
        trace_id: Optional[str] = None,
        event_id: Optional[str] = None,
        policy_context: Optional[PolicyContext] = None,
        data_provenance: Optional[DataProvenance] = None,
        human_intervention: Optional[HumanIntervention] = None,
        model_context: Optional[ModelContext] = None,
        session_context: Optional[SessionContext] = None,
        performance_metrics: Optional[PerformanceMetrics] = None,
    ) -> Receipt:
        """
        Record an evidence event (synchronous).

        This method blocks until the event is confirmed.

        Args:
            event_type: Type of event
            payload: Event data to record
            trace_id: Optional trace ID
            event_id: Optional event ID
            policy_context: Time Machine Defense - captures policy state at inference
            data_provenance: EU AI Act Article 12 - data lineage tracking
            human_intervention: EU AI Act Article 14 - human oversight tracking
            model_context: ISO 42001 / Article 12 - model identification and versioning
            session_context: Article 12 - usage period tracking (start/end times)
            performance_metrics: Post-market monitoring - latency, confidence, anomaly flags

        Returns:
            Receipt with confirmation details
        """
        event_id = event_id or str(uuid.uuid4())
        trace_id = trace_id or str(uuid.uuid4())

        data = {
            "tenant_id": self.tenant_id,
            "event_type": event_type,
            "event_id": event_id,
            "trace_id": trace_id,
            **payload,
        }

        # Add compliance fields if provided
        if policy_context:
            data["policy_context"] = policy_context.to_dict()
        if data_provenance:
            data["data_provenance"] = data_provenance.to_dict()
        if human_intervention:
            data["human_intervention"] = human_intervention.to_dict()
        if model_context:
            data["model_context"] = model_context.to_dict()
        if session_context:
            data["session_context"] = session_context.to_dict()
        if performance_metrics:
            data["performance_metrics"] = performance_metrics.to_dict()

        response = self._send_single(data)
        return Receipt.from_response(response)

    def verify(self, event_id: str, tenant_id: Optional[str] = None) -> VerificationResult:
        """
        Verify an evidence record.

        Args:
            event_id: The event ID to verify
            tenant_id: Optional tenant ID (defaults to client's tenant_id)

        Returns:
            VerificationResult with cryptographic proof
        """
        tenant = tenant_id or self.tenant_id
        url = f"{self.endpoint}/verify/{event_id}?tenant_id={tenant}"
        headers = {}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        req = Request(url, headers=headers, method="GET")

        try:
            with urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return VerificationResult.from_response(data)
        except HTTPError as e:
            if e.code == 404:
                return VerificationResult(
                    status="not_found",
                    event_id=event_id,
                    tenant_id=tenant,
                    kms_signature_valid=None,
                    merkle_root=None,
                    verified_at="",
                )
            raise AegisLogAPIError(f"Verification failed: {e.code}", status_code=e.code)
        except URLError as e:
            raise AegisLogAPIError(f"Network error: {e.reason}")

    def flush(self) -> None:
        """Force flush all queued events."""
        batch = []
        while True:
            try:
                event = self._queue.get_nowait()
                batch.append(event)
            except queue.Empty:
                break

        if batch:
            self._send_batch(batch)

    def close(self) -> None:
        """Shutdown the client and flush remaining events."""
        self._stop_event.set()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)

    def __enter__(self) -> "AegisLog":
        return self

    def __exit__(self, *args) -> None:
        self.close()


class AegisLogAsync:
    """
    Async Fire-and-Forget Evidence Logger.

    Usage:
        async with AegisLogAsync(endpoint="...", tenant_id="...") as log:
            await log.record("event_type", {"data": "value"})
    """

    def __init__(
        self,
        endpoint: str,
        tenant_id: str = "default",
        api_key: Optional[str] = None,
        timeout: int = 10,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.tenant_id = tenant_id
        self.api_key = api_key
        self.timeout = timeout
        self._session = None

    async def __aenter__(self) -> "AegisLogAsync":
        try:
            import aiohttp
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        except ImportError:
            raise AegisLogError("aiohttp required for async client: pip install aiohttp")
        return self

    async def __aexit__(self, *args) -> None:
        if self._session:
            await self._session.close()

    async def record(
        self,
        event_type: str,
        payload: Dict[str, Any],
        trace_id: Optional[str] = None,
        event_id: Optional[str] = None,
        policy_context: Optional[PolicyContext] = None,
        data_provenance: Optional[DataProvenance] = None,
        human_intervention: Optional[HumanIntervention] = None,
        model_context: Optional[ModelContext] = None,
        session_context: Optional[SessionContext] = None,
        performance_metrics: Optional[PerformanceMetrics] = None,
    ) -> Receipt:
        """
        Record an evidence event asynchronously.

        Args:
            event_type: Type of event
            payload: Event data to record
            trace_id: Optional trace ID
            event_id: Optional event ID
            policy_context: Time Machine Defense - captures policy state at inference
            data_provenance: EU AI Act Article 12 - data lineage tracking
            human_intervention: EU AI Act Article 14 - human oversight tracking
            model_context: ISO 42001 / Article 12 - model identification and versioning
            session_context: Article 12 - usage period tracking (start/end times)
            performance_metrics: Post-market monitoring - latency, confidence, anomaly flags

        Returns:
            Receipt with confirmation details
        """
        if not self._session:
            raise AegisLogError("Client not initialized. Use 'async with' context manager.")

        event_id = event_id or str(uuid.uuid4())
        trace_id = trace_id or str(uuid.uuid4())

        data = {
            "tenant_id": self.tenant_id,
            "event_type": event_type,
            "event_id": event_id,
            "trace_id": trace_id,
            **payload,
        }

        # Add compliance fields if provided
        if policy_context:
            data["policy_context"] = policy_context.to_dict()
        if data_provenance:
            data["data_provenance"] = data_provenance.to_dict()
        if human_intervention:
            data["human_intervention"] = human_intervention.to_dict()
        if model_context:
            data["model_context"] = model_context.to_dict()
        if session_context:
            data["session_context"] = session_context.to_dict()
        if performance_metrics:
            data["performance_metrics"] = performance_metrics.to_dict()

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        url = f"{self.endpoint}/ingest"

        async with self._session.post(url, json=data, headers=headers) as resp:
            if resp.status != 200:
                raise AegisLogAPIError(
                    f"API error: {resp.status}",
                    status_code=resp.status
                )
            response = await resp.json()
            return Receipt.from_response(response)

    async def verify(self, event_id: str, tenant_id: Optional[str] = None) -> VerificationResult:
        """Verify an evidence record asynchronously."""
        if not self._session:
            raise AegisLogError("Client not initialized. Use 'async with' context manager.")

        tenant = tenant_id or self.tenant_id
        url = f"{self.endpoint}/verify/{event_id}?tenant_id={tenant}"

        headers = {}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        async with self._session.get(url, headers=headers) as resp:
            if resp.status == 404:
                return VerificationResult(
                    status="not_found",
                    event_id=event_id,
                    tenant_id=tenant,
                    kms_signature_valid=None,
                    merkle_root=None,
                    verified_at="",
                )
            if resp.status != 200:
                raise AegisLogAPIError(f"Verification failed: {resp.status}", status_code=resp.status)
            data = await resp.json()
            return VerificationResult.from_response(data)
