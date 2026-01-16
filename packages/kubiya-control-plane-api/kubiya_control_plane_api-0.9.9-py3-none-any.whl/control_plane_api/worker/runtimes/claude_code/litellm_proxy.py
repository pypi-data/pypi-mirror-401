"""
Local FastAPI proxy for Claude Code SDK to inject Langfuse metadata.

This proxy runs in the same process as the worker and intercepts requests
from Claude Code SDK to add missing metadata before forwarding to the real
LiteLLM proxy.

Architecture:
    Claude Code SDK → Local Proxy (adds metadata) → Real LiteLLM Proxy → Langfuse

The proxy:
1. Receives requests from Claude Code SDK
2. Extracts execution context from thread-local cache
3. Injects Langfuse metadata (trace_name, trace_user_id, session_id, etc.)
4. Forwards request to real LiteLLM proxy
5. Returns response back to Claude Code SDK
"""

import asyncio
import json
import os
import re
import threading
import time
from typing import Dict, Any, Optional, List, Tuple
import structlog
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import uvicorn

logger = structlog.get_logger(__name__)


# Cache for available models from upstream LiteLLM proxy
_available_models_cache: Optional[Dict[str, Any]] = None
_available_models_cache_time: float = 0
_available_models_cache_ttl: int = 300  # 5 minutes


async def fetch_available_models(
    litellm_base_url: str,
    litellm_api_key: str,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_delay: float = 1.0,
) -> List[str]:
    """
    Fetch available models from the upstream LiteLLM proxy with retry logic.

    Args:
        litellm_base_url: Base URL of LiteLLM proxy
        litellm_api_key: API key for authentication
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay between retries (doubles each retry)

    Returns:
        List of available model IDs
    """
    global _available_models_cache, _available_models_cache_time

    # Check cache first
    now = time.time()
    if _available_models_cache is not None and (now - _available_models_cache_time) < _available_models_cache_ttl:
        logger.debug(
            "using_cached_available_models",
            model_count=len(_available_models_cache.get("models", [])),
            cache_age_seconds=int(now - _available_models_cache_time),
        )
        return _available_models_cache.get("models", [])

    last_error = None
    current_delay = retry_delay

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(
                    f"{litellm_base_url.rstrip('/')}/v1/models",
                    headers={"Authorization": f"Bearer {litellm_api_key}"},
                )

                if response.status_code == 200:
                    data = response.json()
                    # LiteLLM returns {"data": [{"id": "model-name", ...}, ...], "object": "list"}
                    models = []
                    if "data" in data and isinstance(data["data"], list):
                        models = [m.get("id") for m in data["data"] if m.get("id")]

                    # Update cache
                    _available_models_cache = {"models": models}
                    _available_models_cache_time = time.time()

                    logger.info(
                        "fetched_available_models_from_upstream",
                        model_count=len(models),
                        models=models[:10] if len(models) > 10 else models,
                        litellm_base_url=litellm_base_url,
                        attempt=attempt + 1,
                    )
                    return models

                elif response.status_code in (502, 503, 504):
                    # Transient errors - retry
                    last_error = f"HTTP {response.status_code}"
                    logger.warning(
                        "transient_error_fetching_models",
                        status_code=response.status_code,
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        retry_delay=current_delay,
                    )
                else:
                    # Non-retryable error
                    logger.warning(
                        "failed_to_fetch_models_from_upstream",
                        status_code=response.status_code,
                        response_text=response.text[:500] if response.text else "",
                        litellm_base_url=litellm_base_url,
                    )
                    return []

        except (httpx.ConnectError, httpx.TimeoutException) as e:
            last_error = str(e)
            logger.warning(
                "connection_error_fetching_models",
                error=str(e),
                error_type=type(e).__name__,
                attempt=attempt + 1,
                max_retries=max_retries,
                retry_delay=current_delay,
            )

        except Exception as e:
            # Unexpected error - don't retry
            logger.error(
                "unexpected_error_fetching_models",
                error=str(e),
                error_type=type(e).__name__,
                litellm_base_url=litellm_base_url,
                exc_info=True,
            )
            return []

        # Wait before retry (with exponential backoff)
        if attempt < max_retries - 1:
            await asyncio.sleep(current_delay)
            current_delay *= 2  # Exponential backoff

    # All retries exhausted
    logger.error(
        "all_retries_exhausted_fetching_models",
        last_error=last_error,
        max_retries=max_retries,
        litellm_base_url=litellm_base_url,
    )
    return []


def get_cached_available_models() -> List[str]:
    """
    Get cached available models (synchronous, for use in non-async contexts).

    Returns empty list if cache is not populated.
    """
    global _available_models_cache, _available_models_cache_time

    now = time.time()
    if _available_models_cache is not None and (now - _available_models_cache_time) < _available_models_cache_ttl:
        return _available_models_cache.get("models", [])
    return []


def _normalize_model_name(model: str) -> str:
    """
    Normalize model name for comparison.

    Handles various model naming patterns:
    - Provider prefixes: bedrock/, anthropic/, openai/, azure/, etc.
    - Region prefixes for Bedrock: us., eu., ap., etc.
    - Version suffixes: -v1:0, -20240620-v1:0, etc.

    Args:
        model: Model name to normalize

    Returns:
        Normalized model name (lowercase, without common prefixes/suffixes)
    """
    normalized = model.lower().strip()

    # Remove common provider prefixes (order matters - longest first)
    provider_prefixes = [
        "bedrock/converse/", "bedrock/invoke/",  # More specific first
        "bedrock/", "anthropic/", "openai/", "azure/", "vertex_ai/",
        "kubiya/", "litellm/",
    ]
    for prefix in provider_prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break

    # Remove Bedrock region prefixes (us., eu., ap., etc.)
    # Pattern: XX. where XX is 2 lowercase letters
    normalized = re.sub(r'^[a-z]{2}\.', '', normalized)

    # Remove provider prefixes within model name (anthropic., meta., etc.)
    inner_prefixes = ["anthropic.", "meta.", "amazon.", "mistral.", "ai21.", "cohere."]
    for prefix in inner_prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break

    # Remove version suffixes like -v1:0, -v2:0, etc.
    normalized = re.sub(r'-v\d+:\d+$', '', normalized)

    # Remove date-version suffixes like -20240620-v1:0
    normalized = re.sub(r'-\d{8}-v\d+:\d+$', '', normalized)
    normalized = re.sub(r'-\d{8}$', '', normalized)

    return normalized


