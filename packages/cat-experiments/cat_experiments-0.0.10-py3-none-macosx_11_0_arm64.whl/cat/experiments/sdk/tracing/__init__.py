"""Tracing helpers with optional OpenTelemetry dependencies.

This module provides helpers for capturing tool calls from OTEL-instrumented
code during task execution. It requires the 'tracing' extra to be installed:

    pip install cat-experiments[tracing]

Example usage in a task:

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

Custom extractors:

    To use custom extractors, call configure_tracing() once at startup
    before any capture_tool_calls() invocations:

    from cat.experiments.tracing import configure_tracing, capture_tool_calls
    from cat.experiments.tracing.extractors import OpenInferenceExtractor

    # At application startup
    configure_tracing(extractors=[OpenInferenceExtractor()])

    # Later, in task code
    with capture_tool_calls() as captured:
        ...
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Iterator, List

if TYPE_CHECKING:  # pragma: no cover - typing only
    from . import _otel as _otel_module
    from .extractors import ToolCallExtractor

try:  # pragma: no cover - exercised via tracing extra
    from . import _otel as _otel_module
    from .extractors import (
        DEFAULT_EXTRACTORS,
        GenAIExtractor,
        GenericToolSpanExtractor,
        OpenInferenceExtractor,
        OpenLLMetryExtractor,
        ToolCallExtractor,
    )
except ImportError:  # pragma: no cover - fallback path when extras missing
    _otel_module = None  # type: ignore[assignment]
    # Provide stub types when OTEL not available
    DEFAULT_EXTRACTORS = []  # type: ignore[misc]
    GenAIExtractor = None  # type: ignore[assignment,misc]
    GenericToolSpanExtractor = None  # type: ignore[assignment,misc]
    OpenInferenceExtractor = None  # type: ignore[assignment,misc]
    OpenLLMetryExtractor = None  # type: ignore[assignment,misc]
    ToolCallExtractor = None  # type: ignore[assignment,misc]


@dataclass
class ToolCallCapture:
    """Container for captured tool calls."""

    tool_calls: list[dict[str, Any]] = field(default_factory=list)


if _otel_module is not None:
    # OTEL is available - use real implementation
    capture_tool_calls = _otel_module.capture_tool_calls
    configure_tracing = _otel_module.configure_tracing
    OTEL_AVAILABLE = True
else:
    # OTEL not available - provide no-op fallback
    @contextmanager
    def _noop_capture_tool_calls() -> Iterator[ToolCallCapture]:
        """No-op tool call capture when OTEL is not available.

        Returns an empty ToolCallCapture - tool calls won't be captured
        but the code will still work.
        """
        yield ToolCallCapture()

    def _noop_configure_tracing(extractors: List[Any] | None = None) -> None:
        """No-op tracing configuration when OTEL is not available."""
        pass

    capture_tool_calls = _noop_capture_tool_calls
    capture_tool_calls.__module__ = __name__
    configure_tracing = _noop_configure_tracing
    OTEL_AVAILABLE = False


__all__ = [
    # Core API
    "ToolCallCapture",
    "capture_tool_calls",
    "configure_tracing",
    "OTEL_AVAILABLE",
    # Extractors (for custom configurations)
    "ToolCallExtractor",
    "OpenInferenceExtractor",
    "GenAIExtractor",
    "OpenLLMetryExtractor",
    "GenericToolSpanExtractor",
    "DEFAULT_EXTRACTORS",
]
