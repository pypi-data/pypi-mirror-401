"""OpenTelemetry helpers for capturing tool calls during task execution.

This module provides the capture_tool_calls() context manager that captures
tool calls from OTEL-instrumented code (e.g., OpenAI via OpenInference).

The actual extraction logic is delegated to pluggable extractors in the
extractors module, allowing support for different instrumentation libraries.

Key design: We use OTEL trace IDs (not ContextVars) to track which tool calls
belong to which capture session. This ensures tool calls are captured even when
the instrumented code runs in separate threads or async contexts, as long as
they're part of the same trace.
"""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, Iterator, List, Optional, Set

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.trace import format_trace_id

from .extractors import DEFAULT_EXTRACTORS, ToolCallExtractor

logger = logging.getLogger(__name__)

# Storage for collected tool calls per trace ID
_TOOL_CALLS: Dict[str, List[dict[str, Any]]] = {}
_TOOL_CALL_LOCK = Lock()

# Set of trace IDs we're actively capturing
_ACTIVE_TRACE_IDS: Set[str] = set()
_ACTIVE_TRACE_LOCK = Lock()


@dataclass
class ToolCallCapture:
    """Container for captured tool calls."""

    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    _trace_id: str = field(default="", repr=False)


class ToolCallCollectorProcessor(SpanProcessor):
    """Span processor that collects tool calls from OTEL spans.

    Uses pluggable extractors to support different instrumentation libraries.
    Tool calls are collected based on trace ID, which propagates correctly
    across threads and async contexts.
    """

    def __init__(self, extractors: list[ToolCallExtractor] | None = None):
        """Initialize with extractors.

        Args:
            extractors: List of extractors to try, in priority order.
                       Defaults to DEFAULT_EXTRACTORS.
        """
        self.extractors = extractors if extractors is not None else DEFAULT_EXTRACTORS

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

        attributes = dict(span.attributes or {})

        # Try each extractor until one handles the span
        for extractor in self.extractors:
            if extractor.can_handle(span, attributes):
                tool_calls = extractor.extract(span, attributes)
                if tool_calls:
                    with _TOOL_CALL_LOCK:
                        _TOOL_CALLS.setdefault(trace_id, []).extend(tool_calls)
                break  # Only use first matching extractor

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


def _consume_collected_tool_calls(trace_id: str) -> list[dict[str, Any]]:
    """Return and clear collected tool calls for a trace."""
    with _TOOL_CALL_LOCK:
        return _TOOL_CALLS.pop(trace_id, [])


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
_collector_processor: Optional[ToolCallCollectorProcessor] = None
_provider_setup_done = False


def _ensure_tracing_setup(
    extractors: list[ToolCallExtractor] | None = None,
) -> None:
    """Set up tracing infrastructure for tool call capture.

    This creates a TracerProvider with our tool call collector if one doesn't exist.
    IMPORTANT: This should be called BEFORE any instrumentors (e.g., OpenInference)
    are set up, so that spans from instrumented libraries are captured.

    Args:
        extractors: Optional list of extractors to use. Defaults to DEFAULT_EXTRACTORS.
    """
    global _collector_processor, _provider_setup_done

    if _provider_setup_done:
        return

    provider = trace.get_tracer_provider()

    # If there's already a real TracerProvider, add our processor to it
    if isinstance(provider, TracerProvider):
        _collector_processor = ToolCallCollectorProcessor(extractors)
        provider.add_span_processor(_collector_processor)
        _provider_setup_done = True
        logger.debug("Added tool call collector to existing TracerProvider")
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

    # Add our tool call collector
    _collector_processor = ToolCallCollectorProcessor(extractors)
    new_provider.add_span_processor(_collector_processor)

    # Set as global provider
    trace.set_tracer_provider(new_provider)
    _provider_setup_done = True
    logger.debug("Created TracerProvider with tool call collector")


# Get a tracer for creating capture spans
_tracer: Optional[trace.Tracer] = None


def _get_tracer() -> trace.Tracer:
    """Get or create the tracer for capture spans."""
    global _tracer
    if _tracer is None:
        _tracer = trace.get_tracer("cat.experiments.tracing")
    return _tracer


def configure_tracing(
    extractors: list[ToolCallExtractor] | None = None,
) -> None:
    """Configure tracing infrastructure for tool call capture.

    Call this once at application startup to customize extractors. If not called,
    default extractors will be used automatically when capture_tool_calls() is
    first invoked.

    IMPORTANT: This must be called BEFORE any instrumentors (e.g., OpenInference)
    are set up, so that spans from instrumented libraries are captured.

    Args:
        extractors: List of extractors to use for tool call extraction.
                   Defaults to DEFAULT_EXTRACTORS which includes OpenInference,
                   GenAI, and generic tool span support.

    Raises:
        RuntimeError: If tracing has already been configured.

    Example:
        from cat.experiments.tracing import configure_tracing, capture_tool_calls
        from cat.experiments.tracing.extractors import OpenInferenceExtractor

        # At startup, before instrumentors
        configure_tracing(extractors=[OpenInferenceExtractor()])

        # Later, in task code
        with capture_tool_calls() as captured:
            ...
    """
    if _provider_setup_done:
        raise RuntimeError(
            "Tracing has already been configured. "
            "configure_tracing() must be called before any capture_tool_calls() invocations."
        )
    _ensure_tracing_setup(extractors)


@contextmanager
def capture_tool_calls() -> Iterator[ToolCallCapture]:
    """Capture tool calls from OTEL-instrumented code.

    Use this context manager in your @task function to automatically capture
    tool calls made by instrumented libraries (e.g., OpenAI via OpenInference).

    Tool calls are captured based on OTEL trace ID, which means they will be
    captured even if the instrumented code runs in separate threads or async
    contexts, as long as they propagate the trace context.

    To customize extractors, call configure_tracing() before first use.

    Example:
        from cat.experiments import task, TaskInput, TaskOutput
        from cat.experiments.tracing import capture_tool_calls

        @task
        async def my_task(input: TaskInput) -> TaskOutput:
            with capture_tool_calls() as captured:
                result = await my_agent.run(input.input["question"])

            return TaskOutput(output={
                "answer": result,
                "tool_calls": captured.tool_calls,
            })

    Yields:
        ToolCallCapture containing the captured tool calls after the context exits
    """
    # Ensure tracing infrastructure is set up (uses defaults if configure_tracing wasn't called)
    _ensure_tracing_setup()

    tracer = _get_tracer()

    # Create a span to establish the trace context
    # All child spans (from instrumented code) will inherit this trace ID
    with tracer.start_as_current_span("cat.capture_tool_calls") as span:
        span_context = span.get_span_context()
        trace_id = format_trace_id(span_context.trace_id)

        capture = ToolCallCapture(_trace_id=trace_id)

        # Register this trace ID for collection
        with _ACTIVE_TRACE_LOCK:
            _ACTIVE_TRACE_IDS.add(trace_id)

        try:
            yield capture
        finally:
            # Unregister the trace ID
            with _ACTIVE_TRACE_LOCK:
                _ACTIVE_TRACE_IDS.discard(trace_id)

            # Collect tool calls into the capture object
            capture.tool_calls = _consume_collected_tool_calls(trace_id)
