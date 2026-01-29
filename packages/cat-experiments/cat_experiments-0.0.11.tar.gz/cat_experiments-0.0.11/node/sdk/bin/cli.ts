#!/usr/bin/env node
/**
 * CLI entry point that delegates to the platform-specific Go binary.
 *
 * This script finds and executes the cat-experiments Go binary,
 * which is installed via optional dependencies for each platform.
 */

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Find the platform-specific binary.
 */
function findBinary(): string | null {
  const platform = process.platform;
  const arch = process.arch;

  // Map Node.js platform/arch to our package names
  let platformKey: string;
  if (platform === "darwin" && arch === "arm64") {
    platformKey = "darwin-arm64";
  } else if (platform === "darwin" && arch === "x64") {
    platformKey = "darwin-x64";
  } else if (platform === "linux" && arch === "arm64") {
    platformKey = "linux-arm64";
  } else if (platform === "linux" && arch === "x64") {
    platformKey = "linux-x64";
  } else if (platform === "win32" && arch === "x64") {
    platformKey = "win32-x64";
  } else {
    return null;
  }

  // Look for the binary in node_modules
  const binaryName =
    platform === "win32" ? "cat-experiments.exe" : "cat-experiments";
  const possiblePaths = [
    // When installed as a dependency
    join(
      __dirname,
      "..",
      "..",
      `cat-experiments-${platformKey}`,
      "bin",
      binaryName,
    ),
    // When running from the monorepo
    join(__dirname, "..", "..", "..", `bin-${platformKey}`, "bin", binaryName),
  ];

  for (const p of possiblePaths) {
    if (existsSync(p)) {
      return p;
    }
  }

  return null;
}

const binary = findBinary();

if (!binary) {
  console.error(
    `Error: No cat-experiments binary found for ${process.platform}-${process.arch}`,
  );
  console.error("");
  console.error(
    "This platform may not be supported, or the binary package failed to install.",
  );
  console.error(
    "Supported platforms: darwin-arm64, darwin-x64, linux-arm64, linux-x64, win32-x64",
  );
  process.exit(1);
}

// Pass through all arguments to the Go binary
const result = spawnSync(binary, process.argv.slice(2), {
  stdio: "inherit",
});

process.exit(result.status ?? 1);
