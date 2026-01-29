"""OpenTelemetry helpers for capturing trace data during task execution.

This module provides the capture_trace() context manager that captures
all OTEL spans from instrumented code (e.g., OpenAI Agents SDK).

The raw span data can then be processed by extraction helpers to get
specific information like tool calls, retrieval context, messages, etc.

Key design: We use OTEL trace IDs to track which spans belong to which
capture session. This ensures spans are captured even when the instrumented
code runs in separate threads or async contexts, as long as they're part
of the same trace.
"""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, Iterator, List, Optional, Set

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.trace import format_span_id, format_trace_id

logger = logging.getLogger(__name__)

# Storage for collected spans per trace ID
_SPANS: Dict[str, List[dict[str, Any]]] = {}
_SPANS_LOCK = Lock()

# Set of trace IDs we're actively capturing
_ACTIVE_TRACE_IDS: Set[str] = set()
_ACTIVE_TRACE_LOCK = Lock()


def _timestamp_to_iso(timestamp_ns: int) -> str:
    """Convert OTEL nanosecond timestamp to ISO 8601 string."""
    dt = datetime.fromtimestamp(timestamp_ns / 1e9, tz=timezone.utc)
    return dt.isoformat()


def _span_to_dict(span: ReadableSpan) -> dict[str, Any]:
    """Convert a ReadableSpan to a serializable dictionary.

    Args:
        span: The OTEL span to convert.

    Returns:
        Dictionary containing span data with ISO timestamps.
    """
    span_context = span.get_span_context()
    parent = span.parent

    return {
        "name": span.name,
        "trace_id": format_trace_id(span_context.trace_id) if span_context else None,
        "span_id": format_span_id(span_context.span_id) if span_context else None,
        "parent_span_id": format_span_id(parent.span_id) if parent else None,
        "start_time": _timestamp_to_iso(span.start_time) if span.start_time else None,
        "end_time": _timestamp_to_iso(span.end_time) if span.end_time else None,
        "status": span.status.status_code.name if span.status else None,
        "attributes": dict(span.attributes) if span.attributes else {},
    }


@dataclass
class TraceCapture:
    """Container for captured trace data."""

    spans: list[dict[str, Any]] = field(default_factory=list)


class SpanCollectorProcessor(SpanProcessor):
    """Span processor that collects all spans belonging to active traces.

    Spans are collected based on trace ID, which propagates correctly
    across threads and async contexts.
    """

    def on_start(self, span: ReadableSpan, parent_context: Any = None) -> None:
        pass

    def on_end(self, span: ReadableSpan) -> None:
        # Get trace ID from the span's context
        span_context = span.get_span_context()
        if not span_context or not span_context.is_valid:
            return

        trace_id = format_trace_id(span_context.trace_id)

        # Only collect if this trace is being actively captured
        with _ACTIVE_TRACE_LOCK:
            if trace_id not in _ACTIVE_TRACE_IDS:
                return

        # Convert span to dict and store
        span_dict = _span_to_dict(span)
        with _SPANS_LOCK:
            _SPANS.setdefault(trace_id, []).append(span_dict)

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


def _consume_collected_spans(trace_id: str) -> list[dict[str, Any]]:
    """Return and clear collected spans for a trace."""
    with _SPANS_LOCK:
        return _SPANS.pop(trace_id, [])


def _parse_otlp_headers(header_str: str) -> dict[str, str]:
    """Parse OTEL_EXPORTER_OTLP_HEADERS environment variable."""
    headers: dict[str, str] = {}
    for pair in header_str.split(","):
        if not pair.strip() or "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        headers[key.strip()] = value.strip()
    return headers


# Global collector processor - added once to the tracer provider
_collector_processor: Optional[SpanCollectorProcessor] = None
_provider_setup_done = False


