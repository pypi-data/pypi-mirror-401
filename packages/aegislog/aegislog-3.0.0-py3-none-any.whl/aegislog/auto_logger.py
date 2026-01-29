"""
AegisLog Auto-Logger
====================
Automatic evidence logging for AI API calls.

Wraps OpenAI and Anthropic clients to transparently capture all
AI interactions as cryptographic evidence.

Usage:
    from aegislog.auto_logger import wrap_openai, wrap_anthropic

    # OpenAI
    from openai import OpenAI
    client = wrap_openai(OpenAI(), tenant_id="my-company", api_key="aegislog-...")

    # Use normally - all calls are automatically logged
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(f"Evidence ID: {response._aegislog_event_id}")

    # Anthropic
    import anthropic
    client = wrap_anthropic(anthropic.Anthropic(), tenant_id="my-company", api_key="aegislog-...")

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(f"Evidence ID: {message._aegislog_event_id}")
"""

from __future__ import annotations

import json
import time
import hashlib
import urllib.request
import ssl
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, Optional, List
from dataclasses import dataclass, field
import threading
import queue


@dataclass
class AegisLogConfig:
    """Configuration for auto-logging."""
    endpoint: str = "https://60yvfcmx35.execute-api.us-east-1.amazonaws.com/prod"
    tenant_id: str = "aegislog"
    api_key: str = ""

    # Logging options
    log_prompts: bool = True  # Log full prompts (disable for privacy)
    log_responses: bool = True  # Log full responses
    max_content_length: int = 10000  # Truncate long content

    # Policy context (for Time Machine Defense)
    policy_name: Optional[str] = None
    policy_version: Optional[str] = None
    policy_hash: Optional[str] = None

    # Data provenance (for EU AI Act Article 12)
    reference_databases: List[str] = field(default_factory=list)

    # Async logging (non-blocking)
    async_logging: bool = True

    # Debug mode
    debug: bool = False


class AsyncLogger:
    """Background thread for non-blocking evidence logging."""

    def __init__(self, config: AegisLogConfig):
        self.config = config
        self.queue: queue.Queue = queue.Queue()
        self.thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._start_worker()

    def _start_worker(self):
        """Start background worker thread."""
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        """Background worker that processes the logging queue."""
        ctx = ssl.create_default_context()

        while not self._stop_event.is_set():
            try:
                payload = self.queue.get(timeout=1)
                if payload is None:
                    break

                self._send_evidence(payload, ctx)

            except queue.Empty:
                continue
            except Exception as e:
                if self.config.debug:
                    print(f"[AegisLog] Async logging error: {e}")

    def _send_evidence(self, payload: dict, ctx: ssl.SSLContext) -> Optional[str]:
        """Send evidence to AegisLog API."""
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{self.config.endpoint}/ingest",
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "X-Api-Key": self.config.api_key
                }
            )

            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                if self.config.debug:
                    print(f"[AegisLog] Evidence recorded: {result.get('event_id')}")
                return result.get('event_id')

        except Exception as e:
            if self.config.debug:
                print(f"[AegisLog] Failed to record evidence: {e}")
            return None

    def log(self, payload: dict):
        """Add evidence to logging queue."""
        self.queue.put(payload)

    def log_sync(self, payload: dict) -> Optional[str]:
        """Log evidence synchronously and return event_id."""
        ctx = ssl.create_default_context()
        return self._send_evidence(payload, ctx)

    def shutdown(self):
        """Stop the background worker."""
        self._stop_event.set()
        self.queue.put(None)
        if self.thread:
            self.thread.join(timeout=5)


# Global async logger instance
_async_logger: Optional[AsyncLogger] = None


def _get_async_logger(config: AegisLogConfig) -> AsyncLogger:
    """Get or create the async logger."""
    global _async_logger
    if _async_logger is None:
        _async_logger = AsyncLogger(config)
    return _async_logger


def _truncate(text: str, max_length: int) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + f"... [truncated, {len(text)} chars total]"


def _build_policy_context(config: AegisLogConfig) -> Optional[dict]:
    """Build policy context from config."""
    if config.policy_name:
        return {
            "policy_name": config.policy_name,
            "policy_version": config.policy_version or "1.0.0",
            "policy_hash": config.policy_hash or f"sha256:{config.policy_name}"
        }
    return None


