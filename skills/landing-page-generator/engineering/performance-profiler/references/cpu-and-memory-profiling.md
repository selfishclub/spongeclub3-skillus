# CPU and Memory Profiling

Read this when diagnosing CPU bottlenecks or memory leaks in Node.js or Python — flamegraphs, V8 CPU profiles, heap snapshots, and allocation tracing. Start every investigation with the Golden Rule below.

## Golden Rule: Measure First

```
WRONG: "I think the N+1 query is slow, let me fix it"
RIGHT: Profile → Confirm bottleneck → Fix → Measure again → Verify improvement

Every optimization must have:
1. Baseline metrics (before)
2. Profiler evidence (what's actually slow)
3. The fix
4. Post-fix metrics (after)
5. Delta calculation (improvement %)
```

## Node.js CPU Profiling

### Method 1: Clinic.js Flamegraph

```bash
# Install
npm install -g clinic

# Generate flamegraph (starts server, applies load, generates HTML report)
clinic flame -- node server.js

# With specific load profile
clinic flame --autocannon [ /api/endpoint -c 10 -d 30 ] -- node server.js

# Analyze specific scenario
clinic flame --on-port 'autocannon -c 50 -d 60 http://localhost:$PORT/api/heavy-endpoint' -- node server.js
```

### Method 2: V8 CPU Profile

```bash
# Start Node with inspector
node --inspect server.js

# Or profile on demand
node --cpu-prof --cpu-prof-dir=./profiles server.js
# Load the .cpuprofile file in Chrome DevTools > Performance

# Programmatic profiling of a specific function
const { Session } = require('inspector');
const session = new Session();
session.connect();

session.post('Profiler.enable', () => {
  session.post('Profiler.start', () => {
    // Run the code you want to profile
    runHeavyOperation();

    session.post('Profiler.stop', (err, { profile }) => {
      require('fs').writeFileSync('profile.cpuprofile', JSON.stringify(profile));
    });
  });
});
```

## Memory Leak Detection

### Node.js Heap Snapshots

```javascript
// Take heap snapshots programmatically
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(label) {
  const snapshotPath = `heap-${label}-${Date.now()}.heapsnapshot`;
  const stream = v8.writeHeapSnapshot(snapshotPath);
  console.log(`Heap snapshot written to: ${snapshotPath}`);
  return snapshotPath;
}

// Leak detection pattern: compare two snapshots
// 1. Take snapshot at startup
takeHeapSnapshot('baseline');

// 2. Run operations that you suspect leak
// ... process 1000 requests ...

// 3. Force GC and take another snapshot
if (global.gc) global.gc(); // requires --expose-gc flag
takeHeapSnapshot('after-load');

// Load both .heapsnapshot files in Chrome DevTools > Memory
// Use "Comparison" view to find objects that grew
```

### Python Memory Profiling

```bash
# Install tracemalloc-based profiler
pip install memray

# Profile a script
memray run my_script.py
memray flamegraph memray-output.bin -o flamegraph.html

# Profile a specific function
python -c "
import tracemalloc
tracemalloc.start()

# Run your code
from my_module import heavy_function
heavy_function()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
print('Top 10 memory allocations:')
for stat in top_stats[:10]:
    print(stat)
"
```
