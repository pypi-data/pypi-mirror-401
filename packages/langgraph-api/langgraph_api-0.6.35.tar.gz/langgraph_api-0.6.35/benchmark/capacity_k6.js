import http from 'k6/http';
import { check } from 'k6';
import { Trend } from 'k6/metrics';

// Single metric: execution latency
const runExecutionLatency = new Trend('run_execution_latency');

// Environment variables
const BASE_URL = __ENV.BASE_URL;
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;
const TARGET = parseInt(__ENV.TARGET || '10');
const RUN_EXECUTION_TIMEOUT_SECONDS = parseInt(__ENV.RUN_EXECUTION_TIMEOUT_SECONDS || '10');

// Agent params
const DATA_SIZE = parseInt(__ENV.DATA_SIZE || '1000');
const DELAY = parseInt(__ENV.DELAY || '0');
const EXPAND = parseInt(__ENV.EXPAND || '10');
const STEPS = parseInt(__ENV.STEPS || '10');

// K6 options
export const options = {
  scenarios: {
    capacity_test: {
      executor: 'per-vu-iterations',
      vus: TARGET,
      iterations: 1,  // Each VU executes once
      maxDuration: `${RUN_EXECUTION_TIMEOUT_SECONDS + 30}s`,
    },
  },
  // No thresholds - let all VUs complete and report success rate
  // The runner will decide if the success rate is acceptable
};

function headers() {
  const h = { 'Content-Type': 'application/json' };
  if (LANGSMITH_API_KEY) {
    h['x-api-key'] = LANGSMITH_API_KEY;
  }
  return h;
}

function buildPayload() {
  return JSON.stringify({
    assistant_id: 'benchmark',
    input: {
      data_size: DATA_SIZE,
      delay: DELAY,
      expand: EXPAND,
      steps: STEPS,
    },
    config: {
      recursion_limit: STEPS + 2,
    },
  });
}

export default function() {
  // Print parameters (only once from VU 1)
  if (__VU === 1 && __ITER === 0) {
    console.log(`\n=== K6 Test Parameters ===`);
    console.log(`BASE_URL: ${BASE_URL}`);
    console.log(`TARGET: ${TARGET}`);
    console.log(`RUN_EXECUTION_TIMEOUT_SECONDS: ${RUN_EXECUTION_TIMEOUT_SECONDS}`);
    console.log(`DATA_SIZE: ${DATA_SIZE}`);
    console.log(`DELAY: ${DELAY}`);
    console.log(`EXPAND: ${EXPAND}`);
    console.log(`STEPS: ${STEPS}`);
    console.log(`=========================\n`);
  }
  
  try {
    doExecute();
  } catch (e) {
    console.error(`VU ${__VU} failed: ${e.message}`);
    throw e;  // Re-throw to fail the test
  }
}

function doExecute() {
  const startTime = Date.now();
  const payload = buildPayload();
  const reqHeaders = headers();
  
  // Stateless run: directly create and wait for run completion (no thread needed)
  const rRes = http.post(`${BASE_URL}/runs/wait`, payload, {
    headers: reqHeaders,
    timeout: `${RUN_EXECUTION_TIMEOUT_SECONDS + 10}s`,  // K6 timeout slightly larger than business timeout
  });
  
  const totalDuration = (Date.now() - startTime) / 1000;

  console.log(`VU ${__VU}: Received response: ${rRes.status} totalDuration: ${totalDuration}`);
  if(rRes.status !== 200) {
      // Try to cancel any pending/running runs when wait fails
      console.log(`VU ${__VU}: Wait failed, attempting to cancel runs...`);
      try {
        const cancelRes = http.post(
          `${BASE_URL}/runs/cancel`,
          JSON.stringify({ status: 'all' }),
          {
            headers: reqHeaders,
            timeout: '10s',
          }
        );
        if (cancelRes.status === 204) {
          console.log(`VU ${__VU}: Successfully canceled runs`);
        }
      } catch (e) {
        // Ignore cancel errors, the main error is the wait failure
        console.log(`VU ${__VU}: Cancel attempt failed: ${e.message}`);
      }
  }
  
  // Check HTTP request succeeded
  check(rRes, {
    'run request succeeded': (r) => r.status === 200,
  });

  if (rRes.status !== 200) {
    throw new Error(`Run request failed with status: ${rRes.status}`);
  }
  
  // Check for timeout - this will fail the threshold if timeout occurs
  const timeoutCheck = check(null, {
    'execution within timeout': () => totalDuration <= RUN_EXECUTION_TIMEOUT_SECONDS,
  });
  
  if (!timeoutCheck) {
    throw new Error(`Execution timeout: ${totalDuration.toFixed(2)}s > ${RUN_EXECUTION_TIMEOUT_SECONDS}s`);
  }
  
  // Record execution latency (convert to ms)
  runExecutionLatency.add(totalDuration * 1000);
}

export function handleSummary(data) {
  const avgLatency = data.metrics.run_execution_latency?.values?.avg / 1000;
  const successRate = data.metrics.checks?.values?.rate * 100 || 0;
  
  return {
    stdout: JSON.stringify({
      target: TARGET,
      avgExecutionLatencySeconds: avgLatency || null,
      successRate: successRate,
    }),
  };
}