def _calculate_model_similarity(requested: str, available: str) -> float:
    """
    Calculate similarity score between two model names.

    Higher score means better match. Uses normalized names and
    considers various matching strategies.

    Args:
        requested: Requested model name
        available: Available model name

    Returns:
        Similarity score (0.0 to 1.0)
    """
    req_norm = _normalize_model_name(requested)
    avail_norm = _normalize_model_name(available)

    # Exact match after normalization
    if req_norm == avail_norm:
        return 1.0

    # One contains the other (after normalization)
    if req_norm in avail_norm:
        return 0.9
    if avail_norm in req_norm:
        return 0.85

    # Check for key model family matches
    # e.g., "claude-sonnet-4" should match "claude-sonnet-4-20250115"
    model_families = [
        "claude-sonnet-4", "claude-4-sonnet", "claude-sonnet-4-5",
        "claude-3-5-sonnet", "claude-3-sonnet", "claude-3-haiku", "claude-3-opus",
        "claude-instant", "claude-v2",
        "gpt-4", "gpt-4o", "gpt-3.5",
        "llama-3", "llama-2",
        "mistral", "mixtral",
    ]

    for family in model_families:
        if family in req_norm and family in avail_norm:
            return 0.8

    # Partial word overlap
    req_parts = set(req_norm.replace("-", " ").replace(".", " ").split())
    avail_parts = set(avail_norm.replace("-", " ").replace(".", " ").split())
    overlap = req_parts & avail_parts
    if overlap:
        return 0.5 * len(overlap) / max(len(req_parts), len(avail_parts))

    return 0.0


def validate_and_resolve_model(
    requested_model: str,
    available_models: List[str],
    default_fallback: str = None,
) -> Tuple[str, bool]:
    """
    Validate requested model against available models and resolve fallback.

    Handles complex model naming patterns including:
    - Bedrock: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
    - Cross-region: bedrock/us.anthropic.claude-sonnet-4-20250115-v1:0
    - Simple: claude-sonnet-4, gpt-4o
    - Provider-prefixed: kubiya/claude-sonnet-4, anthropic/claude-3-sonnet

    Args:
        requested_model: The model requested by the user/agent
        available_models: List of available model IDs from upstream
        default_fallback: Default model to use if no match found

    Returns:
        Tuple of (resolved_model, was_fallback_used)
    """
    if not available_models:
        # No available models list - can't validate, use as-is
        logger.warning(
            "cannot_validate_model_no_available_models",
            requested_model=requested_model,
            note="Proceeding with requested model without validation"
        )
        return requested_model, False

    # Exact match (case-sensitive)
    if requested_model in available_models:
        return requested_model, False

    # Case-insensitive exact match
    requested_lower = requested_model.lower()
    for available in available_models:
        if available.lower() == requested_lower:
            logger.info(
                "model_case_insensitive_match",
                requested_model=requested_model,
                matched_model=available,
            )
            return available, False

    # Find best match using similarity scoring
    best_match = None
    best_score = 0.0

    for available in available_models:
        score = _calculate_model_similarity(requested_model, available)
        if score > best_score:
            best_score = score
            best_match = available

    # Accept match if score is above threshold
    if best_score >= 0.7:
        logger.info(
            "model_similarity_match_found",
            requested_model=requested_model,
            matched_model=best_match,
            similarity_score=best_score,
            note="Found similar model via smart matching"
        )
        return best_match, True

    # Log detailed match attempts for debugging
    logger.warning(
        "model_no_good_match_found",
        requested_model=requested_model,
        requested_normalized=_normalize_model_name(requested_model),
        best_candidate=best_match,
        best_score=best_score,
        available_models_sample=available_models[:5] if len(available_models) > 5 else available_models,
        available_count=len(available_models),
    )

    # No good match - find best fallback from same provider/family
    # Priority: same family > default_fallback > first available
    fallback = _find_same_family_fallback(requested_model, available_models)
    if not fallback:
        fallback = default_fallback or (available_models[0] if available_models else requested_model)

    logger.warning(
        "model_not_found_using_fallback",
        requested_model=requested_model,
        fallback_model=fallback,
        available_models=available_models[:10] if len(available_models) > 10 else available_models,
        note="Requested model not available, using same-family fallback if available"
    )
    return fallback, True


def _find_same_family_fallback(requested_model: str, available_models: List[str]) -> Optional[str]:
    """
    Find a fallback model from the same provider/family.

    For Claude models, prefer other Claude models.
    For GPT models, prefer other GPT models.
    For Llama models, prefer other Llama models.
    etc.

    Args:
        requested_model: The requested model name
        available_models: List of available models

    Returns:
        Best same-family fallback, or None if no match
    """
    requested_lower = requested_model.lower()

    # Define model families and their identifying patterns
    # Order matters - more specific patterns first
    model_families = [
        # Claude family
        ("claude", ["claude", "anthropic"]),
        # OpenAI family
        ("gpt", ["gpt-4", "gpt-3", "gpt4", "gpt3", "openai"]),
        # Llama family
        ("llama", ["llama", "meta"]),
        # Mistral family
        ("mistral", ["mistral", "mixtral"]),
        # DeepSeek family
        ("deepseek", ["deepseek"]),
    ]

    # Determine which family the requested model belongs to
    requested_family = None
    for family_name, patterns in model_families:
        for pattern in patterns:
            if pattern in requested_lower:
                requested_family = family_name
                break
        if requested_family:
            break

    if not requested_family:
        return None

    # Find available models from the same family
    # Score them by how well they match
    same_family_models = []
    for available in available_models:
        available_lower = available.lower()
        for family_name, patterns in model_families:
            if family_name == requested_family:
                for pattern in patterns:
                    if pattern in available_lower:
                        # Calculate a preference score
                        # Prefer models with more capability (sonnet > haiku, etc.)
                        score = _calculate_model_capability_score(available)
                        same_family_models.append((available, score))
                        break
                break

    if not same_family_models:
        return None

    # Sort by capability score (descending) and return the best
    same_family_models.sort(key=lambda x: x[1], reverse=True)
    best_fallback = same_family_models[0][0]

    logger.info(
        "same_family_fallback_found",
        requested_model=requested_model,
        requested_family=requested_family,
        fallback_model=best_fallback,
        same_family_options=[m[0] for m in same_family_models],
    )

    return best_fallback


