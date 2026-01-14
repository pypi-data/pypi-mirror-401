/* Capacity benchmark runner.
 * Incrementally tests capacity from RAMP_START to RAMP_END (target += 1 each step).
 * Stops when first failure occurs and reports max successful target + avg execution latency.
 *
 * Supports running multiple workloads sequentially for a single cluster.
 * Set WORKLOAD_NAMES as a comma-separated list (e.g., "parallel-small,parallel-tiny,sequential-small")
 * or use WORKLOAD_NAME for a single workload (backwards compatible).
 */

import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';

// Minimum success rate to consider a target successful (allows some failures)
const MIN_SUCCESS_RATE = 99;

// Cooldown period between workloads (in seconds) to let the cluster stabilize
const INTER_WORKLOAD_COOLDOWN_SECONDS = 30;

// Configuration mappings
const clusterNameToSettings = {
  'dr-small': {
    url: 'https://cap-bench-dr-small-716e6300275c5afb9979420a8f2684af.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-medium': {
    url: 'https://cap-bench-dr-medium-a7730894248e5aa081e650143f57318f.staging.langgraph.app',
    rampStartMultiplier: 2,
  },
  'dr-large': {
    url: 'https://cap-bench-dr-large-102fbff4d1d95711822e4b6c2d9796f0.staging.langgraph.app',
    rampStartMultiplier: 3,
  },
  'py-small': {
    url: 'https://cap-bench-py-runtime-small-c335b303529259e79c55fa5818911aea.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-medium': {
    url: 'https://cap-bench-py-runtime-medium-5ad796530c8354eea67f82c3a482bc7b.staging.langgraph.app',
    rampStartMultiplier: 2,
  },
  'py-large': {
    url: 'https://cap-bench-py-runtime-large-7721dd6d7a9e5260b47a551e82ae5865.staging.langgraph.app',
    rampStartMultiplier: 3,
  },
  // Python runtime multi-node scaling benchmarks
  'py-1-node': {
    url: 'https://cap-bench-py-1-node-77fbc06f80695b81af35a15f6270409e.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-3-node': {
    url: 'https://cap-bench-py-3-node-3faf368e14ad50d2806dba0e7807d2df.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-5-node': {
    url: 'https://cap-bench-py-5-node-bb59e89d2cd252fa9336cd88843c763a.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-7-node': {
    url: 'https://cap-bench-py-7-node-5f471cdb8a725e0bbb076cc9fb32b76d.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-10-node': {
    url: 'https://cap-bench-py-10-node-cf91dbee24535985a8fa50062acfb917.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-15-node': {
    url: 'https://cap-bench-py-15-node-fdd2802964f756a09a7a5cb90a0762ae.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'py-20-node': {
    url: 'https://cap-bench-py-20-node-0970dd3e458059e488db99d48c69ca69.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  // Distributed runtime multi-node scaling benchmarks
  'dr-1-node': {
    url: 'https://cap-bench-dr-1-node-49e9ad9e573e55f38c51a11626e72e89.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-3-node': {
    url: 'https://cap-bench-dr-3-node-467456b54e7f5606bca4cf4466ed2c9a.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-5-node': {
    url: 'https://cap-bench-dr-5-node-f3c7580d25e65a6ba48dc640f3a9922e.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-7-node': {
    url: 'https://cap-bench-dr-7-node-fbf64b46fc9b57239764478187abe534.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-10-node': {
    url: 'https://cap-bench-dr-10-node-f6a3fb40c33f533fbcfafeee02f9ed68.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-15-node': {
    url: 'https://cap-bench-dr-15-node-38c2ba919c73556c9b2e64d8c2e8f839.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
  'dr-20-node': {
    url: 'https://cap-bench-dr-20-node-7cea036a01a25a9caec0be0b873f9b0a.staging.langgraph.app',
    rampStartMultiplier: 1,
  },
};

const workloadNameToAgentParams = {
  'sequential-small': {
    expand: 1,
    steps: 10,
    dataSize: 100000, // 100KB per step × 10 steps = 1MB total
    delay: 0,
    rampStartBase: 10,
    rampEnd: 1000,
    runExecutionTimeoutSeconds: 60,
  },
  // TODO: there is a bug somewhere! this workload cannot return(but the run is successful)
  // 'sequential-medium': {
  //   expand: 1,
  //   steps: 10,
  //   dataSize: 1000000, // 1MB per step × 10 steps = 10MB total
  //   delay: 0,
  //   rampStartBase: 3,
  //   rampEnd: 1000,
  //   runExecutionTimeoutSeconds: 60,
  // },
  // 'sequential-large': {
  //   expand: 1,
  //   steps: 10,
  //   dataSize: 10000000, // 10MB per step × 10 steps = 100MB total
  //   delay: 0,
  //   rampStartBase: 1,
  //   rampEnd: 1000,
  //   runExecutionTimeoutSeconds: 60,
  // },
  'parallel-tiny': {
    expand: 2,
    steps: 100,
    dataSize: 100, // 100 bytes per step × 100 steps = 10KB total
    delay: 0,
    rampStartBase: 2,
    rampEnd: 1000,
    runExecutionTimeoutSeconds: 60,
  },
  'parallel-small': {
    expand: 2,
    steps: 100,
    dataSize: 10000, // 10KB per step × 100 steps = 1MB total
    delay: 0,
    rampStartBase: 2,
    rampEnd: 1000,
    runExecutionTimeoutSeconds: 60,
  },
  // 'parallel-medium': {
  //   expand: 10,
  //   steps: 500,
  //   dataSize: 100000, // 100KB per step × 500 steps = 50MB total
  //   delay: 0,
  //   rampStartBase: 5,
  //   rampEnd: 1000,
  //   runExecutionTimeoutSeconds: 60,
  // },
  // 'parallel-large': {
  //   expand: 10,
  //   steps: 500,
  //   dataSize: 1000000, // 1MB per step × 500 steps = 500MB total
  //   delay: 0,
  //   rampStartBase: 2,
  //   rampEnd: 1000,
  //   runExecutionTimeoutSeconds: 60,
  // },
};

// Environment variables
const CLUSTER_NAME = process.env.CLUSTER_NAME;
// Support both WORKLOAD_NAMES (comma-separated) and WORKLOAD_NAME (single, backwards compatible)
const WORKLOAD_NAMES = process.env.WORKLOAD_NAMES
  ? process.env.WORKLOAD_NAMES.split(',').map(w => w.trim()).filter(w => w)
  : process.env.WORKLOAD_NAME
    ? [process.env.WORKLOAD_NAME]
    : [];

// Validate inputs
validateInputs();

const clusterSettings = clusterNameToSettings[CLUSTER_NAME];

console.log(`\n=== Cluster Configuration ===`);
console.log(`Cluster: ${CLUSTER_NAME} (multiplier: ${clusterSettings.rampStartMultiplier}x)`);
console.log(`URL: ${clusterSettings.url}`);
console.log(`Workloads to run: ${WORKLOAD_NAMES.join(', ')}`);

// Helper functions (in order of usage)

function validateInputs() {
  if (!CLUSTER_NAME || !clusterNameToSettings[CLUSTER_NAME]) {
    throw new Error(`Invalid CLUSTER_NAME: "${CLUSTER_NAME}". Must be one of: ${Object.keys(clusterNameToSettings).join(', ')}`);
  }
  if (WORKLOAD_NAMES.length === 0) {
    throw new Error(`No workloads specified. Set WORKLOAD_NAMES (comma-separated) or WORKLOAD_NAME. Valid workloads: ${Object.keys(workloadNameToAgentParams).join(', ')}`);
  }
  for (const workloadName of WORKLOAD_NAMES) {
    if (!workloadNameToAgentParams[workloadName]) {
      throw new Error(`Invalid workload: "${workloadName}". Must be one of: ${Object.keys(workloadNameToAgentParams).join(', ')}`);
    }
  }
}

function runK6(target, workloadName) {
  const baseUrl = clusterNameToSettings[CLUSTER_NAME].url;
  const agentParams = workloadNameToAgentParams[workloadName];

  let result;
  try {
    result = execFileSync('k6', ['run', 'capacity_k6.js'], {
      cwd: process.cwd(),
      env: {
        ...process.env,
        BASE_URL: baseUrl,
        TARGET: String(target),
        DATA_SIZE: String(agentParams.dataSize),
        DELAY: String(agentParams.delay),
        EXPAND: String(agentParams.expand),
        STEPS: String(agentParams.steps),
        RUN_EXECUTION_TIMEOUT_SECONDS: String(agentParams.runExecutionTimeoutSeconds),
      },
      encoding: 'utf-8',
      stdio: ['inherit', 'pipe', 'inherit'],  // Inherit stdin and stderr, pipe stdout
    });
  } catch (error) {
    console.log(`\n⚠️  K6 failed at target=${target}`);
    console.error(error);
    return null;
  }

  // Print the output to console for visibility
  console.log(result);

  // Find the JSON line from handleSummary output
  const lines = result.split('\n');
  const jsonLine = lines.find(line => {
    const trimmed = line.trim();
    return trimmed.startsWith('{') && trimmed.includes('"target"');
  });

  if (!jsonLine) {
    throw new Error(`No JSON output found in k6 results. Output: ${result.substring(0, 500)}`);
  }

  return { stdout: jsonLine.trim() };
}

function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

/**
 * Run benchmark for a single workload.
 * Returns the result object or null if no successful runs.
 */
async function runWorkloadBenchmark(workloadName) {
  const workloadConfig = workloadNameToAgentParams[workloadName];
  const rampStart = workloadConfig.rampStartBase * clusterSettings.rampStartMultiplier;
  const rampEnd = workloadConfig.rampEnd;

  console.log(`\n${'='.repeat(60)}`);
  console.log(`=== Workload: ${workloadName} ===`);
  console.log(`${'='.repeat(60)}`);
  console.log(`  - Ramp: ${rampStart} (${workloadConfig.rampStartBase} × ${clusterSettings.rampStartMultiplier}) → ${rampEnd}`);
  console.log(`  - Timeout: ${workloadConfig.runExecutionTimeoutSeconds}s`);
  console.log(`  - Expand: ${workloadConfig.expand}`);
  console.log(`  - Steps: ${workloadConfig.steps}`);
  console.log(`  - Data Size: ${workloadConfig.dataSize} bytes`);
  console.log(`  - Delay: ${workloadConfig.delay}s`);

  let currentTarget = rampStart;
  let lastSuccessfulTarget = null;
  let lastSuccessfulLatency = null;

  while (currentTarget <= rampEnd) {
    console.log(`\n=== Testing target: ${currentTarget} ===`);

    // Run K6
    console.log(`Running k6 with target=${currentTarget}...`);
    const result = runK6(currentTarget, workloadName);

    // Check if k6 command failed (capacity limit reached)
    if (result === null) {
      console.log(`❌ Failed at target ${currentTarget}`);
      break;
    }

    // Parse JSON output
    const metrics = JSON.parse(result.stdout);

    // Check if succeeded (allow some failures, but must meet minimum success rate)
    if (metrics.successRate < MIN_SUCCESS_RATE || !metrics.avgExecutionLatencySeconds) {
      console.log(`❌ Failed at target ${currentTarget} (success rate: ${metrics.successRate.toFixed(2)}%, avg latency: ${metrics.avgExecutionLatencySeconds || 'N/A'})`);
      break;
    }

    // Record success
    lastSuccessfulTarget = currentTarget;
    lastSuccessfulLatency = metrics.avgExecutionLatencySeconds;
    console.log(`✅ Success: ${metrics.avgExecutionLatencySeconds.toFixed(3)}s avg latency (${metrics.successRate.toFixed(2)}% success rate)`);

    currentTarget += 1;
  }

  // Validate results
  if (lastSuccessfulTarget === null) {
    console.log(`⚠️  No successful runs for workload ${workloadName} - RAMP_START may be too high`);
    return null;
  }

  if (currentTarget > rampEnd) {
    console.log(`⚠️  Reached RAMP_END (${rampEnd}) without finding capacity limit for workload ${workloadName} - consider increasing RAMP_END`);
    // Still return the result, as reaching max is a valid (good) outcome
  }

  return {
    maxSuccessfulTarget: lastSuccessfulTarget,
    avgExecutionLatencySeconds: Number(lastSuccessfulLatency.toFixed(3)),
  };
}

// Main function - runs all workloads sequentially
async function main() {
  const allResults = {};
  const errors = [];

  for (let i = 0; i < WORKLOAD_NAMES.length; i++) {
    const workloadName = WORKLOAD_NAMES[i];

    try {
      const result = await runWorkloadBenchmark(workloadName);

      if (result) {
        allResults[workloadName] = result;
        console.log(`\n✅ Completed ${workloadName}`);
      } else {
        errors.push(`${workloadName}: No successful runs`);
      }
    } catch (e) {
      console.error(`\n❌ Error running workload ${workloadName}: ${e.message}`);
      errors.push(`${workloadName}: ${e.message}`);
    }

    // Cooldown between workloads (skip after last workload)
    if (i < WORKLOAD_NAMES.length - 1) {
      console.log(`\n⏳ Cooling down for ${INTER_WORKLOAD_COOLDOWN_SECONDS}s before next workload...`);
      await sleep(INTER_WORKLOAD_COOLDOWN_SECONDS);
    }
  }

  // Print summary
  console.log('\n' + '='.repeat(60));
  console.log('=== Final Summary ===');
  console.log('='.repeat(60));

  for (const [workloadName, result] of Object.entries(allResults)) {
    console.log(`\n${workloadName}:`);
    console.log(JSON.stringify(result, null, 2));
  }

  if (errors.length > 0) {
    console.log('\n⚠️  Errors:');
    for (const error of errors) {
      console.log(`  - ${error}`);
    }
  }

  // Fail if no workloads succeeded
  if (Object.keys(allResults).length === 0) {
    throw new Error('All workloads failed - no successful runs');
  }

  // Write single summary file with all workload results
  const summaryOutput = {
    clusterName: CLUSTER_NAME,
    workloads: allResults,
  };
  writeFileSync('capacity_summary.json', JSON.stringify(summaryOutput, null, 2));
  console.log('\nResults written to capacity_summary.json');

  return allResults;
}

// Run
main().catch((e) => {
  console.error(`\nError: ${e.message}`);
  process.exit(1);
});
