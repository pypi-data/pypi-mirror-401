#!/usr/bin/env node
/**
 * CLI entry point for the cat-experiments executor.
 *
 * This script is invoked by the Go CLI to run experiments.
 * Usage: cat-experiments-executor <experiment.ts>
 */

import { runExecutor } from "../src/executor/index.js";

const experimentPath = process.argv[2];

if (!experimentPath) {
  console.error("Usage: cat-experiments-executor <experiment.ts>");
  console.error("");
  console.error(
    "This command is typically invoked by the cat-experiments CLI.",
  );
  console.error(
    "To run an experiment, use: cat-experiments run <experiment.ts>",
  );
  process.exit(1);
}

runExecutor(experimentPath).catch((error) => {
  console.error("Executor failed:", error);
  process.exit(1);
});