def _ensure_tracing_setup() -> None:
    """Set up tracing infrastructure for span capture.

    This creates a TracerProvider with our span collector if one doesn't exist.
    IMPORTANT: This should be called BEFORE any instrumentors (e.g., OpenInference)
    are set up, so that spans from instrumented libraries are captured.
    """
    global _collector_processor, _provider_setup_done

    if _provider_setup_done:
        return

    provider = trace.get_tracer_provider()

    # If there's already a real TracerProvider, add our processor to it
    if isinstance(provider, TracerProvider):
        _collector_processor = SpanCollectorProcessor()
        provider.add_span_processor(_collector_processor)
        _provider_setup_done = True
        logger.debug("Added span collector to existing TracerProvider")
        return

    # Create a new TracerProvider with our collector
    resource = Resource({SERVICE_NAME: "cat-experiments"})
    new_provider = TracerProvider(resource=resource)

    # Add OTLP exporter if configured
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        try:
            headers = _parse_otlp_headers(os.getenv("OTEL_EXPORTER_OTLP_HEADERS", ""))
            new_provider.add_span_processor(
                SimpleSpanProcessor(OTLPSpanExporter(endpoint=endpoint, headers=headers))
            )
        except Exception as exc:
            logger.debug("Failed to configure OTLP exporter: %s", exc)

    # Add our span collector
    _collector_processor = SpanCollectorProcessor()
    new_provider.add_span_processor(_collector_processor)

    # Set as global provider
    trace.set_tracer_provider(new_provider)
    _provider_setup_done = True
    logger.debug("Created TracerProvider with span collector")


# Get a tracer for creating capture spans
_tracer: Optional[trace.Tracer] = None


def _get_tracer() -> trace.Tracer:
    """Get or create the tracer for capture spans."""
    global _tracer
    if _tracer is None:
        _tracer = trace.get_tracer("cat.experiments.tracing")
    return _tracer


def configure_tracing() -> None:
    """Configure tracing infrastructure for span capture.

    Call this once at application startup to set up the tracing provider.
    If not called, tracing will be configured automatically when capture_trace()
    is first invoked.

    IMPORTANT: This must be called BEFORE any instrumentors (e.g., OpenInference)
    are set up, so that spans from instrumented libraries are captured.

    Raises:
        RuntimeError: If tracing has already been configured.

    Example:
        from cat.experiments.tracing import configure_tracing, capture_trace

        # At startup, before instrumentors
        configure_tracing()

        # Later, in task code
        with capture_trace() as trace:
            ...
    """
    if _provider_setup_done:
        raise RuntimeError(
            "Tracing has already been configured. "
            "configure_tracing() must be called before any capture_trace() invocations."
        )
    _ensure_tracing_setup()


@contextmanager
def capture_trace() -> Iterator[TraceCapture]:
    """Capture all OTEL spans from instrumented code.

    Use this context manager in your @task function to automatically capture
    spans made by instrumented libraries (e.g., OpenAI Agents SDK).

    Spans are captured based on OTEL trace ID, which means they will be
    captured even if the instrumented code runs in separate threads or async
    contexts, as long as they propagate the trace context.

    The captured spans can then be processed using extraction helpers like
    extract_tool_calls() or extract_retrieval_context().

    Example:
        from cat.experiments import task, TaskInput, TaskOutput
        from cat.experiments.tracing import capture_trace, extract_tool_calls

        @task
        async def my_task(input: TaskInput) -> TaskOutput:
            with capture_trace() as trace:
                result = await my_agent.run(input.input["question"])

            return TaskOutput(output={
                "answer": result,
                "tool_calls": extract_tool_calls(trace.spans),
                "trace": trace.spans,  # Raw spans for custom analysis
            })

    Yields:
        TraceCapture containing the captured spans after the context exits
    """
    # Ensure tracing infrastructure is set up
    _ensure_tracing_setup()

    tracer = _get_tracer()

    # Create a span to establish the trace context
    # All child spans (from instrumented code) will inherit this trace ID
    with tracer.start_as_current_span("cat.capture_trace") as span:
        span_context = span.get_span_context()
        trace_id = format_trace_id(span_context.trace_id)

        capture = TraceCapture()

        # Register this trace ID for collection
        with _ACTIVE_TRACE_LOCK:
            _ACTIVE_TRACE_IDS.add(trace_id)

        try:
            yield capture
        finally:
            # Unregister the trace ID
            with _ACTIVE_TRACE_LOCK:
                _ACTIVE_TRACE_IDS.discard(trace_id)

            # Collect spans into the capture object
            capture.spans = _consume_collected_spans(trace_id)
