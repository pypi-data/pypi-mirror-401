"""Tool call extractors for different instrumentation libraries.

Each extractor knows how to pull tool call information from spans created
by a specific instrumentation library (OpenInference, OpenLLMetry, etc.).
"""

from __future__ import annotations

import json
import re
from typing import Any, Protocol

from opentelemetry.sdk.trace import ReadableSpan


class ToolCallExtractor(Protocol):
    """Protocol for tool call extractors."""

    def can_handle(self, span: ReadableSpan, attributes: dict[str, Any]) -> bool:
        """Check if this extractor can handle the given span."""
        ...

    def extract(self, span: ReadableSpan, attributes: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool calls from the span. Returns empty list if none found."""
        ...


class OpenInferenceExtractor:
    """Extracts tool calls from OpenInference-instrumented spans.

    OpenInference (used by Phoenix, Arize) stores tool calls in LLM span attributes:
        'llm.output_messages.0.message.tool_calls.0.tool_call.function.name'
        'llm.output_messages.0.message.tool_calls.0.tool_call.function.arguments'
        'llm.output_messages.0.message.tool_calls.0.tool_call.id'
    """

    # Pattern to find tool call function names in attributes
    _TOOL_CALL_PATTERN = re.compile(
        r"llm\.output_messages\.(\d+)\.message\.tool_calls\.(\d+)\.tool_call\.function\.name"
    )

    def can_handle(self, span: ReadableSpan, attributes: dict[str, Any]) -> bool:
        """Check if span has OpenInference tool call attributes."""
        return any("tool_calls" in key and "function.name" in key for key in attributes.keys())

    def extract(self, span: ReadableSpan, attributes: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool calls from OpenInference LLM span attributes."""
        tool_calls: list[dict[str, Any]] = []

        # Find all tool call indices
        found_indices: set[tuple[int, int]] = set()
        for key in attributes.keys():
            match = self._TOOL_CALL_PATTERN.match(key)
            if match:
                msg_idx = int(match.group(1))
                tc_idx = int(match.group(2))
                found_indices.add((msg_idx, tc_idx))

        # Extract each tool call
        for msg_idx, tc_idx in sorted(found_indices):
            prefix = f"llm.output_messages.{msg_idx}.message.tool_calls.{tc_idx}.tool_call"

            name = attributes.get(f"{prefix}.function.name", "")
            args_str = attributes.get(f"{prefix}.function.arguments", "{}")
            call_id = attributes.get(f"{prefix}.id")

            try:
                args = json.loads(args_str) if args_str else {}
            except (json.JSONDecodeError, TypeError):
                args = {}

            if name:
                tool_call: dict[str, Any] = {"name": name, "args": args}
                if call_id:
                    tool_call["id"] = call_id
                tool_calls.append(tool_call)

        return tool_calls


class GenAIExtractor:
    """Extracts tool calls from GenAI semantic convention spans.

    This handles the OpenTelemetry GenAI semantic conventions used by
    opentelemetry-instrumentation-openai-agents and similar instrumentors.

    Tool calls are stored in attributes like:
        'gen_ai.completion.0.tool_calls.0.name'
        'gen_ai.completion.0.tool_calls.0.arguments'
        'gen_ai.completion.0.tool_calls.0.id'
    """

    # Pattern to find tool call names in gen_ai attributes
    _TOOL_CALL_PATTERN = re.compile(r"gen_ai\.completion\.(\d+)\.tool_calls\.(\d+)\.name")

    def can_handle(self, span: ReadableSpan, attributes: dict[str, Any]) -> bool:
        """Check if span has GenAI tool call attributes."""
        return any(
            key.startswith("gen_ai.completion.") and ".tool_calls." in key and key.endswith(".name")
            for key in attributes.keys()
        )

    def extract(self, span: ReadableSpan, attributes: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool calls from GenAI semantic convention attributes."""
        tool_calls: list[dict[str, Any]] = []

        # Find all tool call indices
        found_indices: set[tuple[int, int]] = set()
        for key in attributes.keys():
            match = self._TOOL_CALL_PATTERN.match(key)
            if match:
                completion_idx = int(match.group(1))
                tc_idx = int(match.group(2))
                found_indices.add((completion_idx, tc_idx))

        # Extract each tool call
        for completion_idx, tc_idx in sorted(found_indices):
            prefix = f"gen_ai.completion.{completion_idx}.tool_calls.{tc_idx}"

            name = attributes.get(f"{prefix}.name", "")
            args_str = attributes.get(f"{prefix}.arguments", "{}")
            call_id = attributes.get(f"{prefix}.id")

            try:
                args = json.loads(args_str) if args_str else {}
            except (json.JSONDecodeError, TypeError):
                args = {}

            if name:
                tool_call: dict[str, Any] = {"name": name, "args": args}
                if call_id:
                    tool_call["id"] = call_id
                tool_calls.append(tool_call)

        return tool_calls


class OpenLLMetryExtractor:
    """Extracts tool calls from OpenLLMetry-instrumented spans.

    OpenLLMetry (Traceloop) uses different attribute conventions.
    This is a placeholder - implement based on actual OpenLLMetry format.
    """

    def can_handle(self, span: ReadableSpan, attributes: dict[str, Any]) -> bool:
        """Check if span has OpenLLMetry tool call attributes."""
        # OpenLLMetry uses 'traceloop.' prefix for its attributes
        return any(key.startswith("traceloop.") for key in attributes.keys())

    def extract(self, span: ReadableSpan, attributes: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool calls from OpenLLMetry span attributes."""
        # TODO: Implement based on actual OpenLLMetry attribute format
        # For now, return empty - users can contribute the implementation
        return []


class GenericToolSpanExtractor:
    """Fallback extractor for generic tool/function spans.

    Handles spans that are explicitly named as tool or function calls,
    rather than LLM spans that contain tool calls in their output.
    """

    def can_handle(self, span: ReadableSpan, attributes: dict[str, Any]) -> bool:
        """Check if span looks like a direct tool/function call."""
        # Skip LLM spans - they should be handled by library-specific extractors
        if attributes.get("openinference.span.kind") == "LLM":
            return False

        span_name = span.name.lower()
        return (
            "function" in span_name
            or "tool" in span_name
            or any(key.startswith("tool.") for key in attributes.keys())
            or "function_call" in attributes
        )

    def extract(self, span: ReadableSpan, attributes: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool call from a generic tool span."""
        from opentelemetry.trace import StatusCode

        name = span.name
        args: dict[str, Any] = {}
        result = attributes.get("output.value", attributes.get("result", ""))

        # Try to extract arguments from attributes
        for key, value in attributes.items():
            if key.startswith("input.") and key != "input.value":
                arg_name = key.replace("input.", "")
                args[arg_name] = value

        # Calculate execution time
        duration_ns = (span.end_time or 0) - (span.start_time or 0)
        execution_time_ms = duration_ns / 1_000_000

        # Check for errors
        error = None
        if span.status.status_code == StatusCode.ERROR:
            error = span.status.description

        return [
            {
                "name": name,
                "args": args,
                "result": result,
                "error": error,
                "execution_time_ms": execution_time_ms,
            }
        ]


# Default extractors in priority order
# More specific extractors should come before generic ones
DEFAULT_EXTRACTORS: list[ToolCallExtractor] = [
    OpenInferenceExtractor(),
    GenAIExtractor(),
    OpenLLMetryExtractor(),
    GenericToolSpanExtractor(),
]
