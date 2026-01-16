// Package orchestrator implements windowed task dispatch with flow control.
package orchestrator

import (
	"context"
	"fmt"
	"strings"
	"sync"

	"github.com/sst/cat-experiments/cli/internal/executor"
	"github.com/sst/cat-experiments/cli/internal/protocol"
)

// Config holds orchestrator configuration.
type Config struct {
	MaxWorkers  int
	Params      map[string]any
	Repetitions int
}

// TaskCallback is called when a task completes.
type TaskCallback func(*protocol.TaskResult)

// EvalCallback is called when an evaluation completes.
type EvalCallback func(*protocol.EvalResult)

// CapturedRunOutput holds captured stdout/stderr for a specific run.
type CapturedRunOutput struct {
	RunID   string
	Output  *executor.CapturedOutput
	IsError bool // true if the task/eval had an error
}

// RunOutputs collects all captured output during an experiment run.
type RunOutputs struct {
	mu      sync.Mutex
	outputs []CapturedRunOutput
}

// Add adds captured output for a run.
func (r *RunOutputs) Add(runID string, output *executor.CapturedOutput, isError bool) {
	if output == nil || output.IsEmpty() {
		return
	}
	r.mu.Lock()
	defer r.mu.Unlock()
	r.outputs = append(r.outputs, CapturedRunOutput{
		RunID:   runID,
		Output:  output,
		IsError: isError,
	})
}

// GetAll returns all captured outputs.
func (r *RunOutputs) GetAll() []CapturedRunOutput {
	r.mu.Lock()
	defer r.mu.Unlock()
	return append([]CapturedRunOutput{}, r.outputs...)
}

// GetFailed returns only outputs from failed runs.
func (r *RunOutputs) GetFailed() []CapturedRunOutput {
	r.mu.Lock()
	defer r.mu.Unlock()
	var failed []CapturedRunOutput
	for _, o := range r.outputs {
		if o.IsError {
			failed = append(failed, o)
		}
	}
	return failed
}

// Orchestrator manages windowed task dispatch to an executor.
type Orchestrator struct {
	executor executor.AsyncExecutor
	config   Config
}

// New creates a new orchestrator.
func New(exec executor.AsyncExecutor, config Config) *Orchestrator {
	if config.MaxWorkers < 1 {
		config.MaxWorkers = 1
	}
	if config.Repetitions < 1 {
		config.Repetitions = 1
	}
	return &Orchestrator{
		executor: exec,
		config:   config,
	}
}

// RunTasks executes all tasks with windowed concurrency.
// Uses async send/receive pattern:
// - Sends up to MaxWorkers tasks without waiting
// - Reads responses as they complete
// - Refills the window with new tasks
// Calls callback for each completed task (if provided).
// If capturedOutputs is non-nil, captured stdout/stderr is collected for later display.
// Returns all results in completion order.
func (o *Orchestrator) RunTasks(
	ctx context.Context,
	examples []protocol.DatasetExample,
	callback TaskCallback,
	capturedOutputs *RunOutputs,
) ([]*protocol.TaskResult, error) {
	// Build task inputs
	var inputs []protocol.TaskInput
	for _, ex := range examples {
		for rep := 1; rep <= o.config.Repetitions; rep++ {
			runID := fmt.Sprintf("%s#%d", ex.ID, rep)
			inputs = append(inputs, protocol.NewTaskInputFromExample(
				ex, "", runID, rep, o.config.Params,
			))
		}
	}

	if len(inputs) == 0 {
		return nil, nil
	}

	totalTasks := len(inputs)
	results := make([]*protocol.TaskResult, 0, totalTasks)
	var resultsMu sync.Mutex

	// Error handling
	errChan := make(chan error, 1)
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// Semaphore for windowed concurrency
	sem := make(chan struct{}, o.config.MaxWorkers)

	// Sender goroutine: sends all tasks (blocks on semaphore)
	senderDone := make(chan struct{})
	go func() {
		defer close(senderDone)
		for _, input := range inputs {
			select {
			case <-ctx.Done():
				return
			case sem <- struct{}{}: // acquire slot
			}

			if err := o.executor.RunTaskAsync(input); err != nil {
				select {
				case errChan <- fmt.Errorf("send task %s: %w", input.RunID, err):
					cancel()
				default:
				}
				return
			}
		}
	}()

	// Reader goroutine: reads responses and releases semaphore slots
	readerDone := make(chan struct{})
	go func() {
		defer close(readerDone)
		received := 0

		for received < totalTasks {
			select {
			case <-ctx.Done():
				return
			default:
			}

			// Read a result
			data, err := o.executor.ReadResult()
			if err != nil {
				select {
				case errChan <- fmt.Errorf("read result: %w", err):
					cancel()
				default:
				}
				return
			}

			result, err := protocol.ParseTaskResult(data)
			if err != nil {
				select {
				case errChan <- fmt.Errorf("parse result: %w", err):
					cancel()
				default:
				}
				return
			}

			// Flush captured output and collect if requested
			capturedOutput := o.executor.FlushCapturedOutput()
			if capturedOutputs != nil && capturedOutput != nil {
				capturedOutputs.Add(result.RunID, capturedOutput, result.Error != "")
			}

			// Release semaphore slot
			<-sem

			// Store result
			resultsMu.Lock()
			results = append(results, result)
			resultsMu.Unlock()

			received++

			// Callback
			if callback != nil {
				callback(result)
			}
		}
	}()

	// Wait for both goroutines
	<-senderDone
	<-readerDone

	// Check for errors (context errors take precedence)
	if ctx.Err() != nil {
		return results, ctx.Err()
	}

	select {
	case err := <-errChan:
		return results, err
	default:
	}

	return results, nil
}