def _calculate_model_capability_score(model: str) -> int:
    """
    Calculate a capability score for model preference.
    Higher score = more capable model (preferred for fallback).

    Args:
        model: Model name

    Returns:
        Capability score (higher is more capable)
    """
    model_lower = model.lower()
    score = 0

    # Claude models - prefer opus > sonnet > haiku
    if "opus" in model_lower:
        score = 100
    elif "sonnet" in model_lower:
        score = 80
    elif "haiku" in model_lower:
        score = 60
    # GPT models - prefer gpt-4 > gpt-3.5
    elif "gpt-4o" in model_lower:
        score = 95
    elif "gpt-4" in model_lower:
        score = 90
    elif "gpt-3.5" in model_lower or "gpt-35" in model_lower:
        score = 70
    # Llama models - prefer larger
    elif "llama-3" in model_lower or "llama3" in model_lower:
        score = 75
    elif "llama-2" in model_lower or "llama2" in model_lower:
        score = 65
    # DeepSeek
    elif "deepseek-r1" in model_lower:
        score = 85
    elif "deepseek-v3" in model_lower:
        score = 80
    elif "deepseek" in model_lower:
        score = 70
    # Mistral
    elif "mixtral" in model_lower:
        score = 75
    elif "mistral" in model_lower:
        score = 70
    else:
        score = 50  # Default for unknown models

    return score


