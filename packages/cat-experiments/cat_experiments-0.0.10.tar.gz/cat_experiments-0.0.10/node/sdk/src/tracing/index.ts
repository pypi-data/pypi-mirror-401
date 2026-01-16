/**
 * Tracing helpers for capturing tool calls from OTEL-instrumented code.
 *
 * This module provides helpers for capturing tool calls from OpenTelemetry-
 * instrumented code during task execution.
 *
 * Example usage in a task:
 *
 *     import { defineExperiment } from "cat-experiments";
 *     import { captureToolCalls } from "cat-experiments/tracing";
 *
 *     export default defineExperiment({
 *       task: async (input) => {
 *         const captured = await captureToolCalls(async () => {
 *           return await myAgent.run(input.input.question);
 *         });
 *
 *         return {
 *           output: {
 *             answer: captured.result,
 *             tool_calls: captured.toolCalls,
 *           },
 *         };
 *       },
 *       // ...
 *     });
 */

import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import type {
  ReadableSpan,
  SpanProcessor,
} from "@opentelemetry/sdk-trace-base";

import {
  type ToolCall,
  type ToolCallExtractor,
  DEFAULT_EXTRACTORS,
  OpenInferenceExtractor,
  OpenLLMetryExtractor,
  GenericToolSpanExtractor,
} from "./extractors.js";

export type { ToolCall, ToolCallExtractor };
export {
  DEFAULT_EXTRACTORS,
  OpenInferenceExtractor,
  OpenLLMetryExtractor,
  GenericToolSpanExtractor,
};

/**
 * Result of capturing tool calls during execution.
 */
export interface CaptureResult<T> {
  /** The result of the captured function */
  result: T;
  /** Tool calls captured during execution */
  toolCalls: ToolCall[];
}

/**
 * Options for captureToolCalls.
 */
export interface CaptureOptions {
  /** Custom extractors to use instead of defaults */
  extractors?: ToolCallExtractor[];
}

// Storage for collected tool calls per capture session
const toolCallStorage = new Map<string, ToolCall[]>();
let currentCaptureId: string | null = null;

// Global state for provider setup
let providerSetupDone = false;

/**
 * Span processor that collects tool calls from OTEL spans.
 */
class ToolCallCollectorProcessor implements SpanProcessor {
  constructor(private extractors: ToolCallExtractor[]) {}

  onStart(): void {
    // No-op
  }

  onEnd(span: ReadableSpan): void {
    if (!currentCaptureId) {
      return;
    }

    const attributes: Record<string, unknown> = {};
    if (span.attributes) {
      for (const [key, value] of Object.entries(span.attributes)) {
        attributes[key] = value;
      }
    }

    // Try each extractor until one handles the span
    for (const extractor of this.extractors) {
      if (extractor.canHandle(span, attributes)) {
        const toolCalls = extractor.extract(span, attributes);
        if (toolCalls.length > 0) {
          const existing = toolCallStorage.get(currentCaptureId) ?? [];
          existing.push(...toolCalls);
          toolCallStorage.set(currentCaptureId, existing);
        }
        break; // Only use first matching extractor
      }
    }
  }

  shutdown(): Promise<void> {
    return Promise.resolve();
  }

  forceFlush(): Promise<void> {
    return Promise.resolve();
  }
}

/**
 * Set up tracing infrastructure for tool call capture.
 *
 * This creates a TracerProvider with our tool call collector if one doesn't exist.
 * Call this BEFORE any instrumentors (e.g., OpenInference) are set up.
 */
export function setupTracing(extractors?: ToolCallExtractor[]): void {
  if (providerSetupDone) {
    return;
  }

  const collectorProcessor = new ToolCallCollectorProcessor(
    extractors ?? DEFAULT_EXTRACTORS,
  );

  // Create a new provider with our collector
  const provider = new NodeTracerProvider({
    spanProcessors: [collectorProcessor],
  });

  // Register as global provider
  provider.register();
  providerSetupDone = true;
}

/**
 * Generate a unique capture ID.
 */
function generateCaptureId(): string {
  return `capture-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

/**
 * Capture tool calls from OTEL-instrumented code.
 *
 * Use this function in your task to automatically capture tool calls made
 * by instrumented libraries (e.g., OpenAI via OpenInference).
 *
 * @example
 * ```typescript
 * import { captureToolCalls } from "cat-experiments/tracing";
 *
 * const captured = await captureToolCalls(async () => {
 *   return await myAgent.run(question);
 * });
 *
 * console.log(captured.toolCalls);
 * // [{ name: "search", args: { query: "..." } }, ...]
 * ```
 *
 * @param fn - The async function to execute while capturing tool calls
 * @param options - Optional configuration
 * @returns The function result along with captured tool calls
 */
export async function captureToolCalls<T>(
  fn: () => Promise<T>,
  options?: CaptureOptions,
): Promise<CaptureResult<T>> {
  // Ensure tracing infrastructure is set up
  setupTracing(options?.extractors);

  const captureId = generateCaptureId();
  toolCallStorage.set(captureId, []);

  // Set current capture ID
  const previousCaptureId = currentCaptureId;
  currentCaptureId = captureId;

  try {
    const result = await fn();
    const toolCalls = toolCallStorage.get(captureId) ?? [];
    return { result, toolCalls };
  } finally {
    // Restore previous capture ID
    currentCaptureId = previousCaptureId;
    // Clean up storage
    toolCallStorage.delete(captureId);
  }
}

/**
 * Check if OpenTelemetry is available.
 */
export const OTEL_AVAILABLE = true;