// RunEvals executes evaluations for all completed tasks.
// If capturedOutputs is non-nil, captured stdout/stderr is collected for later display.
func (o *Orchestrator) RunEvals(
	ctx context.Context,
	taskResults []*protocol.TaskResult,
	examples []protocol.DatasetExample,
	callback EvalCallback,
	capturedOutputs *RunOutputs,
) ([]*protocol.EvalResult, error) {
	// Build example lookup
	exampleMap := make(map[string]protocol.DatasetExample)
	for _, ex := range examples {
		exampleMap[ex.ID] = ex
	}

	// Build eval inputs
	var evalInputs []protocol.EvalInput

	for _, taskResult := range taskResults {
		// Skip errored tasks
		if taskResult.Error != "" {
			continue
		}

		// Extract example ID from run_id (format: "example_id#rep")
		exampleID := extractExampleID(taskResult.RunID)
		example, ok := exampleMap[exampleID]
		if !ok {
			continue
		}

		evalInput := protocol.EvalInput{
			Example: map[string]any{
				"id":       example.ID,
				"run_id":   taskResult.RunID,
				"input":    example.Input,
				"output":   example.Output,
				"metadata": example.Metadata,
			},
			ActualOutput:   taskResult.Output,
			ExpectedOutput: example.Output,
			TaskMetadata:   taskResult.Metadata,
			Params:         o.config.Params,
		}

		evalInputs = append(evalInputs, evalInput)
	}

	if len(evalInputs) == 0 {
		return nil, nil
	}

	totalEvals := len(evalInputs)
	results := make([]*protocol.EvalResult, 0)
	var resultsMu sync.Mutex

	errChan := make(chan error, 1)
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// Semaphore for windowed concurrency
	sem := make(chan struct{}, o.config.MaxWorkers)

	// Sender goroutine
	senderDone := make(chan struct{})
	go func() {
		defer close(senderDone)
		for _, input := range evalInputs {
			select {
			case <-ctx.Done():
				return
			case sem <- struct{}{}:
			}

			if err := o.executor.RunEvalAsync(input, nil); err != nil {
				runID := input.Example["run_id"].(string)
				select {
				case errChan <- fmt.Errorf("send eval %s: %w", runID, err):
					cancel()
				default:
				}
				return
			}
		}
	}()

	// Reader goroutine
	readerDone := make(chan struct{})
	go func() {
		defer close(readerDone)
		received := 0

		for received < totalEvals {
			select {
			case <-ctx.Done():
				return
			default:
			}

			data, err := o.executor.ReadResult()
			if err != nil {
				select {
				case errChan <- fmt.Errorf("read eval result: %w", err):
					cancel()
				default:
				}
				return
			}

			// Parse as array of eval results (one response per eval input)
			evalResults, err := protocol.ParseEvalResults(data)
			if err != nil {
				select {
				case errChan <- fmt.Errorf("parse eval results: %w", err):
					cancel()
				default:
				}
				return
			}

			// Flush captured output and collect if requested
			capturedOutput := o.executor.FlushCapturedOutput()
			if capturedOutputs != nil && capturedOutput != nil {
				// Check if any eval in this batch had an error
				hasError := false
				var runID string
				for _, r := range evalResults {
					runID = r.RunID
					if r.Error != "" {
						hasError = true
						break
					}
				}
				if runID != "" {
					capturedOutputs.Add(runID, capturedOutput, hasError)
				}
			}

			// Release semaphore slot
			<-sem

			resultsMu.Lock()
			results = append(results, evalResults...)
			resultsMu.Unlock()

			received++

			if callback != nil {
				for _, r := range evalResults {
					callback(r)
				}
			}
		}
	}()

	<-senderDone
	<-readerDone

	// Check for errors (context errors take precedence)
	if ctx.Err() != nil {
		return results, ctx.Err()
	}

	select {
	case err := <-errChan:
		return results, err
	default:
	}

	return results, nil
}

// extractExampleID extracts example ID from run_id format "example_id#rep"
func extractExampleID(runID string) string {
	if idx := strings.LastIndex(runID, "#"); idx >= 0 {
		return runID[:idx]
	}
	return runID
}