# Thread-local storage for execution context
# This allows us to access execution metadata from the proxy
class ExecutionContextStore:
    """
    Thread-safe storage for execution context metadata with TTL and proactive cleanup.

    Features:
    - TTL-based expiration (default 3600s)
    - Proactive cleanup timer (runs every 60s)
    - Circuit breaker to prevent runaway memory growth
    - Thread-safe operations
    """

    def __init__(self, ttl_seconds: int = 3600, max_contexts: int = 1000):
        self._contexts: Dict[str, Dict[str, Any]] = {}
        self._context_timestamps: Dict[str, float] = {}
        self._ttl_seconds = ttl_seconds
        self._max_contexts = max_contexts  # Circuit breaker threshold
        self._current_execution: Optional[str] = None
        self._lock = threading.Lock()

        # Proactive cleanup timer
        self._cleanup_timer: Optional[threading.Timer] = None
        self._cleanup_interval = 60  # Run cleanup every 60 seconds
        self._start_proactive_cleanup()

    def _start_proactive_cleanup(self):
        """Start periodic cleanup timer."""
        self._cleanup_timer = threading.Timer(
            self._cleanup_interval,
            self._proactive_cleanup_worker
        )
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()
        logger.debug("proactive_cleanup_timer_started", interval=self._cleanup_interval)

    def _proactive_cleanup_worker(self):
        """Worker that runs periodic cleanup."""
        try:
            self._cleanup_expired()

            # Check circuit breaker
            with self._lock:
                context_count = len(self._contexts)

            if context_count > self._max_contexts:
                logger.error(
                    "context_store_circuit_breaker_triggered",
                    context_count=context_count,
                    max_contexts=self._max_contexts,
                    action="forcing_aggressive_cleanup"
                )
                # Aggressive cleanup: remove oldest 50%
                self._force_cleanup(keep_ratio=0.5)

        except Exception as e:
            logger.error(
                "proactive_cleanup_error",
                error=str(e),
                error_type=type(e).__name__,
                exc_info=True
            )
        finally:
            # Reschedule timer
            self._start_proactive_cleanup()

    def _force_cleanup(self, keep_ratio: float = 0.5):
        """
        Force cleanup of oldest contexts when circuit breaker triggers.

        Args:
            keep_ratio: Ratio of newest contexts to keep (0.5 = keep newest 50%)
        """
        with self._lock:
            if not self._contexts:
                return

            # Sort by timestamp (oldest first)
            sorted_ids = sorted(
                self._context_timestamps.items(),
                key=lambda x: x[1]
            )

            # Calculate how many to remove
            keep_count = int(len(sorted_ids) * keep_ratio)
            to_remove = sorted_ids[:len(sorted_ids) - keep_count]

            # Remove oldest contexts
            removed_count = 0
            for exec_id, _ in to_remove:
                self._contexts.pop(exec_id, None)
                self._context_timestamps.pop(exec_id, None)
                if self._current_execution == exec_id:
                    self._current_execution = None
                removed_count += 1

            logger.warning(
                "forced_cleanup_completed",
                removed=removed_count,
                remaining=len(self._contexts),
                keep_ratio=keep_ratio
            )

    def set_context(self, execution_id: str, context: Dict[str, Any]):
        """Store execution context for an execution ID with timestamp."""
        with self._lock:
            # Check circuit breaker before adding
            if len(self._contexts) >= self._max_contexts:
                logger.error(
                    "context_store_at_capacity",
                    current_count=len(self._contexts),
                    max_contexts=self._max_contexts,
                    action="rejecting_new_context"
                )
                raise RuntimeError(
                    f"Context store at capacity ({self._max_contexts}). "
                    "System may be leaking contexts or under high load."
                )

            self._contexts[execution_id] = context
            self._context_timestamps[execution_id] = time.time()
            self._current_execution = execution_id
            logger.debug(
                "execution_context_stored",
                execution_id=execution_id[:8] if len(execution_id) >= 8 else execution_id,
                total_contexts=len(self._contexts),
                has_user_id=bool(context.get("user_id")),
                has_session_id=bool(context.get("session_id")),
            )

    def get_context(self, execution_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve execution context for an execution ID if not expired.

        If execution_id is None, returns the current active execution context.
        """
        with self._lock:
            target_id = execution_id if execution_id else self._current_execution
            if not target_id:
                return None

            # Check if expired
            timestamp = self._context_timestamps.get(target_id)
            if timestamp and (time.time() - timestamp) > self._ttl_seconds:
                # Expired - remove and return None
                self._contexts.pop(target_id, None)
                self._context_timestamps.pop(target_id, None)
                logger.debug("execution_context_expired", execution_id=target_id[:8] if len(target_id) >= 8 else target_id)
                return None

            return self._contexts.get(target_id)

    def get_current_execution_id(self) -> Optional[str]:
        """Get the current active execution ID."""
        with self._lock:
            return self._current_execution

    def get_any_valid_execution_id(self) -> Optional[str]:
        """
        Get any valid (non-expired) execution ID.

        This is a fallback when _current_execution is None but there are still
        valid contexts available. Useful for sub-agent requests that arrive
        after _current_execution has been overwritten by concurrent executions.

        Returns the most recently set context's execution ID.
        """
        with self._lock:
            if not self._contexts:
                return None

            now = time.time()
            # Find the most recent non-expired context
            valid_contexts = [
                (exec_id, ts) for exec_id, ts in self._context_timestamps.items()
                if (now - ts) <= self._ttl_seconds and exec_id in self._contexts
            ]

            if not valid_contexts:
                return None

            # Return the most recently set context
            most_recent = max(valid_contexts, key=lambda x: x[1])
            logger.debug(
                "using_fallback_execution_context",
                execution_id=most_recent[0][:8] if len(most_recent[0]) >= 8 else most_recent[0],
                total_valid_contexts=len(valid_contexts),
            )
            return most_recent[0]

    def clear_context(self, execution_id: str):
        """Clear execution context after execution completes."""
        with self._lock:
            if execution_id in self._contexts:
                del self._contexts[execution_id]
                self._context_timestamps.pop(execution_id, None)
                if self._current_execution == execution_id:
                    self._current_execution = None
                logger.debug(
                    "execution_context_cleared",
                    execution_id=execution_id[:8] if len(execution_id) >= 8 else execution_id,
                    remaining_contexts=len(self._contexts)
                )

    def _cleanup_expired(self) -> None:
        """Remove contexts older than TTL."""
        now = time.time()
        with self._lock:
            expired_ids = [
                exec_id for exec_id, timestamp in self._context_timestamps.items()
                if (now - timestamp) > self._ttl_seconds
            ]

            if expired_ids:
                for exec_id in expired_ids:
                    self._contexts.pop(exec_id, None)
                    self._context_timestamps.pop(exec_id, None)
                    if self._current_execution == exec_id:
                        self._current_execution = None

                logger.info(
                    "expired_contexts_cleaned",
                    removed=len(expired_ids),
                    remaining=len(self._contexts)
                )

    def get_stats(self) -> Dict[str, Any]:
        """Get context store statistics."""
        with self._lock:
            now = time.time()
            ages = [now - ts for ts in self._context_timestamps.values()]
            return {
                'total_contexts': len(self._contexts),
                'max_contexts': self._max_contexts,
                'ttl_seconds': self._ttl_seconds,
                'oldest_age_seconds': int(max(ages)) if ages else 0,
                'newest_age_seconds': int(min(ages)) if ages else 0,
            }

    def shutdown(self):
        """Stop proactive cleanup timer."""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
            logger.info("context_store_cleanup_timer_stopped")


# Global context store
_context_store = ExecutionContextStore()


class ContextCleanupScheduler:
    """Schedules delayed context cleanup without blocking."""

    def __init__(self):
        self._pending_cleanups: Dict[str, asyncio.Task] = {}
        self._lock = threading.Lock()

    def schedule_cleanup(
        self,
        execution_id: str,
        delay_seconds: float,
        store: 'ExecutionContextStore'
    ):
        """Schedule cleanup after delay (non-blocking)."""
        with self._lock:
            # Cancel existing cleanup if rescheduling
            if execution_id in self._pending_cleanups:
                self._pending_cleanups[execution_id].cancel()

            # Create background task for delayed cleanup
            try:
                loop = asyncio.get_event_loop()
                task = loop.create_task(
                    self._delayed_cleanup(execution_id, delay_seconds, store)
                )
                self._pending_cleanups[execution_id] = task
            except RuntimeError:
                # No event loop - fallback to immediate cleanup
                store.clear_context(execution_id)

    async def _delayed_cleanup(
        self,
        execution_id: str,
        delay_seconds: float,
        store: 'ExecutionContextStore'
    ):
        """Internal: Wait then clear context."""
        try:
            await asyncio.sleep(delay_seconds)
            store.clear_context(execution_id)
        except asyncio.CancelledError:
            pass  # Cleanup was cancelled
        except Exception as e:
            # Log but don't crash - TTL will handle it
            logger.warning(
                "context_cleanup_error",
                execution_id=execution_id[:8] if len(execution_id) >= 8 else execution_id,
                error=str(e)
            )
        finally:
            with self._lock:
                self._pending_cleanups.pop(execution_id, None)


# Global cleanup scheduler
_cleanup_scheduler = ContextCleanupScheduler()


def _hash_user_id(user_id: str, organization_id: str) -> str:
    """
    Hash user_id to avoid sending email addresses to Anthropic API.

    Anthropic API rejects email addresses in metadata.user_id.
    We hash the email with org to create a unique, non-PII identifier.

    Args:
        user_id: User ID (may be email address)
        organization_id: Organization ID

    Returns:
        Hashed user identifier (SHA256, first 16 chars)
    """
    import hashlib
    combined = f"{user_id}-{organization_id}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def build_langfuse_metadata(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build Langfuse metadata from execution context.

    Matches the format used by agno runtime for consistency.

    Args:
        context: Execution context with user_id, session_id, agent_id, etc.

    Returns:
        Metadata dict for Langfuse tracking
    """
    metadata = {}

    user_id = context.get("user_id")
    organization_id = context.get("organization_id")
    session_id = context.get("session_id")
    agent_id = context.get("agent_id")
    agent_name = context.get("agent_name")
    model_id = context.get("model_id")

    # Langfuse naming fields - use custom values if provided, otherwise default to "agent-chat"
    # This allows both agent-chat and plan execution to use the same proxy
    metadata["name"] = context.get("name", "agent-chat")
    metadata["trace_name"] = context.get("trace_name", "agent-chat")
    metadata["generation_name"] = context.get("generation_name", "agent-chat")

    # Hash user_id to avoid sending email addresses to Anthropic API
    # Anthropic rejects: "user_id appears to contain an email address"
    if user_id and organization_id:
        hashed_user_id = _hash_user_id(user_id, organization_id)
        metadata["trace_user_id"] = hashed_user_id
        metadata["user_id"] = hashed_user_id

    # Use session_id as trace_id to group conversation turns
    if session_id:
        metadata["trace_id"] = session_id
        metadata["session_id"] = session_id

    # Additional metadata (these are safe - not sent to Anthropic)
    if agent_id:
        metadata["agent_id"] = agent_id
    if agent_name:
        metadata["agent_name"] = agent_name
    if user_id:
        metadata["user_email"] = user_id  # Keep original for Langfuse internal tracking
    if organization_id:
        metadata["organization_id"] = organization_id
    if model_id:
        metadata["model"] = model_id

    return metadata


class LiteLLMProxyApp:
    """FastAPI application for LiteLLM proxy with metadata injection."""

    def __init__(self, litellm_base_url: str, litellm_api_key: str):
        """
        Initialize the proxy application.

        Args:
            litellm_base_url: Base URL of the real LiteLLM proxy
            litellm_api_key: API key for LiteLLM proxy
        """
        self.litellm_base_url = litellm_base_url.rstrip('/')
        self.litellm_api_key = litellm_api_key
        self.client = None  # Will be lazily initialized per request
        self._client_lock = None  # Asyncio lock for thread-safe client creation

        # Create FastAPI app WITHOUT lifespan
        # Reason: httpx clients must be created in the same event loop where they're used
        # When uvicorn runs in a background thread, it has its own event loop
        # Creating the client in a different loop causes ConnectError
        self.app = FastAPI(
            title="Claude Code LiteLLM Proxy",
            description="Local proxy to inject Langfuse metadata for Claude Code SDK",
        )

        # Register routes
        self._register_routes()

    def _register_routes(self):
        """Register all proxy routes."""

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "claude-code-litellm-proxy"}

        @self.app.post("/v1/messages")
        async def proxy_messages(request: Request):
            """
            Proxy endpoint for Anthropic Messages API format.

            This is the main endpoint used by Claude Code SDK.
            We keep the Anthropic format by forwarding to /v1/messages.
            """
            # Keep Anthropic format - forward to /v1/messages
            return await self._proxy_request(request, "/v1/messages")

        @self.app.post("/v1/chat/completions")
        async def proxy_chat_completions(request: Request):
            """
            Proxy endpoint for OpenAI Chat Completions API format.

            Fallback for OpenAI-format requests.
            """
            return await self._proxy_request(request, "/v1/chat/completions")

    async def _get_client(self) -> httpx.AsyncClient:
        """
        Get or create the httpx client in the current event loop.

        This ensures the client is created in the same event loop where it will be used,
        avoiding ConnectError when uvicorn runs in a background thread.

        Returns:
            httpx.AsyncClient instance
        """
        if self.client is None:
            # Initialize lock if needed (must be done in async context)
            if self._client_lock is None:
                self._client_lock = asyncio.Lock()

            async with self._client_lock:
                # Double-check after acquiring lock
                if self.client is None:
                    logger.info(
                        "initializing_httpx_client_in_current_event_loop",
                        litellm_base_url=self.litellm_base_url,
                    )
                    # Create client with explicit settings for reliability
                    # VERY long timeouts to handle long-running streaming LLM operations
                    # For streaming workflows, the read timeout needs to be very generous
                    # since the connection may be open for hours while streaming responses
                    self.client = httpx.AsyncClient(
                        timeout=httpx.Timeout(
                            connect=30.0,      # Connection timeout (reasonable for initial connection)
                            read=86400.0,      # Read timeout (24 hours for long streaming operations)
                            write=300.0,       # Write timeout (5 minutes for large payloads)
                            pool=300.0,        # Pool timeout (5 minutes to avoid pool exhaustion)
                        ),
                        limits=httpx.Limits(
                            max_keepalive_connections=50,  # Increased for better reuse
                            max_connections=200,           # Increased for high concurrency
                        ),
                        follow_redirects=True,
                    )
        return self.client

    async def cleanup(self):
        """Clean up HTTP client resources."""
        if self.client is not None:
            try:
                await self.client.aclose()
                logger.info("httpx_client_closed")
                self.client = None
            except Exception as e:
                logger.error(
                    "httpx_client_close_failed",
                    error=str(e),
                    error_type=type(e).__name__
                )

    async def _proxy_request(self, request: Request, path: str) -> Response:
        """
        Proxy a request to the real LiteLLM proxy with metadata injection.

        Args:
            request: Incoming FastAPI request
            path: API path to forward to

        Returns:
            Response from LiteLLM proxy
        """
        # Get or create client in current event loop
        client = await self._get_client()

        try:
            # Parse request body
            body = await request.json()

            # CRITICAL: Override model if KUBIYA_MODEL_OVERRIDE is set
            # This ensures the explicit model from CLI --model flag takes precedence
            model_override = os.environ.get("KUBIYA_MODEL_OVERRIDE")
            if model_override:
                original_model = body.get("model")
                body["model"] = model_override
                logger.info(
                    "model_override_applied_in_proxy",
                    original_model=original_model,
                    overridden_model=model_override,
                    path=path,
                    note="CLI --model flag or KUBIYA_MODEL env var is active"
                )

            # Model validation: Only validate when using a LOCAL/CUSTOM LiteLLM proxy
            # This prevents "Invalid model name" errors when the configured model doesn't exist
            # on a local proxy. Skip validation for the default Kubiya proxy which supports all models.
            #
            # Validation is enabled when ANY of these conditions are true:
            # - KUBIYA_ENABLE_LOCAL_PROXY is set (using local LiteLLM proxy)
            # - LITELLM_API_BASE is set to a non-default URL (custom proxy)
            # - KUBIYA_FORCE_MODEL_VALIDATION is set (explicit opt-in)
            default_proxy_url = "https://llm-proxy.kubiya.ai"
            is_local_proxy = os.environ.get("KUBIYA_ENABLE_LOCAL_PROXY", "").lower() in ("true", "1", "yes")
            is_custom_proxy = self.litellm_base_url and self.litellm_base_url.rstrip('/') != default_proxy_url
            force_validation = os.environ.get("KUBIYA_FORCE_MODEL_VALIDATION", "").lower() in ("true", "1", "yes")
            should_validate_model = is_local_proxy or is_custom_proxy or force_validation

            requested_model = body.get("model")
            if requested_model and should_validate_model:
                # Fetch available models from upstream (uses cache)
                available_models = await fetch_available_models(
                    self.litellm_base_url,
                    self.litellm_api_key,
                )

                if available_models:
                    resolved_model, used_fallback = validate_and_resolve_model(
                        requested_model,
                        available_models,
                    )

                    if used_fallback:
                        body["model"] = resolved_model
                        logger.warning(
                            "model_resolved_with_fallback",
                            original_model=requested_model,
                            resolved_model=resolved_model,
                            available_models_count=len(available_models),
                            path=path,
                            note="Original model not available, using fallback"
                        )
                else:
                    logger.warning(
                        "skipping_model_validation",
                        model=requested_model,
                        path=path,
                        note="Could not fetch available models from upstream, proceeding without validation"
                    )
            elif requested_model and not should_validate_model:
                logger.debug(
                    "model_validation_skipped",
                    model=requested_model,
                    litellm_base_url=self.litellm_base_url,
                    note="Using default Kubiya proxy, model validation not needed"
                )

            # Extract execution_id from custom header, or use current execution
            execution_id = request.headers.get("X-Execution-ID")

            if not execution_id:
                # Try to get current execution ID
                execution_id = _context_store.get_current_execution_id()

            if not execution_id:
                # Fallback: try to get any valid execution context
                # This handles sub-agent requests when _current_execution was overwritten
                execution_id = _context_store.get_any_valid_execution_id()
                if execution_id:
                    logger.debug(
                        "using_fallback_execution_id",
                        execution_id=execution_id[:8] if execution_id else None,
                        path=path,
                    )

            if not execution_id:
                # Still no execution_id - this is unexpected but not fatal
                # Log at debug level since this may happen during proxy startup/shutdown
                logger.debug(
                    "no_execution_id_available",
                    path=path,
                    note="Cannot inject Langfuse metadata - no execution context found"
                )

            if execution_id:
                # Get execution context and build metadata
                context = _context_store.get_context(execution_id)

                if context:
                    metadata = build_langfuse_metadata(context)

                    # For Anthropic format, we need to be more explicit with Langfuse fields
                    # LiteLLM looks for specific fields in specific places

                    # 1. Set 'user' at top level (works with both formats)
                    body["user"] = metadata.get("trace_user_id")

                    # 2. Initialize metadata dict
                    if "metadata" not in body:
                        body["metadata"] = {}

                    # 3. Put Langfuse fields with explicit naming that LiteLLM recognizes
                    # Based on LiteLLM source, these specific keys are extracted for Langfuse
                    body["metadata"]["generation_name"] = metadata.get("generation_name", "agent-chat")
                    body["metadata"]["trace_name"] = metadata.get("trace_name", "agent-chat")
                    body["metadata"]["trace_id"] = metadata.get("trace_id")
                    body["metadata"]["session_id"] = metadata.get("session_id")
                    body["metadata"]["trace_user_id"] = metadata.get("trace_user_id")
                    body["metadata"]["user_id"] = metadata.get("trace_user_id")

                    # Additional context metadata
                    body["metadata"]["agent_id"] = metadata.get("agent_id")
                    body["metadata"]["agent_name"] = metadata.get("agent_name")
                    body["metadata"]["organization_id"] = metadata.get("organization_id")
                    body["metadata"]["user_email"] = metadata.get("user_email")
                    body["metadata"]["model"] = metadata.get("model")

                    logger.debug(
                        "metadata_injected_into_request",
                        execution_id=execution_id[:8],
                        path=path,
                        user_field=body.get("user"),
                        metadata_keys=list(metadata.keys()),
                        trace_user_id=metadata.get("trace_user_id"),
                        trace_id=metadata.get("trace_id"),
                        session_id=metadata.get("session_id"),
                        trace_name=metadata.get("trace_name"),
                    )
                else:
                    logger.warning(
                        "no_context_found_for_execution",
                        execution_id=execution_id[:8] if execution_id else "unknown",
                        path=path,
                    )

            # Build forwarding URL (keep same endpoint - don't convert formats)
            forward_url = f"{self.litellm_base_url}{path}"

            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.litellm_api_key}",
                "Content-Type": "application/json",
            }

            # Add Langfuse metadata as custom headers (LiteLLM recognizes these)
            # Can be disabled via KUBIYA_DISABLE_LANGFUSE_HEADERS=true for local proxies
            # that don't support Langfuse or have incompatible versions
            langfuse_headers_enabled = os.environ.get("KUBIYA_DISABLE_LANGFUSE_HEADERS", "").lower() not in ("true", "1", "yes")

            if execution_id and langfuse_headers_enabled:
                context = _context_store.get_context(execution_id)
                if context:
                    metadata = build_langfuse_metadata(context)

                    # LiteLLM extracts Langfuse fields from these custom headers
                    # IMPORTANT: Header values MUST be str, never None
                    # Use `or ""` to handle both missing keys AND keys with None values
                    headers["X-Langfuse-Trace-Id"] = metadata.get("trace_id") or ""
                    headers["X-Langfuse-Session-Id"] = metadata.get("session_id") or ""
                    headers["X-Langfuse-User-Id"] = metadata.get("trace_user_id") or ""
                    headers["X-Langfuse-Trace-Name"] = metadata.get("trace_name") or "agent-chat"

                    # Additional metadata as JSON in custom header
                    extra_metadata = {
                        "agent_id": metadata.get("agent_id"),
                        "agent_name": metadata.get("agent_name"),
                        "organization_id": metadata.get("organization_id"),
                        "user_email": metadata.get("user_email"),
                    }
                    headers["X-Langfuse-Metadata"] = json.dumps(extra_metadata)

                    logger.debug(
                        "langfuse_headers_added",
                        execution_id=execution_id[:8],
                        trace_id=metadata.get("trace_id", ""),
                        session_id=metadata.get("session_id", ""),
                    )
            elif not langfuse_headers_enabled:
                logger.debug(
                    "langfuse_headers_disabled",
                    note="KUBIYA_DISABLE_LANGFUSE_HEADERS is set, skipping Langfuse header injection"
                )

            # Copy relevant headers from original request
            for header in ["X-Request-ID", "User-Agent"]:
                if header.lower() in request.headers:
                    headers[header] = request.headers[header.lower()]

            # Check if streaming is requested
            is_streaming = body.get("stream", False)

            if is_streaming:
                # Handle streaming response
                logger.info(
                    "starting_streaming_request",
                    url=forward_url,
                    model=body.get("model", "unknown"),
                    execution_id=execution_id[:8] if execution_id else "unknown",
                )
                return await self._proxy_streaming_request(client, forward_url, body, headers)
            else:
                # Handle non-streaming response
                response = await client.post(
                    forward_url,
                    json=body,
                    headers=headers,
                )

                logger.debug(
                    "litellm_request_completed",
                    status_code=response.status_code,
                    path=path,
                    execution_id=execution_id[:8] if execution_id else None,
                )

                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )

        except httpx.ConnectError as e:
            logger.error(
                "litellm_proxy_connection_error",
                error=str(e),
                error_type=type(e).__name__,
                path=path,
                forward_url=forward_url,
                litellm_base_url=self.litellm_base_url,
                message="Failed to connect to LiteLLM proxy - check network connectivity and URL",
            )
            raise HTTPException(
                status_code=502,
                detail=f"Failed to connect to LiteLLM proxy at {self.litellm_base_url}: {str(e)}"
            )

        except httpx.HTTPError as e:
            logger.error(
                "litellm_proxy_http_error",
                error=str(e),
                error_type=type(e).__name__,
                path=path,
                forward_url=forward_url,
            )
            raise HTTPException(status_code=502, detail=f"Proxy error: {str(e)}")

        except Exception as e:
            logger.error(
                "litellm_proxy_error",
                error=str(e),
                error_type=type(e).__name__,
                path=path,
                exc_info=True,
            )
            raise HTTPException(status_code=500, detail=f"Internal proxy error: {str(e)}")

    async def _proxy_streaming_request(
        self, client: httpx.AsyncClient, url: str, body: Dict[str, Any], headers: Dict[str, str]
    ) -> StreamingResponse:
        """
        Proxy a streaming request to LiteLLM with robust error handling.

        Args:
            client: httpx AsyncClient instance
            url: Forward URL
            body: Request body
            headers: Request headers

        Returns:
            StreamingResponse that forwards chunks from LiteLLM

        Raises:
            HTTPException: On connection or streaming errors
        """
        async def stream_generator():
            """Generator that yields chunks from LiteLLM with error handling."""
            try:
                # Use VERY long timeout for streaming to ensure long operations work
                # Streaming responses can take hours for complex workflows
                stream_timeout = httpx.Timeout(
                    connect=30.0,      # Connection timeout (reasonable for initial connection)
                    read=86400.0,      # Read timeout (24 hours for long streaming operations)
                    write=300.0,       # Write timeout (5 minutes for large payloads)
                    pool=300.0,        # Pool timeout (5 minutes to avoid pool exhaustion)
                )
                async with client.stream(
                    "POST",
                    url,
                    json=body,
                    headers=headers,
                    timeout=stream_timeout,
                ) as response:
                    # Check for HTTP errors before streaming
                    if response.status_code >= 400:
                        error_text = await response.aread()
                        logger.error(
                            "litellm_streaming_http_error",
                            status_code=response.status_code,
                            error=error_text.decode('utf-8', errors='ignore')[:500],
                            url=url,
                        )
                        # Yield error message as SSE event
                        error_msg = f"data: {{\"error\": \"HTTP {response.status_code}: {error_text.decode('utf-8', errors='ignore')[:200]}\"}}\n\n"
                        yield error_msg.encode('utf-8')
                        return

                    # Stream chunks
                    async for chunk in response.aiter_bytes():
                        yield chunk

            except httpx.ConnectError as e:
                logger.error(
                    "litellm_streaming_connection_error",
                    error=str(e),
                    url=url,
                    message="Failed to connect to LiteLLM proxy during streaming",
                )
                # Yield error as SSE event instead of crashing
                error_msg = f"data: {{\"error\": \"Connection failed: {str(e)}\"}}\n\n"
                yield error_msg.encode('utf-8')

            except httpx.TimeoutException as e:
                # Capture detailed timeout info
                error_detail = str(e) or repr(e) or "No error details available"
                logger.error(
                    "litellm_streaming_timeout",
                    error=error_detail,
                    error_type=type(e).__name__,
                    error_args=getattr(e, 'args', []),
                    url=url,
                    model=body.get("model", "unknown"),
                    message="Request timed out during streaming",
                    note="Check network connectivity to LLM proxy or increase timeouts"
                )
                error_msg = f"data: {{\"error\": \"Request timed out ({type(e).__name__}): {error_detail}\"}}\n\n"
                yield error_msg.encode('utf-8')

            except httpx.HTTPError as e:
                logger.error(
                    "litellm_streaming_http_error_general",
                    error=str(e),
                    error_type=type(e).__name__,
                    url=url,
                )
                error_msg = f"data: {{\"error\": \"HTTP error: {str(e)}\"}}\n\n"
                yield error_msg.encode('utf-8')

            except Exception as e:
                logger.error(
                    "litellm_streaming_unexpected_error",
                    error=str(e),
                    error_type=type(e).__name__,
                    url=url,
                    exc_info=True,
                )
                error_msg = f"data: {{\"error\": \"Unexpected error: {str(e)}\"}}\n\n"
                yield error_msg.encode('utf-8')

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
        )