def _build_data_provenance(config: AegisLogConfig, model: str) -> Optional[dict]:
    """Build data provenance from config."""
    databases = config.reference_databases.copy()
    if model:
        databases.append(model)

    if databases:
        return {
            "reference_databases": databases,
            "data_version": datetime.now(timezone.utc).strftime("%Y-%m-%d")
        }
    return None


# =============================================================================
# OpenAI Wrapper
# =============================================================================

def wrap_openai(client: Any, tenant_id: str = None, api_key: str = None, **kwargs) -> Any:
    """
    Wrap an OpenAI client to automatically log all chat completions.

    Args:
        client: OpenAI client instance
        tenant_id: AegisLog tenant ID
        api_key: AegisLog API key
        **kwargs: Additional AegisLogConfig options

    Returns:
        Wrapped client with automatic logging

    Example:
        from openai import OpenAI
        from aegislog.auto_logger import wrap_openai

        client = wrap_openai(
            OpenAI(),
            tenant_id="my-company",
            api_key="aegislog-prod-..."
        )

        # Use normally
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )

        # Access evidence ID
        print(f"Evidence: {response._aegislog_event_id}")
    """
    config = AegisLogConfig(
        tenant_id=tenant_id or "aegislog",
        api_key=api_key or "",
        **kwargs
    )

    if not config.api_key:
        raise ValueError("AegisLog API key is required")

    logger = _get_async_logger(config) if config.async_logging else None

    # Store original create method
    original_create = client.chat.completions.create

    @wraps(original_create)
    def logged_create(*args, **create_kwargs):
        """Wrapped create method with automatic logging."""
        start_time = time.time()

        # Extract request info
        model = create_kwargs.get('model', 'unknown')
        messages = create_kwargs.get('messages', [])
        temperature = create_kwargs.get('temperature')
        max_tokens = create_kwargs.get('max_tokens')

        # Format prompt
        prompt_parts = []
        system_prompt = None
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                system_prompt = content
            prompt_parts.append(f"[{role}]: {content}")
        full_prompt = "\n".join(prompt_parts)

        # Call original method
        response = original_create(*args, **create_kwargs)

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response info
        ai_response = ""
        if response.choices:
            ai_response = response.choices[0].message.content or ""

        tokens_used = 0
        input_tokens = 0
        output_tokens = 0
        if response.usage:
            tokens_used = response.usage.total_tokens
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

        # Build evidence payload
        payload = {
            "tenant_id": config.tenant_id,
            "event_type": "ai_inference",
            "model": response.model or model,
            "provider": "openai",
            "tokens_used": tokens_used,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "finish_reason": response.choices[0].finish_reason if response.choices else None,
        }

        # Add prompt/response if enabled
        if config.log_prompts:
            payload["prompt"] = _truncate(full_prompt, config.max_content_length)
            if system_prompt:
                payload["system_prompt"] = _truncate(system_prompt, config.max_content_length)

        if config.log_responses:
            payload["response"] = _truncate(ai_response, config.max_content_length)

        # Add optional parameters
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        # Add policy context
        policy_context = _build_policy_context(config)
        if policy_context:
            payload["policy_context"] = policy_context

        # Add data provenance
        data_provenance = _build_data_provenance(config, model)
        if data_provenance:
            payload["data_provenance"] = data_provenance

        # Log evidence
        if config.async_logging and logger:
            logger.log(payload)
            response._aegislog_event_id = "(async - check events API)"
        else:
            event_id = AsyncLogger(config).log_sync(payload)
            response._aegislog_event_id = event_id

        response._aegislog_logged = True

        return response

    # Replace create method
    client.chat.completions.create = logged_create
    client._aegislog_config = config

    return client


# =============================================================================
# Anthropic Wrapper
# =============================================================================

