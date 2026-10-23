# -*- coding: utf-8 -*-
"""
Part 2: Python Coding Problems 13 to 25 for Pavan Chandramouleswara
Senior Data Engineer Interview Preparation Suite.

Each problem includes:
- Problem Statement & Example
- Algorithmic Thought Process & Tradeoffs
- Clean, Typed Python Code with Extensive Comments
- Time & Space Complexity Analysis
"""

CODING_PROBLEMS_PART2 = [
    # =========================================================================
    # PROBLEM 13: FLATTEN NESTED HETEROGENEOUS JSON PAYLOADS
    # =========================================================================
    {
        "num": 13,
        "title": "Flatten Nested Heterogeneous JSON Payloads into Relational Rows",
        "category": "ETL & JSON Transformation",
        "problem_statement": """Data pipelines ingesting webhook payloads, MongoDB documents, or Kafka JSON topics frequently receive deeply nested, heterogeneous dictionaries with arbitrary nesting, arrays, and primitive fields.
Write a recursive function `flatten_json(nested_obj: dict, delimiter: str = '_') -> dict` that flattens arbitrary nesting into a single-level dictionary where keys are joined by the delimiter.
If an array contains objects, expand them with zero-indexed key notation (e.g. `items_0_price`).

Example:
Input:
{
    "trip": {
        "id": "T101",
        "fares": {"base": 12.5, "surge": 1.5},
        "passengers": [{"name": "Alice", "rating": 4.9}, {"name": "Bob", "rating": 5.0}]
    },
    "status": "COMPLETED"
}
Output:
{
    "trip_id": "T101",
    "trip_fares_base": 12.5,
    "trip_fares_surge": 1.5,
    "trip_passengers_0_name": "Alice",
    "trip_passengers_0_rating": 4.9,
    "trip_passengers_1_name": "Bob",
    "trip_passengers_1_rating": 5.0,
    "status": "COMPLETED"
}""",
        "thought_process": """1. **Recursive Traversal**:
   - Inspect the type of each value in the current dictionary:
     - If the value is a `dict`, recursively flatten it, prepending the parent key: `f"{prefix}{key}{delimiter}"`.
     - If the value is a `list`, iterate with index `i` and recursively flatten each element using key `f"{prefix}{key}{delimiter}{i}"`.
     - If the value is a primitive (`str`, `int`, `float`, `bool`, `None`), assign directly to the output dictionary: `out[f"{prefix}{key}"] = val`.
2. **Iterative vs. Recursive**: A recursive DFS is clean and handles standard nesting depth (typically < 100 levels).
3. **Edge Cases**: Empty dictionaries `{}`, empty arrays `[]`, `None` values, special characters in field names.""",
        "code": """from typing import Dict, Any, Union

def flatten_json(
    nested_obj: Dict[str, Any], 
    parent_key: str = "", 
    delimiter: str = "_"
) -> Dict[str, Any]:
    \"\"\"
    Flattens an arbitrarily nested JSON/dictionary structure into a single-level dictionary.
    
    :param nested_obj: The input nested dictionary.
    :param parent_key: Recursive key prefix accumulator.
    :param delimiter: Delimiter used to join nested key levels.
    :return: Flat single-level dictionary.
    \"\"\"
    items: Dict[str, Any] = {}
    
    for key, val in nested_obj.items():
        new_key = f"{parent_key}{delimiter}{key}" if parent_key else str(key)
        
        if isinstance(val, dict):
            # Recurse for nested dictionaries
            items.update(flatten_json(val, new_key, delimiter=delimiter))
        elif isinstance(val, list):
            # Recurse for arrays using index notation
            if len(val) == 0:
                items[new_key] = []
            else:
                for idx, elem in enumerate(val):
                    list_key = f"{new_key}{delimiter}{idx}"
                    if isinstance(elem, (dict, list)):
                        items.update(flatten_json(elem if isinstance(elem, dict) else {str(i): v for i, v in enumerate(elem)}, list_key, delimiter=delimiter))
                    else:
                        items[list_key] = elem
        else:
            # Primitive values (int, float, str, bool, None)
            items[new_key] = val
            
    return items

# Verification
if __name__ == "__main__":
    payload = {
        "trip": {
            "id": "T101",
            "fares": {"base": 12.5, "surge": 1.5},
            "passengers": [{"name": "Alice", "rating": 4.9}, {"name": "Bob", "rating": 5.0}]
        },
        "status": "COMPLETED"
    }
    flattened = flatten_json(payload)
    for k, v in flattened.items():
        print(f"{k}: {v}")
""",
        "time_complexity": "O(N) where N is the total number of nodes (keys + list elements + leaf values) in the JSON document. Each element is visited once.",
        "space_complexity": "O(D + N) where D is the maximum nesting depth (call stack frames) and N is the number of leaf elements in the flattened dictionary."
    },

    # =========================================================================
    # PROBLEM 14: SCD TYPE 2 DIMENSION HISTORY GENERATOR
    # =========================================================================
    {
        "num": 14,
        "title": "Slowly Changing Dimension Type 2 (SCD2) History Generator",
        "category": "Data Warehousing & Dimensional Modeling",
        "problem_statement": """In data warehousing, SCD Type 2 preserves historical changes by creating new records with effective date ranges (`valid_from`, `valid_to`, `is_current`).
Given a list of chronological change events for entities `{"entity_id": str, "attribute": str, "change_timestamp": str}`, generate a consolidated SCD Type 2 dimension table tracking every state transition. 
Set `valid_to` of the current record to `'9999-12-31'` and `is_current` to `True`. Previous records must have `is_current=False` with `valid_to` set to the timestamp of the succeeding state change.""",
        "thought_process": """1. **Partition and Sort**:
   - Group incoming mutation events by `entity_id`.
   - Sort each entity's events chronologically by `change_timestamp`.
2. **State Tracking**:
   - For each entity, iterate through its sorted changes.
   - Discard consecutive duplicate mutations where the attribute did not change.
   - For each valid state change at index `i`, its `valid_from` is its `change_timestamp`.
   - If a succeeding change `i + 1` exists, its `valid_to` is `events[i+1].change_timestamp` and `is_current = False`.
   - For the final record of the entity, `valid_to = '9999-12-31'` and `is_current = True`.
3. **Surrogate Key Generation**: Assign a deterministic surrogate key: `f"{entity_id}_{version}"`.""",
        "code": """from collections import defaultdict
from typing import List, Dict, Any

def generate_scd2_history(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    \"\"\"
    Transforms mutation events into an SCD Type 2 dimension historical table.
    \"\"\"
    if not events:
        return []
        
    # Group by entity_id
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for ev in events:
        grouped[ev["entity_id"]].append(ev)
        
    scd_rows: List[Dict[str, Any]] = []
    
    for entity_id, entity_events in grouped.items():
        # Sort chronologically by timestamp
        entity_events.sort(key=lambda x: x["change_timestamp"])
        
        # Deduplicate consecutive identical attributes
        deduped = []
        for ev in entity_events:
            if not deduped or deduped[-1]["attribute"] != ev["attribute"]:
                deduped.append(ev)
                
        # Generate versioned SCD2 records
        for i, ev in enumerate(deduped):
            version = i + 1
            valid_from = ev["change_timestamp"]
            is_last = (i == len(deduped) - 1)
            
            valid_to = "9999-12-31" if is_last else deduped[i + 1]["change_timestamp"]
            is_current = is_last
            
            scd_rows.append({
                "surrogate_key": f"{entity_id}_v{version}",
                "entity_id": entity_id,
                "attribute": ev["attribute"],
                "valid_from": valid_from,
                "valid_to": valid_to,
                "is_current": is_current
            })
            
    return scd_rows

# Verification
if __name__ == "__main__":
    changes = [
        {"entity_id": "D101", "attribute": "Silver", "change_timestamp": "2026-01-01"},
        {"entity_id": "D101", "attribute": "Gold",   "change_timestamp": "2026-03-15"},
        {"entity_id": "D101", "attribute": "Gold",   "change_timestamp": "2026-03-20"}, # Redundant
        {"entity_id": "D101", "attribute": "Platinum","change_timestamp": "2026-04-10"},
        {"entity_id": "D202", "attribute": "Standard","change_timestamp": "2026-02-01"}
    ]
    scd_table = generate_scd2_history(changes)
    for row in scd_table:
        print(row)
""",
        "time_complexity": "O(N log N) dominated by sorting the events per entity, where N is the total event count.",
        "space_complexity": "O(N) to store entity groupings and resulting SCD2 history records."
    },

    # =========================================================================
    # PROBLEM 15: BIG DATA CHUNKED FILE COMPACTION SIMULATOR
    # =========================================================================
    {
        "num": 15,
        "title": "Big Data File Compaction & Small Files Problem Resolution",
        "category": "Storage Optimization & Bin Packing",
        "problem_statement": """In data lakes (HDFS / Amazon S3), frequent small writes cause the 'Small Files Problem', overwhelming NameNodes and slowing down Spark queries.
Implement a file compaction simulator `compact_small_files` that accepts a list of file sizes in MB `file_sizes` and a target compacted file size `target_size_mb` (e.g. 128 MB or 256 MB Parquet target).
Using the **First Fit Decreasing (FFD)** greedy bin-packing algorithm, pack small files into the minimum number of target compacted files such that no compacted file exceeds `target_size_mb`. Return the file assignments and compaction summary.""",
        "thought_process": """1. **Small Files Problem**: Distributed query engines like Spark or Presto achieve optimal throughput when files are 128MB to 512MB (Parquet block size). Thousands of 5MB files cause severe metadata overhead and excessive random I/O.
2. **Algorithm (First Fit Decreasing)**:
   - FFD is a classical heuristic for the NP-hard Bin Packing Problem, guaranteeing an approximation factor bounded by $1111/9 × OPT + 1.
   - Sort the file sizes in descending order: `sorted_files = sorted(file_sizes, reverse=True)`.
   - Maintain a list of bins (compacted files), where each bin tracks its accumulated size and member file indices.
   - For each file size, scan existing bins from left to right. Place the file into the first bin where `bin.current_size + file_size <= target_size_mb`.
   - If no existing bin has enough capacity, allocate a new bin.
3. **Edge Cases**: Files strictly greater than `target_size_mb` are placed in their own individual bin (cannot be split).""",
        "code": """from typing import List, Dict, Any

def compact_small_files(file_sizes_mb: List[float], target_size_mb: float = 128.0) -> Dict[str, Any]:
    \"\"\"
    Simulates Parquet file compaction using First Fit Decreasing (FFD) bin packing.
    
    :param file_sizes_mb: List of small file sizes in megabytes.
    :param target_size_mb: Ideal target compacted file size (e.g., 128MB).
    :return: Dictionary containing compacted file bins and optimization metrics.
    \"\"\"
    if not file_sizes_mb:
        return {"compacted_files": [], "total_input_files": 0, "total_compacted_files": 0}

    # Step 1: Sort file sizes in descending order
    sorted_files = sorted(file_sizes_mb, reverse=True)
    
    # Bins: list of {"bin_id": int, "total_size": float, "files": List[float]}
    bins: List[Dict[str, Any]] = []
    
    # Step 2: First-Fit Placement
    for f_size in sorted_files:
        placed = False
        for b in bins:
            if b["total_size"] + f_size <= target_size_mb:
                b["files"].append(f_size)
                b["total_size"] = round(b["total_size"] + f_size, 2)
                placed = True
                break
                
        if not placed:
            # Allocate a new bin
            bins.append({
                "compacted_file_id": f"part_{len(bins):04d}.parquet",
                "total_size_mb": round(f_size, 2),
                "files": [f_size]
            })
            
    reduction_ratio = (len(file_sizes_mb) - len(bins)) / len(file_sizes_mb) * 100.0
    return {
        "compacted_files": bins,
        "total_input_files": len(file_sizes_mb),
        "total_compacted_files": len(bins),
        "file_reduction_pct": round(reduction_ratio, 2)
    }

# Verification
if __name__ == "__main__":
    small_files = [12.5, 45.0, 30.2, 85.0, 15.1, 95.0, 22.0, 18.5, 60.0, 10.0]
    res = compact_small_files(small_files, target_size_mb=128.0)
    print(f"Reduced {res['total_input_files']} small files -> {res['total_compacted_files']} compacted files ({res['file_reduction_pct']}% reduction):")
    for b in res["compacted_files"]:
        print(f"  {b['compacted_file_id']}: {b['total_size_mb']} MB (Files: {b['files']})")
""",
        "time_complexity": "O(N log N + N * B) where N is the number of files and B is the number of resulting compacted bins. B <= N.",
        "space_complexity": "O(N) to store file allocations across bins."
    },

    # =========================================================================
    # PROBLEM 16: BINARY SEARCH ON ROTATED TIMESTAMPED LOG FILE
    # =========================================================================
    {
        "num": 16,
        "title": "Search in Rotated Timestamped Log Array (Modified Binary Search)",
        "category": "Searching & Binary Search",
        "problem_statement": """In distributed round-robin or ring-buffered log files, timestamped records are continuously appended. When the buffer reaches max capacity, it wraps around and overwrites from the beginning, creating a sorted array that is rotated at an unknown pivot.
Given a rotated sorted array of integer timestamps `timestamps` and a `target` timestamp, find the index of `target`. If `target` is not present, return -1.
You must write an algorithm with $OO(log N) runtime complexity.

Example:
Input: timestamps = [170040, 170050, 170060, 170010, 170020, 170030], target = 170020
Output: 4""",
        "thought_process": """1. **Binary Search Invariant**: In a rotated sorted array, splitting the array in half at `mid` guarantees that at least one of the two halves (`[low, mid]` or `[mid, high]`) is strictly sorted.
2. **Identification of Sorted Half**:
   - If `nums[low] <= nums[mid]`, the left half is normally sorted.
     - Check if `target` falls within the range `[nums[low], nums[mid])`. If yes, search left (`high = mid - 1`); otherwise search right (`low = mid + 1`).
   - Otherwise, the right half `[mid, high]` is normally sorted.
     - Check if `target` falls within the range `(nums[mid], nums[high]]`. If yes, search right (`low = mid + 1`); otherwise search left (`high = mid - 1`).
3. **Complexity**: Standard binary search halves search space each iteration -> $OO(log N) time, $OO(1) space.""",
        "code": """from typing import List

def search_rotated_log_timestamps(timestamps: List[int], target: int) -> int:
    \"\"\"
    Searches for target timestamp in a rotated sorted array in O(log N) time.
    \"\"\"
    if not timestamps:
        return -1
        
    low = 0
    high = len(timestamps) - 1
    
    while low <= high:
        mid = (low + high) // 2
        
        if timestamps[mid] == target:
            return mid
            
        # Determine which half is sorted
        if timestamps[low] <= timestamps[mid]:
            # Left half is sorted
            if timestamps[low] <= target < timestamps[mid]:
                high = mid - 1  # Target is in the left sorted half
            else:
                low = mid + 1   # Target is in the right half
        else:
            # Right half is sorted
            if timestamps[mid] < target <= timestamps[high]:
                low = mid + 1   # Target is in the right sorted half
            else:
                high = mid - 1  # Target is in the left half
                
    return -1

# Verification
if __name__ == "__main__":
    logs = [170040, 170050, 170060, 170010, 170020, 170030]
    tgt = 170020
    idx = search_rotated_log_timestamps(logs, tgt)
    print(f"Target {tgt} found at index: {idx} (value = {logs[idx]})")
""",
        "time_complexity": "O(log N) - The search interval is halved on every iteration.",
        "space_complexity": "O(1) - Iterative pointer updates use strictly constant memory."
    },

    # =========================================================================
    # PROBLEM 17: LOWEST COMMON ANCESTOR IN DATA LINEAGE DEPENDENCY TREE
    # =========================================================================
    {
        "num": 17,
        "title": "Lowest Common Upstream Ancestor in Data Lineage Graph",
        "category": "Lineage Trees & Graph Algorithms",
        "problem_statement": """In enterprise data governance platforms (like AWS Glue or OpenLineage), two failing analytical models `Model_A` and `Model_B` share common upstream data dependencies. To pinpoint the earliest root-cause table that could have corrupted both models, find their Lowest Common Ancestor (LCA) in the directed acyclic dependency tree.
Given the root of the lineage tree and two target model nodes `node_a` and `node_b`, find their LCA node.""",
        "thought_process": """1. **Tree vs. General DAG**: In a lineage tree structure where every dataset descends from source roots:
   - An LCA of two nodes $p$ and $q$ is defined as the deepest node that has both $p$ and $q$ as descendants.
2. **Recursive Traversal**:
   - Base case: If current `root` is `None` or `root == node_a` or `root == node_b`, return `root`.
   - Recursively search left and right children:
     `left = find_lca(root.left, node_a, node_b)`
     `right = find_lca(root.right, node_a, node_b)`
   - If both `left` and `right` return non-None values, it means `node_a` is in one subtree and `node_b` is in the other subtree. Therefore, `root` is the Lowest Common Ancestor!
   - If only one side returns non-None, return that side.""",
        "code": """from typing import Optional

class LineageNode:
    \"\"\"Represents a dataset node in a data lineage dependency graph.\"\"\"
    def __init__(self, name: str, left: Optional['LineageNode'] = None, right: Optional['LineageNode'] = None):
        self.name = name
        self.left = left
        self.right = right

def find_lowest_common_lineage_ancestor(
    root: Optional[LineageNode], 
    node_a: LineageNode, 
    node_b: LineageNode
) -> Optional[LineageNode]:
    \"\"\"
    Finds the Lowest Common Ancestor (LCA) node for two models in a lineage tree.
    \"\"\"
    # Base cases: end of branch or matched target node
    if root is None or root == node_a or root == node_b:
        return root
        
    left_result = find_lowest_common_lineage_ancestor(root.left, node_a, node_b)
    right_result = find_lowest_common_lineage_ancestor(root.right, node_a, node_b)
    
    # If both branches return a node, root is the LCA
    if left_result and right_result:
        return root
        
    # Otherwise return whichever subtree found a target
    return left_result if left_result is not None else right_result

# Verification
if __name__ == "__main__":
    # Lineage Tree:
    #             raw_marketplace_trips
    #             /                   \
    #     stg_pricing               stg_riders
    #      /       \
    # dim_surge  fact_revenue
    dim_surge = LineageNode("dim_surge")
    fact_rev = LineageNode("fact_revenue")
    stg_riders = LineageNode("stg_riders")
    stg_pricing = LineageNode("stg_pricing", left=dim_surge, right=fact_rev)
    raw_trips = LineageNode("raw_marketplace_trips", left=stg_pricing, right=stg_riders)
    
    lca_node = find_lowest_common_lineage_ancestor(raw_trips, dim_surge, fact_rev)
    print(f"LCA of dim_surge and fact_revenue: {lca_node.name if lca_node else 'None'}")
    # Expected: stg_pricing
    
    lca_cross = find_lowest_common_lineage_ancestor(raw_trips, dim_surge, stg_riders)
    print(f"LCA of dim_surge and stg_riders: {lca_cross.name if lca_cross else 'None'}")
    # Expected: raw_marketplace_trips
""",
        "time_complexity": "O(N) where N is the number of nodes in the lineage tree. Every node is visited at most once.",
        "space_complexity": "O(H) where H is the height of the tree, corresponding to the recursion call stack depth."
    },

    # =========================================================================
    # PROBLEM 18: CONSISTENT HASHING RING WITH VIRTUAL NODES
    # =========================================================================
    {
        "num": 18,
        "title": "Consistent Hashing Ring with Virtual Nodes for Distributed Sharding",
        "category": "System Design & Distributed Data",
        "problem_statement": """In distributed databases and Kafka partition sharding, simple modulo hashing `hash(key) % N` causes catastrophic data shuffling whenever nodes are added or removed (nearly 100% of keys move).
Implement a `ConsistentHashRing` that:
1. Distributes keys across a logical hash ring $[0, 2^{32} - 1]$.
2. Supports adding (`add_node`) and removing (`remove_node`) physical cluster nodes.
3. Uses `num_replicas` virtual nodes per physical node to prevent hotspotting and ensure uniform partition distribution.
4. Provides `get_node(key: str) -> str` which maps an incoming key to the nearest node clockwise on the ring in $OO(log K) time using binary search.""",
        "thought_process": """1. **Concept**: In consistent hashing, both nodes and data keys are mapped onto a shared circular hash space.
   - An incoming key is hashed, and we find the first node whose hash is >= hash(key) by walking clockwise. If no node hash is larger, wrap around to the first node on the ring.
2. **Virtual Nodes**: A small number of physical nodes (e.g., 3) often cause uneven hash distribution. By creating $V$ virtual nodes per physical node (e.g. `node_id#1`, `node_id#2`), we achieve uniform distribution across the ring.
3. **Data Structures**:
   - `ring: Dict[int, str]`: Maps virtual hash integer to physical `node_id`.
   - `sorted_keys: List[int]`: Sorted list of virtual hash integers.
   - Lookup uses Python's `bisect.bisect_right` for $OO(log(N × V)) binary search.""",
        "code": """import hashlib
import bisect
from typing import List, Dict

class ConsistentHashRing:
    \"\"\"
    Consistent Hashing implementation with virtual nodes for distributed data sharding.
    \"\"\"
    def __init__(self, num_virtual_nodes: int = 100):
        self.num_virtual_nodes = num_virtual_nodes
        self.ring: Dict[int, str] = {}  # hash_value -> physical_node_id
        self.sorted_hashes: List[int] = []

    def _hash(self, key: str) -> int:
        \"\"\"Hashes key string to a 32-bit unsigned integer using MD5.\"\"\"
        digest = hashlib.md5(key.encode('utf-8')).hexdigest()
        return int(digest[:8], 16)

    def add_node(self, node_id: str) -> None:
        \"\"\"Adds a physical node and its virtual replicas to the hash ring.\"\"\"
        for i in range(self.num_virtual_nodes):
            v_key = f"{node_id}#vn_{i}"
            h = self._hash(v_key)
            self.ring[h] = node_id
            bisect.insort(self.sorted_hashes, h)

    def remove_node(self, node_id: str) -> None:
        \"\"\"Removes a physical node and its virtual replicas from the hash ring.\"\"\"
        for i in range(self.num_virtual_nodes):
            v_key = f"{node_id}#vn_{i}"
            h = self._hash(v_key)
            if h in self.ring:
                del self.ring[h]
                idx = bisect.bisect_left(self.sorted_hashes, h)
                if idx < len(self.sorted_hashes) and self.sorted_hashes[idx] == h:
                    self.sorted_hashes.pop(idx)

    def get_node(self, data_key: str) -> str:
        \"\"\"
        Maps data key to the closest clockwise node on the ring in O(log(N * V)) time.
        \"\"\"
        if not self.ring:
            raise RuntimeError("Hash ring is empty. No nodes available.")
            
        h = self._hash(data_key)
        # Binary search for the first node with hash >= h
        idx = bisect.bisect_right(self.sorted_hashes, h)
        
        # If past the end of the ring, wrap around to the first node
        if idx == len(self.sorted_hashes):
            idx = 0
            
        return self.ring[self.sorted_hashes[idx]]

# Verification
if __name__ == "__main__":
    ring = ConsistentHashRing(num_virtual_nodes=50)
    ring.add_node("node_us_east_1")
    ring.add_node("node_us_west_2")
    ring.add_node("node_eu_central_1")
    
    keys = ["driver_5501", "trip_9921", "rider_3342", "surge_zone_12"]
    for k in keys:
        print(f"Key '{k}' mapped to: {ring.get_node(k)}")
        
    print("\nRemoving node_us_west_2...")
    ring.remove_node("node_us_west_2")
    for k in keys:
        print(f"Key '{k}' remapped to: {ring.get_node(k)}")
""",
        "time_complexity": "Lookup: O(log(N * V)) where N is the number of physical nodes and V is the number of virtual nodes per physical node. Add/Remove: O(V log(N * V)).",
        "space_complexity": "O(N * V) to store virtual node hashes on the ring."
    },

    # =========================================================================
    # PROBLEM 19: LONGEST SUBSEQUENCE WITHOUT REPEATING KEYS
    # =========================================================================
    {
        "num": 19,
        "title": "Longest Non-Repeating Event Sequence in Telemetry Stream",
        "category": "Sliding Window & Hash Map",
        "problem_statement": """In clickstream sequence analysis, we want to find the maximum length of contiguous events where all event types are completely unique (no duplicates).
Given a string or list of event tokens `events`, return the length of the longest contiguous subsegment containing no duplicate events.

Example:
Input: events = ["login", "search", "view_item", "search", "checkout", "logout"]
Output: 4
Explanation: The longest contiguous subsegment of unique events is ["view_item", "search", "checkout", "logout"] of length 4.""",
        "thought_process": """1. **Sliding Window with Two Pointers**:
   - Maintain a window `[left, right]` where all elements inside are strictly unique.
   - Use a hash map `last_seen: Dict[event, index]` to store the most recent index where each event was observed.
2. **Window Expansion & Contraction**:
   - As `right` iterates from 0 to $N - 1$:
     - If `events[right]` is already in `last_seen` and its previous index is >= left:
       - We have encountered a duplicate. Jump `left = last_seen[events[right]] + 1` to skip the previous occurrence.
     - Update `last_seen[events[right]] = right`.
     - Update `max_len = max(max_len, right - left + 1)`.
3. **Complexity**: Each pointer moves at most $N$ steps forward -> $OO(N) linear time.""",
        "code": """from typing import List

def longest_unique_event_subsequence(events: List[str]) -> int:
    \"\"\"
    Computes length of the longest contiguous subsegment with no duplicate events.
    \"\"\"
    if not events:
        return 0
        
    last_seen = {}
    left = 0
    max_len = 0
    
    for right, ev in enumerate(events):
        if ev in last_seen and last_seen[ev] >= left:
            # Advance left pointer past the previous occurrence of this event
            left = last_seen[ev] + 1
            
        last_seen[ev] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len

# Verification
if __name__ == "__main__":
    stream = ["login", "search", "view_item", "search", "checkout", "logout"]
    res = longest_unique_event_subsequence(stream)
    print("Longest Unique Subsequence Length:", res)
    # Output: 4
""",
        "time_complexity": "O(N) where N is the length of the event sequence. Each element is examined once.",
        "space_complexity": "O(U) where U is the number of unique event types in the stream, stored in the hash map."
    },

    # =========================================================================
    # PROBLEM 20: DEADLOCK DETECTION IN CONCURRENT PIPELINE TRANSACTIONS
    # =========================================================================
    {
        "num": 20,
        "title": "Deadlock Detection in Concurrent Transactions (Cycle in Directed Graph)",
        "category": "Concurrency & Graph DFS",
        "problem_statement": """In high-concurrency analytical databases (e.g. Snowflake, BigQuery, Postgres), concurrent transactions acquire locks on multiple tables. When Transaction A holds Lock 1 and waits for Lock 2 (held by Transaction B), while Transaction B waits for Lock 1, a Deadlock occurs.
Given a Wait-For Graph represented as an adjacency list `waits_for: Dict[str, List[str]]` where `T1: [T2]` means Transaction T1 is waiting for Transaction T2 to release a lock, detect if a deadlock exists and return the participating transactions.""",
        "thought_process": """1. **Wait-For Graph Theory**: A deadlock in database systems is equivalent to the existence of a directed cycle in the Wait-For Graph.
2. **Three-Color Graph Coloring (DFS)**:
   - To detect cycles in a directed graph cleanly, use DFS with node state tracking:
     - `WHITE (0)`: Unvisited node.
     - `GRAY (1)`: Currently being visited (in current DFS recursion path).
     - `BLACK (2)`: Completely visited and verified acyclic.
   - If DFS encounters a `GRAY` node during traversal, a back-edge exists, confirming a cycle (deadlock)!
3. **Deadlock Recovery**: Once a cycle is detected, one of the transactions in the cycle must be aborted (the 'victim transaction') to break the deadlock.""",
        "code": """from typing import Dict, List, Set, Tuple

def detect_transaction_deadlock(waits_for: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    \"\"\"
    Detects deadlocks (cycles) in a transaction wait-for graph using 3-color DFS.
    
    :param waits_for: Dict mapping tx_id -> list of tx_ids it is waiting on.
    :return: (has_deadlock, cycle_path)
    \"\"\"
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[str, int] = {tx: WHITE for tx in waits_for}
    # Ensure all referenced downstream nodes are also initialized
    for targets in waits_for.values():
        for t in targets:
            if t not in color:
                color[t] = WHITE
                
    parent: Dict[str, str] = {}
    cycle_nodes: List[str] = []
    
    def dfs(u: str) -> bool:
        nonlocal cycle_nodes
        color[u] = GRAY
        
        for v in waits_for.get(u, []):
            if color[v] == GRAY:
                # Cycle detected! Reconstruct the cycle
                curr = u
                cycle_nodes.append(v)
                while curr != v:
                    cycle_nodes.append(curr)
                    curr = parent.get(curr, v)
                cycle_nodes.reverse()
                return True
            elif color[v] == WHITE:
                parent[v] = u
                if dfs(v):
                    return True
                    
        color[u] = BLACK
        return False
        
    for node in list(color.keys()):
        if color[node] == WHITE:
            if dfs(node):
                return True, cycle_nodes
                
    return False, []

# Verification
if __name__ == "__main__":
    # T1 -> T2 -> T3 -> T1 (Cycle / Deadlock)
    deadlocked_graph = {
        "T1": ["T2"],
        "T2": ["T3"],
        "T3": ["T1"],
        "T4": ["T2"]
    }
    has_dl, cycle = detect_transaction_deadlock(deadlocked_graph)
    print(f"Deadlock Detected: {has_dl} | Deadlocked Transactions: {cycle}")
""",
        "time_complexity": "O(V + E) where V is the number of transactions and E is the number of lock wait dependencies.",
        "space_complexity": "O(V) to maintain color status, parent pointers, and recursion stack."
    },

    # =========================================================================
    # PROBLEM 21: ROLLING Z-SCORE ANOMALY DETECTOR FOR OBSERVABILITY
    # =========================================================================
    {
        "num": 21,
        "title": "Rolling Z-Score Data Quality Anomaly Detector (Welford's Algorithm)",
        "category": "Data Quality & Numerical Algorithms",
        "problem_statement": """In data quality monitoring (like Great Expectations or Monte Carlo), data engineers track ingestion metrics (e.g. daily row counts, average trip fares). When a metric deviates by more than $Z$ standard deviations from its rolling historical mean, an anomaly alert must trigger.
Implement a streaming class `RollingZScoreDetector` with window size `window_size` and threshold `z_threshold`. It should process streaming numeric values one-by-one, computing the current Z-score and flagging whether the value is an anomaly without maintaining large history arrays.""",
        "thought_process": """1. **Z-Score Formula**: $ZZ = (x - μ) / σ. An anomaly occurs when |Z| >= z_threshold.
2. **Sliding Window Maintenance**:
   - Maintain a sliding window of the last $W$ values using a `deque`.
   - Maintain running sum Σ x and running sum of squares Σ x².
   - When a new value arrives, if the deque is full (size W), subtract the oldest value from the sums before appending the new value.
   - Mean μ = (Σ x) / W, Variance σ² = (Σ x² / W) - μ².
   - Standard deviation σ = √(max(0, σ²)).
3. **Numerical Stability**: When variance is near zero (e.g. identical values), avoid division by zero.""",
        "code": """from collections import deque
import math
from typing import Tuple

class RollingZScoreDetector:
    \"\"\"
    Streaming Z-score statistical anomaly detector over a bounded sliding window.
    \"\"\"
    def __init__(self, window_size: int = 30, z_threshold: float = 3.0):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.window: deque[float] = deque()
        self.sum_x: float = 0.0
        self.sum_x2: float = 0.0

    def observe(self, value: float) -> Tuple[bool, float, float, float]:
        \"\"\"
        Records a new observation. 
        Returns: (is_anomaly, z_score, current_mean, current_std)
        \"\"\"
        n = len(self.window)
        
        # We need at least 3 samples to compute meaningful baseline statistics
        if n < 3:
            self._add(value)
            return False, 0.0, value, 0.0
            
        mean = self.sum_x / n
        variance = (self.sum_x2 / n) - (mean ** 2)
        std = math.sqrt(max(0.0, variance))
        
        # Compute Z-score if std is non-zero
        z_score = 0.0
        is_anomaly = False
        if std > 1e-9:
            z_score = (value - mean) / std
            if abs(z_score) >= self.z_threshold:
                is_anomaly = True
                
        # Update rolling window state
        self._add(value)
        return is_anomaly, round(z_score, 2), round(mean, 2), round(std, 2)

    def _add(self, val: float) -> None:
        if len(self.window) >= self.window_size:
            old_val = self.window.popleft()
            self.sum_x -= old_val
            self.sum_x2 -= (old_val ** 2)
            
        self.window.append(val)
        self.sum_x += val
        self.sum_x2 += (val ** 2)

# Verification
if __name__ == "__main__":
    detector = RollingZScoreDetector(window_size=5, z_threshold=2.5)
    baseline = [100.0, 102.0, 99.0, 101.0, 100.5]
    for b in baseline:
        detector.observe(b)
        
    # Sudden anomaly: 10x spike
    is_ano, z, m, s = detector.observe(350.0)
    print(f"Spike 350.0 -> Anomaly: {is_ano} | Z-Score: {z} | Baseline Mean: {m} | Std: {s}")
""",
        "time_complexity": "O(1) strict per observation. Adding and evicting from sums and deque runs in constant time.",
        "space_complexity": "O(W) where W is the sliding window size."
    },

    # =========================================================================
    # PROBLEM 22: PRIORITY QUEUE TASK SCHEDULER WITH COOLING INTERVAL
    # =========================================================================
    {
        "num": 22,
        "title": "Pipeline Task Scheduler with Minimum Cooling Interval",
        "category": "Greedy & Priority Queue",
        "problem_statement": """In workflow executors, CPU-intensive ETL tasks of different types are assigned to worker pools. Tasks of the same type cannot be executed within `cooling_interval` time units of each other to prevent database lock contention. Idle slots can be filled with other tasks or idle CPU ticks.
Given a list of task types `tasks` (e.g. `["A", "A", "A", "B", "B", "B"]`) and an integer `cooling_interval = 2`, find the minimum total time units required to execute all tasks.

Example:
Input: tasks = ["A","A","A","B","B","B"], cooling_interval = 2
Output: 8
Explanation: A -> B -> idle -> A -> B -> idle -> A -> B (Total time: 8)""",
        "thought_process": """1. **Greedy Strategy**:
   - The task with the highest frequency represents the execution bottleneck. We should always prioritize scheduling the most frequent available task first.
2. **Max-Heap + Cooldown Queue**:
   - Count task frequencies with `collections.Counter`.
   - Insert negative counts into a Max-Heap (`heapq`).
   - Maintain a cooldown queue `cooldown: deque[(remaining_count, ready_time)]`.
   - In each time tick:
     - Check if any task in `cooldown` has reached `ready_time == current_time`. If so, push it back into the max-heap.
     - If the max-heap is not empty, pop the most frequent task, decrement its count, and if it still has remaining executions, append it to `cooldown` with `ready_time = current_time + cooling_interval + 1`.
     - Increment `current_time`.
   - Continue until both the heap and cooldown queue are completely empty.""",
        "code": """from collections import Counter, deque
import heapq
from typing import List

def least_interval_task_scheduler(tasks: List[str], cooling_interval: int) -> int:
    \"\"\"
    Computes minimum execution time units required to schedule all tasks with cooling intervals.
    \"\"\"
    if not tasks:
        return 0
    if cooling_interval == 0:
        return len(tasks)
        
    # Count task frequencies
    counts = Counter(tasks)
    # Max-heap storing negative counts
    max_heap = [-c for c in counts.values()]
    heapq.heapify(max_heap)
    
    # Cooldown queue: stores (remaining_neg_count, available_at_time)
    cooldown = deque()
    current_time = 0
    
    while max_heap or cooldown:
        current_time += 1
        
        # Release tasks from cooldown if ready
        if cooldown and cooldown[0][1] == current_time:
            ready_count, _ = cooldown.popleft()
            heapq.heappush(max_heap, ready_count)
            
        if max_heap:
            # Execute the most frequent available task
            neg_count = heapq.heappop(max_heap)
            remaining = neg_count + 1  # (since it's negative, adding 1 decreases count)
            
            if remaining < 0:
                cooldown.append((remaining, current_time + cooling_interval + 1))
                
    return current_time

# Verification
if __name__ == "__main__":
    t_list = ["A", "A", "A", "B", "B", "B"]
    c_int = 2
    print("Minimum Total Time Units:", least_interval_task_scheduler(t_list, c_int))
    # Output: 8
""",
        "time_complexity": "O(N log U) where N is the total number of tasks and U is the count of distinct task types (U <= 26). Very efficient.",
        "space_complexity": "O(U) to store the heap and cooldown queue."
    },

    # =========================================================================
    # PROBLEM 23: COSINE SIMILARITY & VECTOR TOP-K RETRIEVAL FOR RAG
    # =========================================================================
    {
        "num": 23,
        "title": "Cosine Similarity Vector Top-K Retrieval from Scratch for RAG Pipelines",
        "category": "GenAI & Vector Search",
        "problem_statement": """In GenAI Retrieval-Augmented Generation (RAG) pipelines, queries must be matched against pre-indexed vector embeddings without relying on heavy third-party libraries.
Implement a vector search function `retrieve_top_k_vectors` that accepts:
- `query_vector: List[float]`
- `candidate_vectors: List[Tuple[str, List[float]]]` (id, vector)
- `k: int`
The function must compute Cosine Similarity cos(θ) = (u · v) / (||u|| ||v||) and return the top K most relevant document IDs with their similarity scores sorted in descending order.""",
        "thought_process": """1. **Cosine Similarity Definition**:
   $$sim(u, v) = Σ(u_i × v_i) / (√(Σ u_i²) × √(Σ v_i²))$$
2. **Top-K Selection via Min-Heap**:
   - Calculating similarity against $M$ candidates takes $OO(M × D) where $D$ is embedding dimension.
   - To extract top $K$ without sorting the entire candidate list ($OO(M log M)), use a Min-Heap of size $K$.
   - Push `(similarity, doc_id)` into heap. If heap size exceeds $K$, pop the minimum.
   - At completion, pop remaining $K$ elements and reverse to return in descending order ($OO(M log K)).""",
        "code": """import math
import heapq
from typing import List, Tuple

def compute_cosine_similarity(v1: List[float], v2: List[float]) -> float:
    \"\"\"Computes cosine similarity between two equal-length vectors.\"\"\"
    dot_product = 0.0
    norm_a = 0.0
    norm_b = 0.0
    
    for a, b in zip(v1, v2):
        dot_product += a * b
        norm_a += a * a
        norm_b += b * b
        
    denom = math.sqrt(norm_a) * math.sqrt(norm_b)
    if denom == 0:
        return 0.0
    return dot_product / denom

def retrieve_top_k_vectors(
    query_vector: List[float], 
    candidate_vectors: List[Tuple[str, List[float]]], 
    k: int
) -> List[Tuple[str, float]]:
    \"\"\"
    Finds top K most similar vectors using a bounded min-heap.
    \"\"\"
    if not candidate_vectors or k <= 0:
        return []
        
    # Min-heap storing: (similarity_score, doc_id)
    heap: List[Tuple[float, str]] = []
    
    for doc_id, emb in candidate_vectors:
        score = compute_cosine_similarity(query_vector, emb)
        
        if len(heap) < k:
            heapq.heappush(heap, (score, doc_id))
        else:
            if score > heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (score, doc_id))
                
    # Sort descending
    top_k = []
    while heap:
        score, doc_id = heapq.heappop(heap)
        top_k.append((doc_id, round(score, 4)))
        
    top_k.reverse()
    return top_k

# Verification
if __name__ == "__main__":
    query = [1.0, 0.0, 0.5]
    docs = [
        ("doc_spark_tuning", [0.9, 0.1, 0.4]),
        ("doc_kafka_intro",   [0.1, 0.9, 0.0]),
        ("doc_bigquery_perf", [0.8, 0.0, 0.6]),
        ("doc_hr_policy",     [-0.5, 0.8, 0.1])
    ]
    top_results = retrieve_top_k_vectors(query, docs, k=2)
    print("Top 2 Retrieved Documents:", top_results)
""",
        "time_complexity": "O(M * D + M log K) where M is the number of documents, D is embedding dimensionality, and K is the number of top items retrieved.",
        "space_complexity": "O(K) for the bounded min-heap."
    },

    # =========================================================================
    # PROBLEM 24: FIND MEDIAN FROM CONTINUOUS DATA STREAM (TWO HEAPS)
    # =========================================================================
    {
        "num": 24,
        "title": "Continuous Median from Real-Time Telemetry Stream (Two Heaps)",
        "category": "Streaming & Two Heaps",
        "problem_statement": """In data quality and latency observability, computing the median (p50) of metrics like API response times or marketplace trip fares across continuous streams is crucial. Sorting the stream on every arrival takes $OO(N log N), which is unusable in real time.
Design a class `StreamingMedianFinder` supporting:
- `add_num(num: float) -> None`: Ingests a new metric number from the stream.
- `find_median() -> float`: Returns the exact median of all numbers observed so far in $OO(1) time.""",
        "thought_process": """1. **Two Heaps Concept**:
   - Divide the numbers into two halves:
     - Lower half: stored in a **Max-Heap** `small` (storing negative values).
     - Upper half: stored in a **Min-Heap** `large`.
   - Maintain the invariant that `len(small) == len(large)` or `len(small) == len(large) + 1`.
   - Every element in `small` is <= every element in `large`.
2. **Operations**:
   - `add_num(x)`:
     - Push $x$ to `small`, then pop the maximum from `small` and push it to `large`.
     - If `len(large) > len(small)`, pop the minimum from `large` and push to `small` to balance sizes.
   - `find_median()`:
     - If total elements is odd, return `-small[0]`.
     - If total elements is even, return `(-small[0] + large[0]) / 2.0`.""",
        "code": """import heapq

class StreamingMedianFinder:
    \"\"\"
    Maintains continuous median over a streaming sequence using dual heaps in O(log N) insertion.
    \"\"\"
    def __init__(self):
        # Max-heap for lower half (stores negative values)
        self.small = []
        # Min-heap for upper half
        self.large = []

    def add_num(self, num: float) -> None:
        # Step 1: Add to small (max-heap)
        heapq.heappush(self.small, -num)
        
        # Step 2: Ensure every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
            
        # Step 3: Maintain size balance: len(small) == len(large) or len(small) == len(large) + 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        \"\"\"Returns exact median in O(1) time.\"\"\"
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

# Verification
if __name__ == "__main__":
    mf = StreamingMedianFinder()
    stream = [10.0, 20.0, 30.0, 40.0, 50.0]
    for val in stream:
        mf.add_num(val)
        print(f"Added {val} -> Current Median: {mf.find_median()}")
    # Output progresses: 10.0 -> 15.0 -> 20.0 -> 25.0 -> 30.0
""",
        "time_complexity": "add_num: O(log N) due to heap push and pop operations. find_median: O(1) strict time.",
        "space_complexity": "O(N) to store the stream elements partitioned across both heaps."
    },

    # =========================================================================
    # PROBLEM 25: MINIMUM COST TO CONNECT HETEROGENEOUS PIPELINE NETWORKS
    # =========================================================================
    {
        "num": 25,
        "title": "Minimum Cost Pipeline Network Topology (Kruskal's MST with Union-Find)",
        "category": "Graph Algorithms & Optimization",
        "problem_statement": """In multi-region enterprise data platforms, regional data clusters (e.g. AWS US-East, GCP Central, On-Premise Dell Datacenter) must be connected via dedicated cross-region network links. Each connection carries a financial latency/bandwidth cost.
Given $N$ cluster data centers and a list of available bidirectional connections `connections` where each connection is `[datacenter_u, datacenter_v, cost]`, find the minimum total cost to connect all data centers together so that data can be routed between any two centers. If it is impossible to connect all centers, return -1.""",
        "thought_process": """1. **Minimum Spanning Tree (MST)**:
   - This problem is directly modeled as finding the Minimum Spanning Tree of a weighted undirected graph.
   - Kruskal's Algorithm with Disjoint Set Union (Union-Find) is optimal:
2. **Kruskal's Algorithm**:
   - Sort all edges in ascending order of connection cost ($OO(E log E)).
   - Initialize a Disjoint Set Union (DSU) data structure with path compression and union by rank.
   - Iterate through sorted edges:
     - For edge $(u, v, \text{cost})$, check `find(u)` vs `find(v)`.
     - If they belong to different components, perform `union(u, v)`, add `cost` to total, and increment connected edges counter.
     - If they are already in the same component, skip (adding this edge would create a redundant cycle).
   - If connected edges reaches $N - 1$, return total cost. Otherwise return -1 (graph is disconnected).""",
        "code": """from typing import List

class UnionFind:
    \"\"\"Disjoint Set Union (DSU) with path compression and union by rank.\"\"\"
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False  # Already connected, would create cycle
            
        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True

def min_cost_connect_pipeline_network(n: int, connections: List[List[int]]) -> int:
    \"\"\"
    Calculates minimum cost to connect N data centers using Kruskal's MST algorithm.
    \"\"\"
    if n <= 1:
        return 0
        
    # Sort edges by cost ascending
    connections.sort(key=lambda x: x[2])
    
    uf = UnionFind(n + 1)  # 1-indexed support
    total_cost = 0
    edges_connected = 0
    
    for u, v, cost in connections:
        if uf.union(u, v):
            total_cost += cost
            edges_connected += 1
            if edges_connected == n - 1:
                return total_cost
                
    return -1  # Not all data centers could be connected

# Verification
if __name__ == "__main__":
    num_centers = 4
    # connections: [dc1, dc2, cost]
    available_links = [
        [1, 2, 3],
        [3, 4, 4],
        [1, 4, 5],
        [2, 3, 1],
        [1, 3, 7]
    ]
    min_cost = min_cost_connect_pipeline_network(num_centers, available_links)
    print("Minimum Network Connection Cost:", min_cost)
    # Output: 8 (links: [2,3,1] + [1,2,3] + [3,4,4] = 8)
""",
        "time_complexity": "O(E log E) dominated by sorting the E connections. DSU operations run in near-linear O(E * alpha(V)) time, where alpha is the inverse Ackermann function.",
        "space_complexity": "O(V) to store the DSU parent and rank arrays."
    }
]