class LiteLLMProxyServer:
    """Manager for running the LiteLLM proxy server in the same process."""

    def __init__(self, port: int = 0):
        """
        Initialize the proxy server.

        Args:
            port: Port to listen on (0 = auto-assign random port)
        """
        self.port = port
        self.actual_port: Optional[int] = None
        self.server_thread: Optional[threading.Thread] = None
        self.app: Optional[LiteLLMProxyApp] = None
        self._started = threading.Event()
        self._shutdown = threading.Event()

    def start(self) -> int:
        """
        Start the proxy server in a background thread.

        Returns:
            The actual port the server is listening on

        Raises:
            RuntimeError: If server fails to start
        """
        # Get LiteLLM configuration
        litellm_base_url = os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai")
        litellm_api_key = os.getenv("LITELLM_API_KEY")

        # Check for model override
        model_override = os.getenv("KUBIYA_MODEL_OVERRIDE")

        logger.info(
            "litellm_proxy_server_initializing",
            litellm_base_url=litellm_base_url,
            model_override=model_override,
            has_model_override=bool(model_override),
            note="Model override will be applied to ALL requests" if model_override else "No model override active"
        )

        if not litellm_api_key:
            raise RuntimeError("LITELLM_API_KEY not set")

        # Create proxy app
        self.app = LiteLLMProxyApp(litellm_base_url, litellm_api_key)

        # Auto-assign port if needed
        if self.port == 0:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', 0))
                s.listen(1)
                self.actual_port = s.getsockname()[1]
        else:
            self.actual_port = self.port

        # Start server in background thread
        self.server_thread = threading.Thread(
            target=self._run_server,
            daemon=True,
            name="LiteLLMProxyServer"
        )
        self.server_thread.start()

        # Wait for server to become ready by checking health endpoint
        import time
        import httpx
        max_wait = 10  # seconds
        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                # Try to connect to health endpoint
                with httpx.Client(timeout=1.0) as client:
                    response = client.get(f"http://127.0.0.1:{self.actual_port}/health")
                    if response.status_code == 200:
                        self._started.set()
                        logger.info(
                            "litellm_proxy_server_started",
                            port=self.actual_port,
                            url=f"http://127.0.0.1:{self.actual_port}",
                        )
                        return self.actual_port
            except Exception:
                # Server not ready yet, wait and retry
                time.sleep(0.1)
                continue

        # Timeout waiting for server
        raise RuntimeError("LiteLLM proxy server failed to start within 10 seconds")

    def _run_server(self):
        """Run the uvicorn server (called in background thread)."""
        try:
            # Create event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Create uvicorn config
            config = uvicorn.Config(
                self.app.app,
                host="127.0.0.1",
                port=self.actual_port,
                log_level="error",
                access_log=False,
                loop=loop,
            )
            server = uvicorn.Server(config)

            # Run server
            loop.run_until_complete(server.serve())

        except Exception as e:
            logger.error(
                "litellm_proxy_server_error",
                error=str(e),
                error_type=type(e).__name__,
                exc_info=True,
            )
        finally:
            # Cleanup HTTP client
            if self.app and self.app.client:
                try:
                    loop.run_until_complete(self.app.cleanup())
                except Exception as cleanup_error:
                    logger.error(
                        "proxy_app_cleanup_failed",
                        error=str(cleanup_error)
                    )

            # Close event loop
            try:
                loop.close()
            except Exception as loop_error:
                logger.error("event_loop_close_failed", error=str(loop_error))

            self._shutdown.set()

    def stop(self):
        """Stop the proxy server and cleanup resources."""
        logger.info("stopping_litellm_proxy_server")
        self._shutdown.set()

        # Give server time to shutdown gracefully
        if self.server_thread:
            self.server_thread.join(timeout=10)

            if self.server_thread.is_alive():
                logger.warning(
                    "proxy_server_thread_still_alive",
                    note="Daemon thread will be terminated by Python at exit"
                )
            else:
                logger.info("proxy_server_thread_stopped")

        logger.info("litellm_proxy_server_stopped")

    def get_base_url(self) -> str:
        """Get the base URL of the proxy server."""
        if not self.actual_port:
            raise RuntimeError("Server not started")
        return f"http://127.0.0.1:{self.actual_port}"