def wrap_anthropic(client: Any, tenant_id: str = None, api_key: str = None, **kwargs) -> Any:
    """
    Wrap an Anthropic client to automatically log all message creations.

    Args:
        client: Anthropic client instance
        tenant_id: AegisLog tenant ID
        api_key: AegisLog API key
        **kwargs: Additional AegisLogConfig options

    Returns:
        Wrapped client with automatic logging

    Example:
        import anthropic
        from aegislog.auto_logger import wrap_anthropic

        client = wrap_anthropic(
            anthropic.Anthropic(),
            tenant_id="my-company",
            api_key="aegislog-prod-..."
        )

        # Use normally
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}]
        )

        # Access evidence ID
        print(f"Evidence: {message._aegislog_event_id}")
    """
    config = AegisLogConfig(
        tenant_id=tenant_id or "aegislog",
        api_key=api_key or "",
        **kwargs
    )

    if not config.api_key:
        raise ValueError("AegisLog API key is required")

    logger = _get_async_logger(config) if config.async_logging else None

    # Store original create method
    original_create = client.messages.create

    @wraps(original_create)
    def logged_create(*args, **create_kwargs):
        """Wrapped create method with automatic logging."""
        start_time = time.time()

        # Extract request info
        model = create_kwargs.get('model', 'unknown')
        messages = create_kwargs.get('messages', [])
        system = create_kwargs.get('system')
        temperature = create_kwargs.get('temperature')
        max_tokens = create_kwargs.get('max_tokens')

        # Format prompt
        prompt_parts = []
        if system:
            prompt_parts.append(f"[system]: {system}")
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt_parts.append(f"[{role}]: {content}")
        full_prompt = "\n".join(prompt_parts)

        # Call original method
        response = original_create(*args, **create_kwargs)

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract response info
        ai_response = ""
        if response.content:
            ai_response = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])

        input_tokens = response.usage.input_tokens if response.usage else 0
        output_tokens = response.usage.output_tokens if response.usage else 0
        tokens_used = input_tokens + output_tokens

        # Build evidence payload
        payload = {
            "tenant_id": config.tenant_id,
            "event_type": "ai_inference",
            "model": response.model or model,
            "provider": "anthropic",
            "tokens_used": tokens_used,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stop_reason": response.stop_reason,
        }

        # Add prompt/response if enabled
        if config.log_prompts:
            payload["prompt"] = _truncate(full_prompt, config.max_content_length)
            if system:
                payload["system_prompt"] = _truncate(system, config.max_content_length)

        if config.log_responses:
            payload["response"] = _truncate(ai_response, config.max_content_length)

        # Add optional parameters
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        # Add policy context
        policy_context = _build_policy_context(config)
        if policy_context:
            payload["policy_context"] = policy_context

        # Add data provenance
        data_provenance = _build_data_provenance(config, model)
        if data_provenance:
            payload["data_provenance"] = data_provenance

        # Log evidence
        if config.async_logging and logger:
            logger.log(payload)
            response._aegislog_event_id = "(async - check events API)"
        else:
            event_id = AsyncLogger(config).log_sync(payload)
            response._aegislog_event_id = event_id

        response._aegislog_logged = True

        return response

    # Replace create method
    client.messages.create = logged_create
    client._aegislog_config = config

    return client


# =============================================================================
# Convenience function for any client
# =============================================================================

def auto_log(client: Any, tenant_id: str = None, api_key: str = None, **kwargs) -> Any:
    """
    Automatically wrap any supported AI client for evidence logging.

    Detects the client type and applies the appropriate wrapper.

    Args:
        client: AI client instance (OpenAI, Anthropic, etc.)
        tenant_id: AegisLog tenant ID
        api_key: AegisLog API key
        **kwargs: Additional options

    Returns:
        Wrapped client with automatic logging

    Example:
        from aegislog.auto_logger import auto_log
        from openai import OpenAI

        client = auto_log(
            OpenAI(),
            tenant_id="my-company",
            api_key="aegislog-prod-..."
        )
    """
    client_type = type(client).__module__

    if 'openai' in client_type:
        return wrap_openai(client, tenant_id=tenant_id, api_key=api_key, **kwargs)
    elif 'anthropic' in client_type:
        return wrap_anthropic(client, tenant_id=tenant_id, api_key=api_key, **kwargs)
    else:
        raise ValueError(f"Unsupported client type: {client_type}. Supported: openai, anthropic")


# =============================================================================
# Context manager for temporary logging
# =============================================================================

class LoggingContext:
    """
    Context manager for temporary evidence logging configuration.

    Example:
        with LoggingContext(policy_name="v2_policy", policy_version="2.0.0"):
            response = client.chat.completions.create(...)
    """

    def __init__(self, client: Any, **kwargs):
        self.client = client
        self.kwargs = kwargs
        self.original_config = None

    def __enter__(self):
        if hasattr(self.client, '_aegislog_config'):
            self.original_config = self.client._aegislog_config
            # Create new config with overrides
            new_config = AegisLogConfig(
                endpoint=self.original_config.endpoint,
                tenant_id=self.original_config.tenant_id,
                api_key=self.original_config.api_key,
                **{**vars(self.original_config), **self.kwargs}
            )
            self.client._aegislog_config = new_config
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_config:
            self.client._aegislog_config = self.original_config
        return False
