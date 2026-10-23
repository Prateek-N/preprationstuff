# -*- coding: utf-8 -*-
"""
Part 1: Python Coding Problems 1 to 12 for Pavan Chandramouleswara
Senior Data Engineer Interview Preparation Suite.

Each problem includes:
- Problem Statement & Example
- Algorithmic Thought Process & Tradeoffs
- Clean, Typed Python Code with Extensive Comments
- Time & Space Complexity Analysis
"""

CODING_PROBLEMS_PART1 = [
    # =========================================================================
    # PROBLEM 1: SLIDING WINDOW MAXIMUM (REAL-TIME SURGE MULTIPLIER)
    # =========================================================================
    {
        "num": 1,
        "title": "Sliding Window Maximum Event Metric (Marketplace Surge Calculation)",
        "category": "Streaming & Sliding Windows",
        "problem_statement": """In Uber's marketplace streaming engine, telemetry events report demand intensity per minute. Given an array of numeric demand multipliers `nums` and a sliding window size `k` (representing the rolling lookback window in minutes), calculate the maximum surge multiplier observed in every sliding window of size `k` as the window moves from left to right across the stream.

Example:
Input: nums = [1.2, 3.5, -1.1, -3.2, 5.0, 3.6, 6.7, 7.1], k = 3
Output: [3.5, 3.5, 5.0, 5.0, 6.7, 7.1]
Explanation:
Window [1.2, 3.5, -1.1] -> Max: 3.5
Window [3.5, -1.1, -3.2] -> Max: 3.5
Window [-1.1, -3.2, 5.0] -> Max: 5.0
Window [-3.2, 5.0, 3.6] -> Max: 5.0
Window [5.0, 3.6, 6.7] -> Max: 6.7
Window [3.6, 6.7, 7.1] -> Max: 7.1""",
        "thought_process": """1. **Brute Force Approach**: For each window of size k, scan all k elements to determine the maximum. With N elements and window size k, this requires (N - k + 1) * k comparisons, yielding an O(N * k) time complexity. For large streaming batches (e.g., N = 10^6, k = 10^4), this causes severe latency spikes and fails real-time SLAs.
2. **Optimal Approach (Monotonic Deque)**: We can achieve linear O(N) time complexity by maintaining a double-ended queue (`collections.deque`) storing indices of candidates in monotonically decreasing order of their corresponding values.
3. **Invariant Maintenance**:
   - As we inspect element at index `i`, we first evict any indices from the front of the deque that fall outside the active window boundary (i.e., `index <= i - k`).
   - We then evict elements from the back of the deque whose values are less than or equal to `nums[i]`, because `nums[i]` is both newer and larger, rendering older smaller elements irrelevant for future windows.
   - We push the current index `i` to the back.
   - Once the loop reaches at least index `k - 1`, the element at `deque[0]` represents the index of the maximum value for the current window.
4. **Edge Cases**: Empty input array returns empty list; `k >= len(nums)` returns a single maximum; negative values handled naturally by monotonic ordering.""",
        "code": """from collections import deque
from typing import List

def max_sliding_window_surge(nums: List[float], k: int) -> List[float]:
    \"\"\"
    Computes the maximum value in every sliding window of size k using a monotonic deque.
    
    :param nums: List of floating-point telemetry surge multipliers.
    :param k: Window length in steps.
    :return: List of maximum values for each sliding window.
    \"\"\"
    if not nums or k <= 0:
        return []
    if k == 1:
        return nums[:]
    
    # Monotonic deque storing indices of candidate maximums
    # Values corresponding to indices in dq are strictly decreasing
    dq: deque[int] = deque()
    result: List[float] = []
    
    for i, val in enumerate(nums):
        # Step 1: Remove indices that are outside the current sliding window [i - k + 1, i]
        while dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # Step 2: Remove indices whose values are <= current value from the back
        # They will never be the maximum because the current element is larger and newer
        while dq and nums[dq[-1]] <= val:
            dq.pop()
            
        # Step 3: Append current index
        dq.append(i)
        
        # Step 4: Record current window max once we have processed at least k elements
        if i >= k - 1:
            result.append(nums[dq[0]])
            
    return result

# Verification
if __name__ == "__main__":
    test_stream = [1.2, 3.5, -1.1, -3.2, 5.0, 3.6, 6.7, 7.1]
    window = 3
    print("Surge Maxima:", max_sliding_window_surge(test_stream, window))
    # Output: [3.5, 3.5, 5.0, 5.0, 6.7, 7.1]
""",
        "time_complexity": "O(N) - Every index is pushed into the deque exactly once and popped from the deque at most once across the entire iteration, amortizing to constant O(1) operations per element.",
        "space_complexity": "O(k) - The deque stores at most k indices corresponding to the active sliding window."
    },

    # =========================================================================
    # PROBLEM 2: STREAM DEDUPLICATION WITH WATERMARK & TTL CACHE
    # =========================================================================
    {
        "num": 2,
        "title": "Stream Deduplication with Bounded Watermark and TTL Eviction",
        "category": "Streaming & Event Processing",
        "problem_statement": """In real-time Kafka consumers, network retries introduce duplicate message payloads. Implement a stream deduplicator class `StreamDeduplicator` that processes an incoming stream of `(event_id, event_timestamp)` tuples. 
The system must:
1. Accept an allowable lateness threshold `watermark_delay_seconds`.
2. Reject events that arrive older than `current_max_timestamp - watermark_delay_seconds` (too late).
3. Filter out duplicate `event_id`s that have already been seen within the valid watermark retention window.
4. Automatically evict expired event IDs from memory to maintain bounded memory footprint.

Example:
dedup = StreamDeduplicator(watermark_delay_seconds=60)
dedup.process_event("e1", 100) -> True  (First seen, accepted)
dedup.process_event("e1", 105) -> False (Duplicate event_id within window)
dedup.process_event("e2", 170) -> True  (Advances max_time to 170, watermark is 110)
dedup.process_event("e3", 90)  -> False (Rejected: timestamp 90 is older than watermark 110)""",
        "thought_process": """1. **Requirements Analysis**: Unbounded memory growth is the primary failure mode of naive streaming deduplication (e.g., storing all seen IDs in a Python set). We must bind memory to only elements within the active watermark interval.
2. **Data Structure Selection**:
   - `max_event_time`: Monotonically tracks the highest event timestamp observed so far.
   - `seen_ids`: Hash map mapping `event_id -> event_timestamp` for O(1) membership lookup.
   - `expiry_min_heap`: Min-heap storing `(event_timestamp, event_id)` pairs to identify and evict expired IDs in O(log M) time without scanning the entire map.
3. **Processing Steps**:
   - Compute current watermark = `max_event_time - watermark_delay_seconds`.
   - If incoming `event_timestamp < watermark`, drop immediately (late arrival).
   - If incoming `event_id` is already in `seen_ids`, drop (duplicate within window).
   - Otherwise, accept: update `max_event_time`, insert into `seen_ids`, push to heap.
   - Run lazy eviction: pop from heap while `heap[0].timestamp < new_watermark`, deleting evicted IDs from `seen_ids`.
4. **Edge Cases**: Out-of-order events arriving within the allowable watermark must be accepted. Duplicate events arriving with different timestamps should be checked against previous record timestamp.""",
        "code": """import heapq
from typing import Dict, Tuple

class StreamDeduplicator:
    \"\"\"
    Real-time event stream deduplicator with bounded watermarking and TTL eviction.
    Guarantees exactly-once stream processing within a configurable time window.
    \"\"\"
    def __init__(self, watermark_delay_seconds: int):
        self.watermark_delay = watermark_delay_seconds
        self.max_event_time: int = 0
        self.seen_events: Dict[str, int] = {}  # event_id -> timestamp
        self.expiry_heap: list[Tuple[int, str]] = []  # (timestamp, event_id)

    def process_event(self, event_id: str, timestamp: int) -> bool:
        \"\"\"
        Processes an incoming event. Returns True if event is valid and accepted, 
        or False if it is a duplicate or arrived past the watermark threshold.
        \"\"\"
        # Calculate current watermark boundary
        watermark = self.max_event_time - self.watermark_delay
        
        # Rule 1: Reject events that arrive older than the active watermark
        if self.max_event_time > 0 and timestamp < watermark:
            return False
            
        # Rule 2: Check if event_id has already been processed within the retention window
        if event_id in self.seen_events:
            return False
            
        # Update high-watermark anchor if this event advances the global timeline
        if timestamp > self.max_event_time:
            self.max_event_time = timestamp
            # Update watermark and evict expired records
            new_watermark = self.max_event_time - self.watermark_delay
            self._evict_expired(new_watermark)
            
        # Register the valid event in memory and heap
        self.seen_events[event_id] = timestamp
        heapq.heappush(self.expiry_heap, (timestamp, event_id))
        return True

    def _evict_expired(self, watermark: int) -> None:
        \"\"\"
        Evicts all event records from memory whose timestamps fall behind the new watermark.
        \"\"\"
        while self.expiry_heap and self.expiry_heap[0][0] < watermark:
            expired_time, expired_id = heapq.heappop(self.expiry_heap)
            # Only remove if the timestamp matches the latest registered timestamp
            if self.seen_events.get(expired_id) == expired_time:
                del self.seen_events[expired_id]

# Verification
if __name__ == "__main__":
    dedup = StreamDeduplicator(watermark_delay_seconds=60)
    print("e1 @ 100:", dedup.process_event("e1", 100))  # True
    print("e1 @ 105:", dedup.process_event("e1", 105))  # False (Duplicate)
    print("e2 @ 170:", dedup.process_event("e2", 170))  # True (Advances watermark to 110)
    print("e3 @ 90 :", dedup.process_event("e3", 90))   # False (Too late, < 110)
    print("e4 @ 120:", dedup.process_event("e4", 120))  # True (Valid, >= 110)
""",
        "time_complexity": "O(log M) per accepted event, where M is the number of active unexpired events in the watermark window (due to heap push and pop). Lookups and drops take O(1) time.",
        "space_complexity": "O(M) - Space is bounded strictly by the volume of distinct events occurring within the `watermark_delay_seconds` interval."
    },

    # =========================================================================
    # PROBLEM 3: CHUNKED GROUP-BY & AGGREGATE ENGINE FROM SCRATCH
    # =========================================================================
    {
        "num": 3,
        "title": "Custom Chunked Group-By and Aggregate Engine (Streaming Reducer)",
        "category": "ETL & Data Processing",
        "problem_statement": """Data engineers frequently process files larger than available RAM. Implement a memory-efficient generator function `chunked_group_by_agg` that accepts an iterator/generator of record dictionaries and performs multi-column grouping and multi-metric aggregations (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`) without loading the entire dataset into memory simultaneously.

Input Signature:
records: Iterator[dict]
group_keys: List[str]
agg_specs: Dict[str, Tuple[str, str]]  # alias -> (metric_field, agg_func)

Example:
records = [
    {"region": "US-East", "service": "UberX", "fare": 25.0, "duration": 15},
    {"region": "US-East", "service": "UberX", "fare": 35.0, "duration": 25},
    {"region": "US-West", "service": "UberBlack", "fare": 60.0, "duration": 30},
    {"region": "US-East", "service": "UberXL", "fare": 45.0, "duration": 20},
]
group_by = ["region", "service"]
aggs = {
    "total_fare": ("fare", "SUM"),
    "avg_fare": ("fare", "AVG"),
    "trip_count": ("fare", "COUNT"),
    "max_duration": ("duration", "MAX")
}""",
        "thought_process": """1. **Memory Consideration**: If records arrive as a stream of 100M rows, calling `list(records)` causes Out-Of-Memory (OOM) failures. We must process records sequentially in single-pass streaming fashion.
2. **Intermediate State Accumulation**:
   - Rather than storing all raw rows per group, we maintain running accumulators per unique group key tuple.
   - For `SUM`: running sum `s`.
   - For `COUNT`: running count `c`.
   - For `AVG`: running sum `s` and running count `c` (derived as `s / c` at completion).
   - For `MIN` / `MAX`: running min / max values updated via `min(curr, val)` / `max(curr, val)`.
3. **Data Structure**:
   - `groups: Dict[Tuple, Dict[str, Any]]`: Maps group composite key tuple to its metric accumulator dictionary.
4. **Final Formatting**: After consuming the entire iterator, yield the materialized result dictionaries one by one.
5. **Edge Cases**: Missing fields in record dictionaries handled defensively with `get()` or default skips; empty input stream yields empty generator; division by zero on empty counts prevented.""",
        "code": """from typing import Iterator, Dict, List, Tuple, Any

def chunked_group_by_agg(
    records: Iterator[Dict[str, Any]],
    group_keys: List[str],
    agg_specs: Dict[str, Tuple[str, str]]
) -> Iterator[Dict[str, Any]]:
    \"\"\"
    Performs memory-efficient group-by and aggregation over an iterable record stream.
    
    :param records: Streaming iterator yielding individual dictionary records.
    :param group_keys: List of dictionary keys to group by.
    :param agg_specs: Mapping of output_alias -> (field_name, aggregation_function).
                      Supported functions: 'SUM', 'COUNT', 'AVG', 'MIN', 'MAX'.
    :return: Iterator yielding aggregated summary dictionaries.
    \"\"\"
    # Map: group_tuple -> {alias: accumulator_state}
    acc_store: Dict[Tuple[Any, ...], Dict[str, Any]] = {}
    
    for row in records:
        # Extract composite group key as immutable tuple
        group_val = tuple(row.get(k) for k in group_keys)
        
        if group_val not in acc_store:
            # Initialize accumulator slots for each aggregation specification
            state: Dict[str, Any] = {}
            for alias, (col, func) in agg_specs.items():
                f_upper = func.upper()
                if f_upper == "SUM":
                    state[alias] = 0.0
                elif f_upper == "COUNT":
                    state[alias] = 0
                elif f_upper == "AVG":
                    state[alias] = {"sum": 0.0, "count": 0}
                elif f_upper == "MIN":
                    state[alias] = float("inf")
                elif f_upper == "MAX":
                    state[alias] = float("-inf")
                else:
                    raise ValueError(f"Unsupported aggregation operator: {func}")
            acc_store[group_val] = state
            
        group_acc = acc_store[group_val]
        
        # Accumulate metrics
        for alias, (col, func) in agg_specs.items():
            val = row.get(col)
            if val is None:
                continue  # Skip NULL values in metric calculation
                
            f_upper = func.upper()
            if f_upper == "SUM":
                group_acc[alias] += float(val)
            elif f_upper == "COUNT":
                group_acc[alias] += 1
            elif f_upper == "AVG":
                group_acc[alias]["sum"] += float(val)
                group_acc[alias]["count"] += 1
            elif f_upper == "MIN":
                if float(val) < group_acc[alias]:
                    group_acc[alias] = float(val)
            elif f_upper == "MAX":
                if float(val) > group_acc[alias]:
                    group_acc[alias] = float(val)

    # Finalization phase: emit formatted aggregated dictionaries
    for group_val, metrics in acc_store.items():
        out_row = {k: v for k, v in zip(group_keys, group_val)}
        for alias, (col, func) in agg_specs.items():
            f_upper = func.upper()
            if f_upper == "AVG":
                c = metrics[alias]["count"]
                out_row[alias] = (metrics[alias]["sum"] / c) if c > 0 else None
            elif f_upper in ("MIN", "MAX"):
                v = metrics[alias]
                out_row[alias] = None if v in (float("inf"), float("-inf")) else v
            else:
                out_row[alias] = metrics[alias]
        yield out_row

# Verification
if __name__ == "__main__":
    sample_records = iter([
        {"region": "US-East", "service": "UberX", "fare": 25.0, "duration": 15},
        {"region": "US-East", "service": "UberX", "fare": 35.0, "duration": 25},
        {"region": "US-West", "service": "UberBlack", "fare": 60.0, "duration": 30},
        {"region": "US-East", "service": "UberXL", "fare": 45.0, "duration": 20},
    ])
    g_keys = ["region", "service"]
    a_specs = {
        "total_fare": ("fare", "SUM"),
        "avg_fare": ("fare", "AVG"),
        "trip_count": ("fare", "COUNT"),
        "max_duration": ("duration", "MAX")
    }
    for res in chunked_group_by_agg(sample_records, g_keys, a_specs):
        print(res)
""",
        "time_complexity": "O(N * A) where N is the total number of incoming streaming rows and A is the number of aggregation specifications. Every record is processed in a single pass.",
        "space_complexity": "O(G * A) where G is the cardinality of unique group combinations and A is the number of aggregation metrics. Memory is independent of total row count N."
    },

    # =========================================================================
    # PROBLEM 4: MERGE K SORTED INGESTION STREAMS (MIN-HEAP / K-WAY MERGE)
    # =========================================================================
    {
        "num": 4,
        "title": "Merge K Sorted Partitioned Event Logs (K-Way Merge with Min-Heap)",
        "category": "Data Streaming & Ingestion",
        "problem_statement": """In distributed ingestion architectures, multiple Kafka partition files or log files are individually sorted by event timestamp. Given K sorted iterators/streams of log events where each event is a dictionary `{"timestamp": int, "payload": str}`, merge them into a single sorted output stream.

Example:
Stream 0: [{"timestamp": 10, "payload": "A1"}, {"timestamp": 30, "payload": "A2"}]
Stream 1: [{"timestamp": 5,  "payload": "B1"}, {"timestamp": 25, "payload": "B2"}]
Stream 2: [{"timestamp": 15, "payload": "C1"}, {"timestamp": 40, "payload": "C2"}]

Merged Output:
[5, "B1"], [10, "A1"], [15, "C1"], [25, "B2"], [30, "A2"], [40, "C2"]""",
        "thought_process": """1. **Brute Force**: Concatenate all K streams into a single list and sort it. If there are K streams each with M elements, total elements N = K * M. Sorting takes O(N log N) time and requires O(N) memory, which is catastrophic when logs are gigabytes in size.
2. **Optimal Approach (K-Way Min-Heap Merge)**:
   - Since each individual input stream is already sorted, we only need to compare the earliest unconsumed element from each of the K streams at any point in time.
   - We initialize a min-heap with the first element of each non-empty stream: `(event["timestamp"], stream_index, event)`.
   - Repeatedly pop the smallest element from the heap, yield it to the caller, and fetch the next event from that exact same stream (`stream_index`).
   - If that stream has another element, push it into the heap.
   - Repeat until the heap is empty.
3. **Tie-Breaking**: In Python, when heap tuples have matching timestamps, comparing the next tuple item (`stream_index`) breaks ties deterministically without attempting to compare non-comparable dictionary objects.
4. **Edge Cases**: Empty streams in input list are ignored during initialization; streams with unequal lengths handled gracefully when iterators exhaust.""",
        "code": """import heapq
from typing import Iterator, List, Dict, Any, Tuple

def merge_k_sorted_streams(streams: List[Iterator[Dict[str, Any]]]) -> Iterator[Dict[str, Any]]:
    \"\"\"
    Merges K timestamp-sorted event streams into a single globally sorted stream using a min-heap.
    
    :param streams: List of iterators yielding timestamp-ordered event dictionaries.
    :return: Generator yielding events in ascending timestamp order.
    \"\"\"
    # Min-heap storing: (timestamp, stream_idx, event_dict)
    heap: List[Tuple[int, int, Dict[str, Any]]] = []
    
    # Initialize heap with the first event from each active stream
    for idx, stream in enumerate(streams):
        try:
            first_event = next(stream)
            heapq.heappush(heap, (first_event["timestamp"], idx, first_event))
        except StopIteration:
            # Stream is empty, ignore
            continue
            
    # Process until all streams are completely consumed
    while heap:
        ts, stream_idx, event = heapq.heappop(heap)
        yield event
        
        # Advance the specific stream from which the minimum event was pulled
        try:
            next_event = next(streams[stream_idx])
            heapq.heappush(heap, (next_event["timestamp"], stream_idx, next_event))
        except StopIteration:
            # This stream is exhausted, continue processing remaining streams
            pass

# Verification
if __name__ == "__main__":
    s0 = iter([{"timestamp": 10, "payload": "A1"}, {"timestamp": 30, "payload": "A2"}])
    s1 = iter([{"timestamp": 5,  "payload": "B1"}, {"timestamp": 25, "payload": "B2"}])
    s2 = iter([{"timestamp": 15, "payload": "C1"}, {"timestamp": 40, "payload": "C2"}])
    
    merged = merge_k_sorted_streams([s0, s1, s2])
    for ev in merged:
        print(f"Timestamp: {ev['timestamp']:02d} | Payload: {ev['payload']}")
""",
        "time_complexity": "O(N log K) where N is the total number of events across all streams and K is the number of streams. Each event undergoes exactly one heap push and one heap pop of size K.",
        "space_complexity": "O(K) - The heap holds at most one element per active input stream at any time, requiring negligible memory even for massive log datasets."
    },

    # =========================================================================
    # PROBLEM 5: DETECT CIRCULAR DEPENDENCIES IN PIPELINE DAGS
    # =========================================================================
    {
        "num": 5,
        "title": "Detect Circular Dependencies in Pipeline DAGs (Topological Sort / Kahn's)",
        "category": "Orchestration & Graph Algorithms",
        "problem_statement": """In workflow orchestration platforms like Apache Airflow or dbt, tasks and models form Directed Acyclic Graphs (DAGs). A circular dependency causes infinite execution loops and scheduler deadlocks. 
Given a list of tasks and a list of directed dependency edges `(upstream_task, downstream_task)` where `upstream_task -> downstream_task`, determine:
1. Whether the workflow contains a circular dependency (is NOT a valid DAG).
2. If valid, return a valid topological execution order.
3. If invalid, identify tasks participating in or affected by cyclic dependencies.

Example 1:
tasks = ["extract", "transform", "test", "load"]
edges = [("extract", "transform"), ("transform", "test"), ("test", "load")]
Output: Valid DAG, Execution Order: ["extract", "transform", "test", "load"]

Example 2:
tasks = ["A", "B", "C"]
edges = [("A", "B"), ("B", "C"), ("C", "A")]
Output: Invalid (Cycle Detected), Cyclic Tasks: ["A", "B", "C"]""",
        "thought_process": """1. **Algorithm Selection**: Kahn's Algorithm (BFS-based Topological Sort) is ideal for workflow scheduling because it mimics how an orchestration engine executes tasks:
   - Compute the in-degree (number of prerequisite upstream dependencies) for every task.
   - Initialize a FIFO queue with all tasks possessing `in_degree == 0` (tasks with no upstream blockers that can run immediately).
   - While queue is not empty:
     - Dequeue task `u`, append `u` to execution plan.
     - For each downstream dependent task `v` of `u`, decrement `in_degree[v]`.
     - If `in_degree[v]` reaches 0, enqueue `v`.
   - After queue is exhausted, if the number of scheduled tasks equals the total task count, the graph is a valid DAG.
   - If scheduled count < total task count, a cycle exists. Any task with `in_degree > 0` is locked in a cyclic deadlock.
2. **Edge Cases**: Disconnected components (independent sub-DAGs), self-referencing loops `("A", "A")`, isolated nodes with no edges.""",
        "code": """from collections import deque, defaultdict
from typing import List, Tuple, Dict, Set

def validate_pipeline_dag(
    tasks: List[str], 
    dependencies: List[Tuple[str, str]]
) -> Tuple[bool, List[str], Set[str]]:
    \"\"\"
    Validates a pipeline DAG using Kahn's algorithm (Topological Sort).
    
    :param tasks: List of all task identifiers.
    :param dependencies: List of directed edges as (upstream_task, downstream_task).
    :return: (is_valid_dag, topological_order, cyclic_tasks)
    \"\"\"
    adj_list: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {t: 0 for t in tasks}
    
    # Build adjacency list and compute in-degrees
    for upstream, downstream in dependencies:
        adj_list[upstream].append(downstream)
        in_degree[downstream] = in_degree.get(downstream, 0) + 1
        
    # Queue all root tasks with 0 upstream dependencies
    queue: deque[str] = deque([t for t in tasks if in_degree[t] == 0])
    execution_order: List[str] = []
    
    while queue:
        curr_task = queue.popleft()
        execution_order.append(curr_task)
        
        # Decrement dependency counters for all downstream dependents
        for downstream in adj_list[curr_task]:
            in_degree[downstream] -= 1
            if in_degree[downstream] == 0:
                queue.append(downstream)
                
    # If all tasks were scheduled, graph is acyclic
    if len(execution_order) == len(tasks):
        return True, execution_order, set()
    else:
        # Tasks with in_degree > 0 are involved in cycles
        cyclic_tasks = {t for t, deg in in_degree.items() if deg > 0}
        return False, [], cyclic_tasks

# Verification
if __name__ == "__main__":
    valid_tasks = ["extract_raw", "stage_dbt", "data_quality_test", "load_bi_mart"]
    valid_deps = [
        ("extract_raw", "stage_dbt"),
        ("stage_dbt", "data_quality_test"),
        ("data_quality_test", "load_bi_mart")
    ]
    is_valid, order, _ = validate_pipeline_dag(valid_tasks, valid_deps)
    print(f"Valid Pipeline: {is_valid} | Order: {order}")
    
    cyclic_tasks = ["task_A", "task_B", "task_C", "task_D"]
    cyclic_deps = [
        ("task_A", "task_B"),
        ("task_B", "task_C"),
        ("task_C", "task_A"),
        ("task_C", "task_D")
    ]
    is_valid_c, _, cycles = validate_pipeline_dag(cyclic_tasks, cyclic_deps)
    print(f"Cyclic Pipeline: {is_valid_c} | Stuck Tasks: {cycles}")
""",
        "time_complexity": "O(V + E) where V is the number of tasks and E is the number of dependency relationships. Every node and edge is traversed once.",
        "space_complexity": "O(V + E) to store the adjacency list, in-degree mappings, and BFS traversal queue."
    },

    # =========================================================================
    # PROBLEM 6: TOKEN BUCKET RATE LIMITER FOR API INGESTION
    # =========================================================================
    {
        "num": 6,
        "title": "Thread-Safe Token Bucket Rate Limiter for Ingestion Connectors",
        "category": "System Design & Concurrency",
        "problem_statement": """When extracting data from third-party SaaS APIs (e.g., Salesforce, Stripe, SAP) in data pipelines, connectors must strictly respect API rate limits to prevent HTTP 429 (Too Many Requests) errors. 
Implement a thread-safe `TokenBucketRateLimiter` that allows up to `capacity` tokens, replenishing at `refill_rate` tokens per second. The class should provide an acquire method `acquire(tokens=1)` that blocks or returns boolean approval.""",
        "thought_process": """1. **Algorithm Concept**: The Token Bucket algorithm allows bursts up to bucket capacity while enforcing an average rate of consumption over time:
   - The bucket holds up to `capacity` tokens.
   - Tokens replenish smoothly at rate `refill_rate` tokens per second.
   - Rather than spinning a background thread that constantly adds tokens (which wastes CPU and causes lock contention), compute tokens lazily upon each request based on elapsed time:
     `new_tokens = elapsed_time * refill_rate`.
   - Update `current_tokens = min(capacity, current_tokens + new_tokens)`.
   - If `current_tokens >= requested`, deduct and return `True`.
2. **Concurrency & Thread Safety**: Data pipelines often run extraction workers in multi-threaded pools. All token checks and state updates must be guarded by a `threading.Lock`.
3. **Edge Cases**: Rapid bursts under capacity succeed immediately; requests demanding more tokens than capacity are clamped or rejected; floating point precision timing handled gracefully.""",
        "code": """import time
import threading

class TokenBucketRateLimiter:
    \"\"\"
    Thread-safe lazy-refill Token Bucket Rate Limiter for API extraction pipelines.
    \"\"\"
    def __init__(self, capacity: float, refill_rate: float):
        \"\"\"
        :param capacity: Maximum burst size (maximum tokens bucket can hold).
        :param refill_rate: Tokens added per second.
        \"\"\"
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.current_tokens = float(capacity)
        self.last_refill_timestamp = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, tokens: float = 1.0, blocking: bool = True, timeout: float = 10.0) -> bool:
        \"\"\"
        Attempts to acquire the specified number of tokens.
        
        :param tokens: Number of tokens requested.
        :param blocking: If True, sleeps until tokens become available or timeout expires.
        :param timeout: Maximum seconds to block waiting for tokens.
        :return: True if tokens were acquired, False otherwise.
        \"\"\"
        if tokens > self.capacity:
            raise ValueError(f"Requested {tokens} tokens exceeds maximum capacity {self.capacity}")

        deadline = time.monotonic() + timeout

        while True:
            with self._lock:
                now = time.monotonic()
                elapsed = now - self.last_refill_timestamp
                self.last_refill_timestamp = now
                
                # Replenish tokens based on elapsed time
                self.current_tokens = min(self.capacity, self.current_tokens + elapsed * self.refill_rate)
                
                # Check if sufficient tokens are available
                if self.current_tokens >= tokens:
                    self.current_tokens -= tokens
                    return True
                    
                if not blocking:
                    return False
                    
                # Calculate sleep duration until enough tokens replenish
                needed = tokens - self.current_tokens
                wait_time = needed / self.refill_rate
                
            # If wait exceeds deadline, abort
            if time.monotonic() + wait_time > deadline:
                return False
                
            time.sleep(min(wait_time, 0.05))

# Verification
if __name__ == "__main__":
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2)
    # Burst 5 requests
    for i in range(5):
        print(f"Req {i+1}: {limiter.acquire(1, blocking=False)}")
    # 6th immediate request should fail without blocking
    print(f"Req 6 (instant): {limiter.acquire(1, blocking=False)}")
    # 7th request with blocking waits for token refill
    print(f"Req 7 (blocking): {limiter.acquire(1, blocking=True)}")
""",
        "time_complexity": "O(1) - Lazy token calculation involves constant time mathematical calculations and conditional checks.",
        "space_complexity": "O(1) - Requires constant scalar storage for timestamps, token count, and lock primitive."
    },

    # =========================================================================
    # PROBLEM 7: LRU CACHE IMPLEMENTATION FOR METADATA CACHING
    # =========================================================================
    {
        "num": 7,
        "title": "LRU Cache for Pipeline Schema & Metadata Caching (Doubly Linked List + Hash Map)",
        "category": "Data Structures & Caching",
        "problem_statement": """In data transformation engines, looking up remote catalog schemas, user permissions, or partition metadata over network APIs is expensive. Implement a Least Recently Used (LRU) Cache from scratch supporting:
- `get(key: str) -> Any`: Returns the cached item or -1 if not found. Accessing an item marks it as most recently used.
- `put(key: str, value: Any) -> None`: Updates or inserts the key-value pair. If capacity is exceeded, evict the least recently used key.
Both operations must run in strict O(1) average time complexity.""",
        "thought_process": """1. **Data Structure Architecture**:
   - A Hash Map provides O(1) key lookup, but cannot maintain chronological access order efficiently.
   - An Array or Python list can maintain order, but deleting/moving an arbitrary element takes O(N) time.
   - Combining a **Hash Map with a Doubly Linked List** achieves O(1) for both lookups and position shifts:
     - The Hash Map maps `key -> Node`.
     - The Doubly Linked List maintains nodes in access order: head contains the Least Recently Used (LRU) node, and tail contains the Most Recently Used (MRU) node.
     - Using dummy `head` and `tail` sentinel nodes completely eliminates boundary null checks during insertion and removal.
2. **Operations**:
   - `_remove(node)`: Unlinks node by updating `node.prev.next = node.next` and `node.next.prev = node.prev`.
   - `_add_to_tail(node)`: Inserts node right before dummy tail.
   - `get(key)`: If key exists, move its node to tail and return value.
   - `put(key, val)`: If key exists, update value and move to tail. If new and capacity full, remove node right after dummy head, delete from hash map, then insert new node at tail.""",
        "code": """from typing import Any, Optional, Dict

class Node:
    \"\"\"Doubly linked list node storing key, value, and neighbor pointers.\"\"\"
    def __init__(self, key: str = "", value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCache:
    \"\"\"
    O(1) Least Recently Used (LRU) Cache utilizing a Hash Map and Doubly Linked List.
    \"\"\"
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[str, Node] = {}
        
        # Sentinel dummy nodes
        self.head = Node()  # LRU sentinel
        self.tail = Node()  # MRU sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        \"\"\"Unlinks an existing node from the doubly linked list in O(1).\"\"\"
        p = node.prev
        n = node.next
        if p and n:
            p.next = n
            n.prev = p

    def _add_to_tail(self, node: Node) -> None:
        \"\"\"Appends a node right before the tail sentinel (marks as MRU) in O(1).\"\"\"
        p = self.tail.prev
        if p:
            p.next = node
            node.prev = p
            node.next = self.tail
            self.tail.prev = node

    def get(self, key: str) -> Any:
        \"\"\"Fetches value and marks key as MRU. Returns -1 if key does not exist.\"\"\"
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.value

    def put(self, key: str, value: Any) -> None:
        \"\"\"Inserts or updates value. Evicts LRU item if capacity is exceeded.\"\"\"
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_tail(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict LRU node (immediately following head sentinel)
                lru = self.head.next
                if lru and lru != self.tail:
                    self._remove(lru)
                    del self.cache[lru.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_tail(new_node)

# Verification
if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("schema_trips", "v1.0")
    cache.put("schema_drivers", "v2.1")
    print("trips:", cache.get("schema_trips"))  # Returns v1.0, marks as MRU
    cache.put("schema_surge", "v1.5")           # Evicts schema_drivers (LRU)
    print("drivers:", cache.get("schema_drivers"))  # Returns -1 (evicted)
    print("surge:", cache.get("schema_surge"))      # Returns v1.5
""",
        "time_complexity": "O(1) strict for both `get` and `put` operations, guaranteed by direct hash table lookup and pointer manipulation in the doubly linked list.",
        "space_complexity": "O(C) where C is the maximum cache capacity."
    },

    # =========================================================================
    # PROBLEM 8: CUSTOM FLAT-FILE SCHEMA VALIDATOR & ANOMALY DETECTOR
    # =========================================================================
    {
        "num": 8,
        "title": "Streaming Flat-File Schema Validator & Data Contract Gatekeeper",
        "category": "Data Quality & Contract Enforcement",
        "problem_statement": """Data pipelines ingesting CSV or delimited flat feeds frequently fail due to malformed rows, unescaped delimiters, and type casting violations. 
Write a streaming validator function `validate_delimited_stream` that parses a delimited line-by-line file generator against a formal schema contract.
Schema contract specifies:
- Column names and expected types (`int`, `float`, `str`, `date`)
- Nullability constraint (`nullable: bool`)
- Value range or regex pattern
The function must return a tuple: `(valid_records_generator, anomaly_summary_report)` without holding all valid records in memory simultaneously.""",
        "thought_process": """1. **Design Goals**:
   - High memory efficiency: stream valid parsed rows lazily via generator.
   - Comprehensive error capture: record exact line number, column name, violating value, and error reason for all anomalies.
2. **Validation Rules**:
   - Header validation: check column count and names match schema contract.
   - Row length check: verify row split matches expected column count.
   - Nullability check: if value is empty/null and `nullable=False`, flag violation.
   - Type parsing: attempt defensive casting (`int(v)`, `float(v)`, date parsing).
3. **Execution Architecture**:
   - Use an inner generator for valid records.
   - Track an external mutable anomaly collector dictionary recording total lines processed, valid lines, and detailed anomaly records.""",
        "code": """import re
from datetime import datetime
from typing import Iterator, Dict, Any, Tuple, List

SCHEMA_CONTRACT = {
    "trip_id": {"type": "str", "nullable": False, "regex": r"^TRIP_[0-9]+$"},
    "driver_id": {"type": "int", "nullable": False},
    "fare": {"type": "float", "nullable": False, "min": 0.0, "max": 10000.0},
    "trip_date": {"type": "date", "format": "%Y-%m-%d", "nullable": False}
}

def validate_delimited_stream(
    lines: Iterator[str],
    schema: Dict[str, Dict[str, Any]],
    delimiter: str = ","
) -> Tuple[Iterator[Dict[str, Any]], Dict[str, Any]]:
    \"\"\"
    Streams and validates delimited text records against a strict schema contract.
    \"\"\"
    report = {
        "total_lines_read": 0,
        "valid_count": 0,
        "error_count": 0,
        "anomalies": []
    }
    
    expected_cols = list(schema.keys())
    
    def record_generator() -> Iterator[Dict[str, Any]]:
        nonlocal report
        header_parsed = False
        
        for line_num, raw_line in enumerate(lines, start=1):
            report["total_lines_read"] += 1
            line = raw_line.strip()
            if not line:
                continue
                
            tokens = [t.strip() for t in line.split(delimiter)]
            
            # Step 1: Validate header row
            if not header_parsed:
                if tokens != expected_cols:
                    report["anomalies"].append({
                        "line": line_num,
                        "error": f"Header mismatch. Expected {expected_cols}, got {tokens}"
                    })
                    report["error_count"] += 1
                    return
                header_parsed = True
                continue
                
            # Step 2: Validate column count
            if len(tokens) != len(expected_cols):
                report["anomalies"].append({
                    "line": line_num,
                    "error": f"Column count mismatch: expected {len(expected_cols)}, got {len(tokens)}"
                })
                report["error_count"] += 1
                continue
                
            # Step 3: Validate individual fields
            row_dict: Dict[str, Any] = {}
            row_is_valid = True
            
            for col_name, val in zip(expected_cols, tokens):
                rules = schema[col_name]
                
                # Check nullability
                if val == "" or val.upper() == "NULL":
                    if not rules.get("nullable", True):
                        report["anomalies"].append({"line": line_num, "col": col_name, "error": "Non-nullable field is NULL"})
                        row_is_valid = False
                        break
                    row_dict[col_name] = None
                    continue
                    
                # Type validations
                t = rules.get("type")
                try:
                    if t == "int":
                        row_dict[col_name] = int(val)
                    elif t == "float":
                        f_val = float(val)
                        if "min" in rules and f_val < rules["min"]:
                            raise ValueError(f"Value {f_val} < min {rules['min']}")
                        row_dict[col_name] = f_val
                    elif t == "date":
                        dt = datetime.strptime(val, rules.get("format", "%Y-%m-%d"))
                        row_dict[col_name] = dt.date()
                    elif t == "str":
                        if "regex" in rules and not re.match(rules["regex"], val):
                            raise ValueError(f"Value '{val}' failed regex pattern {rules['regex']}")
                        row_dict[col_name] = val
                except Exception as err:
                    report["anomalies"].append({"line": line_num, "col": col_name, "error": str(err)})
                    row_is_valid = False
                    break
                    
            if row_is_valid:
                report["valid_count"] += 1
                yield row_dict
            else:
                report["error_count"] += 1

    return record_generator(), report

# Verification
if __name__ == "__main__":
    sample_csv = iter([
        "trip_id,driver_id,fare,trip_date",
        "TRIP_101,5501,24.50,2026-04-01",
        "TRIP_102,INVALID_ID,35.00,2026-04-01",  # Type error
        "TRIP_103,5503,-15.00,2026-04-01",       # Min value error
        "TRIP_104,5504,50.00,2026-04-01"         # Valid
    ])
    valid_stream, err_report = validate_delimited_stream(sample_csv, SCHEMA_CONTRACT)
    valid_rows = list(valid_stream)
    print("Valid Rows:", valid_rows)
    print("Audit Report:", err_report)
""",
        "time_complexity": "O(N * C) where N is the total number of lines in the file and C is the number of schema columns. Every token is validated in linear time.",
        "space_complexity": "O(1) memory footprint for the streaming generator; anomaly reporting memory scales only with the number of erroneous rows."
    },

    # =========================================================================
    # PROBLEM 9: DISTRIBUTED LOG EVENT SESSIONIZATION VIA TWO POINTERS
    # =========================================================================
    {
        "num": 9,
        "title": "User Event Sessionization with Inactivity Timeout Threshold",
        "category": "Log Analysis & Windowing",
        "problem_statement": """In clickstream and telemetry engineering, continuous user interactions must be grouped into distinct analytical 'sessions'. A session terminates if a user remains inactive for more than `session_inactivity_timeout` seconds.
Given an unsorted list of user interaction events `{"user_id": str, "timestamp": int, "event_name": str}`, return a list of aggregated sessions:
`{"user_id": str, "session_id": str, "start_time": int, "end_time": int, "event_count": int, "duration_sec": int}`.""",
        "thought_process": """1. **Partitioning & Sorting**:
   - Events arrive unordered across users. We must partition events by `user_id`.
   - Within each user partition, sort events chronologically by `timestamp`.
2. **Session Boundary Detection**:
   - Iterate through sorted events for each user.
   - Maintain active session state: `start_time`, `end_time`, and `event_count`.
   - For event `i`, if `event[i].timestamp - last_event.timestamp > session_inactivity_timeout`, the previous session has ended. Emit the completed session, increment session sequence counter, and initialize a new session.
   - Otherwise, extend the active session by setting `end_time = event[i].timestamp` and incrementing `event_count`.
3. **Complexity & Scale**: Sorting each user's event list of length $M$ takes $O(M \log M)$. Across all $N$ events, total sorting time is $O(N \log N)$ in worst case.""",
        "code": """from collections import defaultdict
from typing import List, Dict, Any

def sessionize_events(
    events: List[Dict[str, Any]], 
    inactivity_timeout_sec: int = 1800  # Default 30 minutes
) -> List[Dict[str, Any]]:
    \"\"\"
    Groups clickstream events into sessions based on inactivity time thresholds.
    \"\"\"
    if not events:
        return []

    # Step 1: Partition events by user_id
    user_events: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for ev in events:
        user_events[ev["user_id"]].append(ev)

    sessions: List[Dict[str, Any]] = []

    # Step 2: Process each user independently
    for user_id, u_events in user_events.items():
        # Sort chronologically
        u_events.sort(key=lambda x: x["timestamp"])

        session_num = 1
        sess_start = u_events[0]["timestamp"]
        sess_end = sess_start
        count = 1

        for i in range(1, len(u_events)):
            curr_ts = u_events[i]["timestamp"]
            diff = curr_ts - sess_end

            if diff > inactivity_timeout_sec:
                # Close out current session
                sessions.append({
                    "user_id": user_id,
                    "session_id": f"{user_id}_s{session_num}",
                    "start_time": sess_start,
                    "end_time": sess_end,
                    "event_count": count,
                    "duration_sec": sess_end - sess_start
                })
                # Reset for new session
                session_num += 1
                sess_start = curr_ts
                sess_end = curr_ts
                count = 1
            else:
                sess_end = curr_ts
                count += 1

        # Emit trailing final session
        sessions.append({
            "user_id": user_id,
            "session_id": f"{user_id}_s{session_num}",
            "start_time": sess_start,
            "end_time": sess_end,
            "event_count": count,
            "duration_sec": sess_end - sess_start
        })

    return sessions

# Verification
if __name__ == "__main__":
    logs = [
        {"user_id": "u1", "timestamp": 100, "event_name": "app_open"},
        {"user_id": "u1", "timestamp": 200, "event_name": "search_ride"},
        {"user_id": "u1", "timestamp": 2500, "event_name": "app_open"},  # Gap > 1800s -> New session
        {"user_id": "u2", "timestamp": 50, "event_name": "app_open"}
    ]
    res = sessionize_events(logs, inactivity_timeout_sec=1800)
    for s in res:
        print(s)
""",
        "time_complexity": "O(N log N) dominated by sorting events per user partition, where N is the total count of events across the dataset.",
        "space_complexity": "O(N) to group and store the partition events and materialized session summaries."
    },

    # =========================================================================
    # PROBLEM 10: SPARSE MATRIX / LARGE COORDINATE FORMAT MULTIPLICATION
    # =========================================================================
    {
        "num": 10,
        "title": "Sparse Matrix Multiplication in Coordinate (COO) Format",
        "category": "Mathematical & Vector Algorithms",
        "problem_statement": """In recommendation systems, feature stores, and graph analytics, matrices representing user-item interactions or geographic distance matrices are often 99%+ sparse. Storing them as dense 2D arrays causes extreme memory bloat.
Implement sparse matrix multiplication $C = A \times B$ where matrices $A$ and $B$ are represented in Coordinate (COO) format as lists of tuples: `(row_idx, col_idx, value)`.""",
        "thought_process": """1. **Mathematical Definition**: In matrix multiplication $C_{i, j} = \sum_k A_{i, k} \times B_{k, j}$.
   - A non-zero product only occurs when there exists a common index $k$ such that $A_{i, k} \neq 0$ and $B_{k, j} \neq 0$.
2. **Indexing Strategy**:
   - To avoid comparing all pairs of elements ($O(N_A \times N_B)$), index matrix $B$ by its row index:
     `b_rows: Dict[k, List[(j, val_b)]]`.
   - Iterate over non-zero elements in $A$: `(i, k, val_a)`.
   - Look up row $k$ in `b_rows`. For each matching `(j, val_b)`:
     `c_dict[(i, j)] += val_a * val_b`.
3. **Filtering & Output**: Convert the accumulated `c_dict` back into COO list format, filtering out any resulting zeroes.""",
        "code": """from collections import defaultdict
from typing import List, Tuple

# Type alias: Coordinate format tuple (row, col, value)
COOMatrix = List[Tuple[int, int, float]]

def multiply_sparse_matrices(
    mat_a: COOMatrix, 
    mat_b: COOMatrix
) -> COOMatrix:
    \"\"\"
    Multiplies two sparse matrices in Coordinate (COO) format.
    
    :param mat_a: List of non-zero entries (row, col, val) for Matrix A.
    :param mat_b: List of non-zero entries (row, col, val) for Matrix B.
    :return: Non-zero entries (row, col, val) of product Matrix C = A x B.
    \"\"\"
    # Index Matrix B by its row index: k -> list of (col_j, val)
    b_by_row: defaultdict[int, List[Tuple[int, float]]] = defaultdict(list)
    for k, j, val_b in mat_b:
        b_by_row[k].append((j, val_b))
        
    # Accumulate products into: (i, j) -> accumulated_sum
    c_accum: defaultdict[Tuple[int, int], float] = defaultdict(float)
    
    # Iterate through non-zero entries in A
    for i, k, val_a in mat_a:
        if k in b_by_row:
            for j, val_b in b_by_row[k]:
                c_accum[(i, j)] += val_a * val_b
                
    # Format output COO list, excluding zeros
    mat_c: COOMatrix = [
        (i, j, round(val, 6))
        for (i, j), val in c_accum.items()
        if abs(val) > 1e-9
    ]
    
    mat_c.sort(key=lambda x: (x[0], x[1]))
    return mat_c

# Verification
if __name__ == "__main__":
    # A = [[1, 0, 2], [0, 0, 3]] -> (0,0,1), (0,2,2), (1,2,3)
    A = [(0, 0, 1.0), (0, 2, 2.0), (1, 2, 3.0)]
    # B = [[0, 4], [0, 0], [5, 0]] -> (0,1,4), (2,0,5)
    B = [(0, 1, 4.0), (2, 0, 5.0)]
    
    # Expected C = A x B:
    # Row 0: 1*0 + 2*5 = 10 (col 0); 1*4 + 2*0 = 4 (col 1) -> (0,0,10), (0,1,4)
    # Row 1: 3*5 = 15 (col 0); 3*0 = 0 (col 1) -> (1,0,15)
    C = multiply_sparse_matrices(A, B)
    print("Matrix Product C:", C)
""",
        "time_complexity": "O(N_A + N_B + K_matches) where N_A and N_B are the counts of non-zero entries in A and B respectively. Significantly faster than dense O(N^3) multiplication.",
        "space_complexity": "O(N_B + N_C) to store the row index of B and the accumulator hash map for product matrix C."
    },

    # =========================================================================
    # PROBLEM 11: TOP K FREQUENT TELEMETRY EVENTS IN STREAMING DATA
    # =========================================================================
    {
        "num": 11,
        "title": "Top-K Frequent Telemetry Event Types (Min-Heap + Hash Map)",
        "category": "Streaming & Heaps",
        "problem_statement": """In real-time infrastructure monitoring, operators need to track the top K most frequent telemetry errors or event types across a stream of millions of events.
Given a list or stream of string event types `events` and an integer `k`, return the `k` most frequent events sorted by frequency in descending order. If two events have the same frequency, sort them alphabetically.

Example:
events = ["timeout", "auth_fail", "timeout", "disk_full", "timeout", "auth_fail", "net_reset"]
k = 2
Output: ["timeout", "auth_fail"]""",
        "thought_process": """1. **Counting**: Count event frequencies using a hash map (`collections.Counter`). This takes $O(N)$ time.
2. **Top-K Selection**:
   - Rather than sorting all $U$ unique elements ($O(U \log U)$), maintain a Min-Heap of size $K$.
   - For custom tie-breaking (equal counts sorted alphabetically), we define a custom comparator or tuple `(count, ReverseString(word))` so the min-heap evicts the lexicographically larger word when counts are tied.
   - Alternatively, use Python's `heapq.nsmallest` / `heapq.nlargest` with a custom key: `(-count, word)`.
3. **Complexity Tradeoff**: When unique keys $U$ are large and $K \ll U$, the min-heap method requires only $O(U \log K)$ time, preserving CPU cycles.""",
        "code": """from collections import Counter
import heapq
from typing import List

class Element:
    \"\"\"Helper wrapper to achieve correct min-heap eviction order.\"\"\"
    def __init__(self, word: str, count: int):
        self.word = word
        self.count = count

    def __lt__(self, other: 'Element') -> bool:
        # Lower count has higher eviction priority (min-heap)
        if self.count != other.count:
            return self.count < other.count
        # When counts match, reverse alphabetical order to evict later words first
        return self.word > other.word

def top_k_frequent_telemetry(events: List[str], k: int) -> List[str]:
    \"\"\"
    Finds top K most frequent event strings using a bounded min-heap of size K.
    \"\"\"
    if not events or k <= 0:
        return []
        
    counts = Counter(events)
    heap: List[Element] = []
    
    for word, count in counts.items():
        heapq.heappush(heap, Element(word, count))
        if len(heap) > k:
            heapq.heappop(heap)
            
    # Pop from heap and reverse to get descending frequency order
    result: List[str] = []
    while heap:
        result.append(heapq.heappop(heap).word)
        
    result.reverse()
    return result

# Verification
if __name__ == "__main__":
    test_events = ["timeout", "auth_fail", "timeout", "disk_full", "timeout", "auth_fail", "net_reset"]
    print("Top 2 Events:", top_k_frequent_telemetry(test_events, 2))
    # Output: ['timeout', 'auth_fail']
""",
        "time_complexity": "O(N + U log K) where N is the total event count and U is the count of distinct event types. When U is large, this is substantially faster than full sorting.",
        "space_complexity": "O(U) to store the frequency map, plus O(K) for the heap."
    },

    # =========================================================================
    # PROBLEM 12: INTERVAL MERGING & DOWNTIME CONSOLIDATION
    # =========================================================================
    {
        "num": 12,
        "title": "Merge Overlapping System Downtime & Maintenance Intervals",
        "category": "Intervals & Scheduling",
        "problem_statement": """Infrastructure nodes in a cluster report maintenance windows and unexpected outage intervals as `[start_time, end_time]`. Overlapping or contiguous intervals must be merged into unified downtime windows to compute net SLA downtime accurately.
Given an array of intervals `intervals`, merge all overlapping intervals and return the consolidated non-overlapping windows sorted by start time.

Example:
Input: intervals = [[10, 25], [20, 40], [50, 60], [55, 70], [80, 90]]
Output: [[10, 40], [50, 70], [80, 90]]
Explanation:
- [10, 25] and [20, 40] overlap -> merged into [10, 40]
- [50, 60] and [55, 70] overlap -> merged into [50, 70]
- [80, 90] has no overlap -> remains [80, 90]""",
        "thought_process": """1. **Sort First**: If intervals are ordered arbitrarily, comparing every interval against all others requires $O(N^2)$ brute force. If we sort intervals by their start time ($O(N \log N)$), overlapping intervals are guaranteed to appear consecutively.
2. **Linear Merge Scan**:
   - Initialize `merged = [intervals[0]]`.
   - Iterate through remaining intervals `curr = [start, end]`:
     - Compare `curr.start` with `merged[-1].end`.
     - If `curr.start <= merged[-1].end`, an overlap exists:
       update `merged[-1].end = max(merged[-1].end, curr.end)`.
     - If `curr.start > merged[-1].end`, no overlap:
       append `curr` directly into `merged`.
3. **Edge Cases**: Empty list returns empty list; identical intervals; completely nested intervals (e.g., `[1, 10]` and `[2, 5]`); contiguous touching intervals (e.g., `[1, 5]` and `[5, 8]`).""",
        "code": """from typing import List

def merge_downtime_intervals(intervals: List[List[int]]) -> List[List[int]]:
    \"\"\"
    Merges overlapping and adjacent interval windows.
    
    :param intervals: List of [start_time, end_time] pairs.
    :return: Merged list of non-overlapping intervals sorted by start time.
    \"\"\"
    if not intervals:
        return []
        
    # Step 1: Sort intervals by start time ascending
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged: List[List[int]] = [sorted_intervals[0]]
    
    # Step 2: Linear sweep to merge overlapping windows
    for current in sorted_intervals[1:]:
        prev = merged[-1]
        
        # Check if current interval overlaps or directly touches previous interval
        if current[0] <= prev[1]:
            # Merge by extending the end boundary to the maximum observed
            prev[1] = max(prev[1], current[1])
        else:
            # No overlap, append as new distinct window
            merged.append(current)
            
    return merged

# Verification
if __name__ == "__main__":
    test_intervals = [[10, 25], [20, 40], [50, 60], [55, 70], [80, 90]]
    res = merge_downtime_intervals(test_intervals)
    print("Merged Downtime Windows:", res)
    # Output: [[10, 40], [50, 70], [80, 90]]
""",
        "time_complexity": "O(N log N) dominated by sorting the N intervals. The subsequent merge scan runs in linear O(N) time.",
        "space_complexity": "O(N) to store the sorted array and output merged intervals."
    }
]