# Singleton instance
_proxy_server: Optional[LiteLLMProxyServer] = None
_proxy_lock = threading.Lock()


def get_proxy_server() -> LiteLLMProxyServer:
    """
    Get or create the singleton proxy server instance.

    Returns:
        LiteLLMProxyServer instance
    """
    global _proxy_server

    with _proxy_lock:
        if _proxy_server is None:
            _proxy_server = LiteLLMProxyServer(port=0)  # Auto-assign port
            _proxy_server.start()

        return _proxy_server


def set_execution_context(execution_id: str, context: Dict[str, Any]):
    """
    Store execution context for metadata injection.

    Call this before starting a Claude Code execution.

    Args:
        execution_id: Execution ID
        context: Context dict with user_id, session_id, agent_id, etc.
    """
    _context_store.set_context(execution_id, context)


def clear_execution_context(
    execution_id: str,
    immediate: bool = False,
    delay_seconds: float = 5.0
):
    """
    Clear execution context after execution completes.

    Args:
        execution_id: Execution ID
        immediate: If True, clear immediately. If False, schedule delayed cleanup.
        delay_seconds: Delay before cleanup (only if immediate=False)
    """
    if immediate:
        _context_store.clear_context(execution_id)
    else:
        _cleanup_scheduler.schedule_cleanup(
            execution_id,
            delay_seconds,
            _context_store
        )


