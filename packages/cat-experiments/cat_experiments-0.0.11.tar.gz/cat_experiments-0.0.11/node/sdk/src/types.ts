/**
 * Protocol types for cat-experiments.
 *
 * These types define the JSON-serializable data structures that flow between
 * the Go CLI orchestrator and the Node executor. They mirror the Python
 * protocol types for cross-language compatibility.
 */

// -----------------------------------------------------------------------------
// Task Protocol Types
// -----------------------------------------------------------------------------

/**
 * Input to a task function.
 *
 * @template TInput - Type of the input data from the dataset example
 */
export interface TaskInput<TInput = Record<string, unknown>> {
  /** Unique identifier for the dataset example */
  id: string;

  /** Input data from the dataset example */
  input: TInput;

  /** Expected output from the dataset example (for reference) */
  output?: Record<string, unknown>;

  /** Metadata from the dataset example */
  metadata?: Record<string, unknown>;

  /** Experiment identifier */
  experiment_id?: string;

  /** Unique run identifier (example_id#repetition) */
  run_id?: string;

  /** Repetition number (1-based) */
  repetition_number?: number;

  /** User-defined experiment parameters */
  params: Record<string, unknown>;
}

/**
 * Output from a task function.
 *
 * @template TOutput - Type of the task output
 */
export interface TaskOutput<TOutput = unknown> {
  /** The task result */
  output: TOutput;

  /** Optional metadata about the execution */
  metadata?: Record<string, unknown>;

  /** Error message if the task failed */
  error?: string;
}

// -----------------------------------------------------------------------------
// Evaluator Protocol Types
// -----------------------------------------------------------------------------

/**
 * Input to an evaluator function.
 *
 * @template TInput - Type of the original input data
 * @template TOutput - Type of the actual output from the task
 */
export interface EvalInput<
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _TInput = Record<string, unknown>,
  TOutput = unknown,
> {
  /** The original task input as a dictionary */
  example: Record<string, unknown>;

  /** The actual output produced by the task */
  actual_output: TOutput;

  /** The expected output from the dataset (if available) */
  expected_output?: Record<string, unknown>;

  /** Metadata from the task execution */
  task_metadata?: Record<string, unknown>;

  /** User-defined experiment parameters */
  params: Record<string, unknown>;
}

/**
 * Output from an evaluator function.
 */
export interface EvalOutput {
  /** Numerical score (typically 0.0 to 1.0, but not enforced) */
  score: number;

  /** Optional categorical label (e.g., "pass", "fail", "correct") */
  label?: string;

  /** Optional metadata about the evaluation */
  metadata?: Record<string, unknown>;
}

// -----------------------------------------------------------------------------
// Executor Protocol Messages
// -----------------------------------------------------------------------------

/**
 * Response from executor discover command.
 *
 * Returns metadata about the experiment file: task name, evaluators,
 * default params, etc.
 */
export interface DiscoverResult {
  /** Protocol version for compatibility checking */
  protocol_version: string;

  /** Experiment name */
  name?: string;

  /** Experiment description */
  description?: string;

  /** Name of the registered task function */
  task?: string;

  /** Names of registered evaluator functions */
  evaluators: string[];

  /** Default parameters from the experiment definition */
  params: Record<string, unknown>;
}

/**
 * Request to initialize the executor.
 */
export interface InitRequest {
  /** Maximum number of concurrent workers */
  max_workers: number;

  /** Experiment parameters to use */
  params: Record<string, unknown>;
}

/**
 * Response from executor init command.
 */
export interface InitResult {
  /** Whether initialization succeeded */
  ok: boolean;

  /** Error message if initialization failed */
  error?: string;
}

/**
 * Single task result from executor.
 */
export interface TaskResult {
  /** Run identifier matching the input */
  run_id: string;

  /** Task output (any JSON-serializable value) */
  output?: unknown;

  /** Execution metadata (timing, etc.) */
  metadata?: Record<string, unknown>;

  /** Error message if task failed */
  error?: string;
}

/**
 * Single evaluation result from executor.
 */
export interface EvalResult {
  /** Run identifier matching the input */
  run_id: string;

  /** Name of the evaluator that produced this result */
  evaluator: string;

  /** Numerical score */
  score: number;

  /** Optional categorical label */
  label?: string;

  /** Evaluation metadata */
  metadata?: Record<string, unknown>;

  /** Error message if evaluation failed */
  error?: string;
}

/**
 * Response from executor shutdown command.
 */
export interface ShutdownResult {
  /** Whether shutdown completed successfully */
  ok: boolean;
}

// -----------------------------------------------------------------------------
// Protocol Message Types (for JSON-lines communication)
// -----------------------------------------------------------------------------

/**
 * Commands that can be sent to the executor.
 */
export type ExecutorCommand =
  | { cmd: "discover" }
  | { cmd: "init"; max_workers: number; params: Record<string, unknown> }
  | { cmd: "run_task"; input: TaskInput }
  | {
      cmd: "run_eval";
      input: EvalInput;
      evaluators?: string[];
    }
  | { cmd: "shutdown" };

/**
 * Parsed executor command with discriminated union.
 */
export interface DiscoverCommand {
  cmd: "discover";
}

export interface InitCommand {
  cmd: "init";
  max_workers: number;
  params: Record<string, unknown>;
}

export interface RunTaskCommand {
  cmd: "run_task";
  input: TaskInput;
}

export interface RunEvalCommand {
  cmd: "run_eval";
  input: EvalInput;
  evaluators?: string[];
}

export interface ShutdownCommand {
  cmd: "shutdown";
}

export type Command =
  | DiscoverCommand
  | InitCommand
  | RunTaskCommand
  | RunEvalCommand
  | ShutdownCommand;

// -----------------------------------------------------------------------------
// Helper functions for type conversion
// -----------------------------------------------------------------------------

/**
 * Create a TaskInput from a raw object.
 */
export function parseTaskInput<TInput = Record<string, unknown>>(
  data: Record<string, unknown>,
): TaskInput<TInput> {
  return {
    id: data.id as string,
    input: (data.input ?? {}) as TInput,
    output: data.output as Record<string, unknown> | undefined,
    metadata: data.metadata as Record<string, unknown> | undefined,
    experiment_id: data.experiment_id as string | undefined,
    run_id: data.run_id as string | undefined,
    repetition_number: data.repetition_number as number | undefined,
    params: (data.params ?? {}) as Record<string, unknown>,
  };
}

/**
 * Create an EvalInput from a raw object.
 */
export function parseEvalInput<
  TInput = Record<string, unknown>,
  TOutput = unknown,
>(data: Record<string, unknown>): EvalInput<TInput, TOutput> {
  return {
    example: (data.example ?? {}) as Record<string, unknown>,
    actual_output: data.actual_output as TOutput,
    expected_output: data.expected_output as
      | Record<string, unknown>
      | undefined,
    task_metadata: data.task_metadata as Record<string, unknown> | undefined,
    params: (data.params ?? {}) as Record<string, unknown>,
  };
}