def get_proxy_base_url() -> str:
    """
    Get the base URL of the local proxy server.

    Starts the server if not already running.

    Returns:
        Base URL (e.g., "http://127.0.0.1:8080")
    """
    server = get_proxy_server()
    return server.get_base_url()


def list_available_models_sync(timeout: float = 10.0) -> List[str]:
    """
    Synchronously fetch and return available models from upstream LiteLLM proxy.

    This is useful for CLI/debugging to show what models are available.

    Args:
        timeout: Request timeout in seconds

    Returns:
        List of available model IDs
    """
    litellm_base_url = os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai")
    litellm_api_key = os.getenv("LITELLM_API_KEY")

    if not litellm_api_key:
        logger.warning("cannot_list_models_no_api_key")
        return []

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(
                f"{litellm_base_url.rstrip('/')}/v1/models",
                headers={"Authorization": f"Bearer {litellm_api_key}"},
            )

            if response.status_code == 200:
                data = response.json()
                models = []
                if "data" in data and isinstance(data["data"], list):
                    models = [m.get("id") for m in data["data"] if m.get("id")]

                logger.info(
                    "listed_available_models_sync",
                    model_count=len(models),
                    models=models,
                    litellm_base_url=litellm_base_url,
                )
                return models
            else:
                logger.warning(
                    "failed_to_list_models_sync",
                    status_code=response.status_code,
                    litellm_base_url=litellm_base_url,
                )
                return []

    except Exception as e:
        logger.warning(
            "error_listing_models_sync",
            error=str(e),
            error_type=type(e).__name__,
            litellm_base_url=litellm_base_url,
        )
        return []


def print_available_models():
    """
    Print available models to stdout for debugging.

    Useful for CLI troubleshooting when model errors occur.
    """
    models = list_available_models_sync()
    litellm_base_url = os.getenv("LITELLM_API_BASE", "https://llm-proxy.kubiya.ai")

    print(f"\n{'='*60}")
    print(f"Available Models from LiteLLM Proxy")
    print(f"Proxy URL: {litellm_base_url}")
    print(f"{'='*60}")

    if models:
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
    else:
        print("  No models available or failed to fetch models.")
        print("  Check LITELLM_API_BASE and LITELLM_API_KEY environment variables.")

    print(f"{'='*60}\n")
