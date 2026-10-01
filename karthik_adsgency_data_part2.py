# -*- coding: utf-8 -*-
"""
Part 2: Top 15 DSA & Coding Questions for Karthik Ravula
Target Role: Member of Technical Staff (MTS) - Full Stack / AI Systems at AdsGency AI
Format: Problem Statement, Complete Thought Process & Intuition, Production Python 3 Code with Comments, Time & Space Complexity
"""

dsa_questions = [
    {
        "id": 1,
        "title": "Design a Distributed Sliding Window Log Rate Limiter",
        "topic": "Sliding Window / Hash Map / Queue",
        "difficulty": "Medium-Hard",
        "problem_statement": """In digital advertising platforms like AdsGency AI, external APIs (Meta Graph API, Google Ads API, TikTok API) enforce strict rate limits per account (e.g., maximum 100 requests per 60 seconds). Implement a sliding window log rate limiter class `SlidingWindowRateLimiter` that evaluates whether an incoming request from an account should be allowed or dropped in real time.

Methods to implement:
- `__init__(max_requests: int, window_seconds: int)`: Initializes the rate limiter with quota and sliding window window in seconds.
- `allow_request(account_id: str, timestamp: float) -> bool`: Returns `True` if the request at the given timestamp is within the rate limit, otherwise records nothing and returns `False`.""",
        "thought_process": """To implement an exact sliding window log rate limiter, we must track the exact timestamp of every accepted request rather than relying on discrete fixed windows, which suffer from 2x boundary spikes.

Data Structure Choice:
We can maintain a dictionary mapping `account_id` to a double-ended queue (`collections.deque`) of floating-point timestamps.

Algorithm:
1. When `allow_request(account_id, timestamp)` is called, retrieve the deque for the account.
2. Evict old timestamps: Remove all timestamps from the left of the deque where `entry_timestamp <= timestamp - window_seconds`.
3. Check capacity: If the length of the deque is strictly less than `max_requests`, the request is allowed. We append `timestamp` to the right of the deque and return `True`.
4. If the deque already has `max_requests`, the request breaches the rate limit. We do not record the timestamp and return `False`.

In a production distributed environment like Redis, this algorithm maps directly to a Redis Sorted Set (ZSET) using `ZREMRANGEBYSCORE` to evict expired items, `ZCARD` to count elements, and `ZADD` to record the new request within an atomic transaction.""",
        "code": """from collections import deque
from typing import Dict

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Maps account_id -> deque of timestamps
        self.account_logs: Dict[str, deque] = {}

    def allow_request(self, account_id: str, timestamp: float) -> bool:
        if account_id not in self.account_logs:
            self.account_logs[account_id] = deque()

        queue = self.account_logs[account_id]
        window_start = timestamp - self.window_seconds

        # Evict all timestamps outside the current sliding window
        while queue and queue[0] <= window_start:
            queue.popleft()

        # Check if current request can be accommodated
        if len(queue) < self.max_requests:
            queue.append(timestamp)
            return True
        
        # Quota exceeded; drop request
        return False
""",
        "complexity": "Time Complexity: O(k) per request where k is the number of expired timestamps evicted (amortized O(1) per request). Space Complexity: O(N * max_requests) where N is the number of unique active accounts."
    },
    {
        "id": 2,
        "title": "Multi-Agent Task Dependency Resolution & Scheduling",
        "topic": "Graph / Topological Sort / Kahn's Algorithm",
        "difficulty": "Medium",
        "problem_statement": """An autonomous ad campaign launch at AdsGency AI requires executing multiple dependent tasks across agents (e.g., Task 0: Generate Copy, Task 1: Generate Image Assets, Task 2: Assemble Creative, Task 3: Deploy to Meta). Given `num_tasks` and a list of directed dependencies `dependencies` where `[a, b]` means Task `a` depends on Task `b` (Task `b` must complete before Task `a` can start), return a valid execution order for the agents. If a circular dependency exists (e.g., Task 0 needs Task 1, and Task 1 needs Task 0), return an empty list `[]`.""",
        "thought_process": """This problem models task scheduling in a workflow orchestrator like LangGraph or Airflow and can be solved using Topological Sort on a Directed Acyclic Graph (DAG).

We can apply Kahn's Algorithm (BFS-based Topological Sort):
1. Build an adjacency list `graph` where `b -> a` (since `b` must precede `a`).
2. Track the in-degree of each task (number of prerequisite tasks that must finish before this task can execute).
3. Initialize a queue with all tasks having `in_degree == 0` (tasks with zero prerequisites that can execute immediately).
4. While the queue is non-empty, dequeue a task, append it to our `execution_order`, and decrement the in-degree of all its downstream dependent neighbors.
5. If a neighbor's in-degree drops to 0, push it to the queue.
6. Once the queue is empty, check if `len(execution_order) == num_tasks`. If true, we found a valid schedule. If false, a cycle exists, and scheduling is impossible.""",
        "code": """from collections import deque
from typing import List

class AgentTaskScheduler:
    def find_execution_order(self, num_tasks: int, dependencies: List[List[int]]) -> List[int]:
        # Adjacency list: prereq -> list of dependent tasks
        graph = {i: [] for i in range(num_tasks)}
        in_degree = [0] * num_tasks

        for task, prereq in dependencies:
            graph[prereq].append(task)
            in_degree[task] += 1

        # Tasks with 0 prerequisites can execute immediately
        queue = deque([i for i in range(num_tasks) if in_degree[i] == 0])
        execution_order = []

        while queue:
            curr = queue.popleft()
            execution_order.append(curr)

            for neighbor in graph[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # If order contains all tasks, no cycle exists
        return execution_order if len(execution_order) == num_tasks else []
""",
        "complexity": "Time Complexity: O(V + E) where V = num_tasks and E = len(dependencies), as each task and edge is visited once. Space Complexity: O(V + E) to store the adjacency graph and in-degree array."
    },
    {
        "id": 3,
        "title": "Design In-Memory LRU Cache with Time-To-Live (TTL)",
        "topic": "Hash Map + Doubly Linked List",
        "difficulty": "Hard",
        "problem_statement": """AdsGency AI caches external ad campaign statistics and semantic embeddings in memory. Implement an LRU (Least Recently Used) cache with Time-To-Live (TTL) expiration.

Implement the `LRUCacheWithTTL` class:
- `__init__(capacity: int)`: Initializes the LRU cache with positive size capacity.
- `get(key: str, current_time: float) -> int`: Returns the value of the key if it exists and has not expired (`current_time < expiry_time`). Otherwise, removes the key and returns -1. Accessing a valid key marks it as most recently used.
- `put(key: str, value: int, ttl: float, current_time: float) -> None`: Sets or inserts the key with value and expiry timestamp (`current_time + ttl`). If capacity is exceeded, evicts the least recently used unexpired key.""",
        "thought_process": """A standard LRU cache uses a Hash Map combined with a Doubly Linked List to achieve O(1) reads, updates, and evictions.

To support TTL expiration:
1. Each node in the doubly linked list stores `key`, `value`, and `expires_at = current_time + ttl`.
2. Hash Map maps `key -> Node`.
3. In `get(key, current_time)`:
   - If `key` is not in map, return -1.
   - If `node.expires_at <= current_time`, the item has expired. We delete it from the linked list and hash map and return -1.
   - If valid, we move the node to the head of the doubly linked list (most recently used) and return its value.
4. In `put(key, value, ttl, current_time)`:
   - If `key` already exists, update its value and expiry, and move it to the head.
   - If new key and cache is at capacity, remove the tail node (least recently used) from both the linked list and hash map.
   - Insert the new node at the head.""",
        "code": """from typing import Optional, Dict

class Node:
    def __init__(self, key: str, value: int, expires_at: float):
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCacheWithTTL:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[str, Node] = {}
        # Sentinel dummy nodes
        self.head = Node("", 0, float('inf'))
        self.tail = Node("", 0, float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str, current_time: float) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        # Check expiration
        if current_time >= node.expires_at:
            self._remove(node)
            del self.cache[key]
            return -1

        # Move accessed node to head (most recently used)
        self._remove(node)
        self._add_to_head(node)
        return node.value

    def put(self, key: str, value: int, ttl: float, current_time: float) -> None:
        expires_at = current_time + ttl

        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            node.expires_at = expires_at
            self._add_to_head(node)
            return

        if len(self.cache) >= self.capacity:
            # Evict LRU node from tail
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

        new_node = Node(key, value, expires_at)
        self._add_to_head(new_node)
        self.cache[key] = new_node
""",
        "complexity": "Time Complexity: O(1) for both get and put operations. Space Complexity: O(capacity) to store nodes and hash map entries."
    },
    {
        "id": 4,
        "title": "Optimal Ad Campaign Budget Allocation (Knapsack DP)",
        "topic": "Dynamic Programming / 0-1 Knapsack",
        "difficulty": "Medium",
        "problem_statement": """AdsGency AI is given a total client daily advertising budget `total_budget` (in dollars). A set of candidate ad campaigns is available, each with a required cost `costs[i]` and an estimated conversion return value `returns[i]`. Each campaign can be either fully funded once or skipped. Determine the maximum expected conversion return that can be achieved without exceeding `total_budget`.""",
        "thought_process": """This problem is a classic 0/1 Knapsack optimization problem.

State Representation:
Let `dp[b]` represent the maximum conversion return achievable using a budget of exactly or at most `b`.

Base Case:
`dp[b] = 0` for all `0 <= b <= total_budget`.

Transitions:
For each campaign `i` with cost `c = costs[i]` and return `r = returns[i]`:
We iterate backwards from `total_budget` down to `c`:
`dp[b] = max(dp[b], dp[b - c] + r)`
Iterating backwards ensures that each campaign is used at most once (avoiding unbounded knapsack behavior).

After evaluating all campaigns, `dp[total_budget]` contains the maximum possible return.""",
        "code": """from typing import List

class CampaignBudgetOptimizer:
    def max_conversion_return(self, total_budget: int, costs: List[int], returns: List[int]) -> int:
        n = len(costs)
        # dp[b] stores max return achievable with budget b
        dp = [0] * (total_budget + 1)

        for i in range(n):
            c = costs[i]
            r = returns[i]
            # Iterate backwards to ensure 0/1 constraint
            for b in range(total_budget, c - 1, -1):
                dp[b] = max(dp[b], dp[b - c] + r)

        return dp[total_budget]
""",
        "complexity": "Time Complexity: O(N * total_budget) where N is the number of candidate campaigns. Space Complexity: O(total_budget) using a 1D space-optimized dynamic programming array."
    },
    {
        "id": 5,
        "title": "Ad Keyword Autocomplete & Prefix Search (Trie)",
        "topic": "Trie / Tree / Prefix Search",
        "difficulty": "Medium",
        "problem_statement": """AdsGency AI provides a search bar where marketing operators type ad keywords to see autocomplete recommendations. Implement a Trie-based autocomplete system `KeywordTrie` that stores ad keywords along with their search popularity frequencies.

Methods:
- `insert(word: str, frequency: int) -> None`: Inserts a keyword and its historical search volume.
- `search_prefix(prefix: str) -> List[str]`: Returns up to the top 3 highest-frequency keywords starting with `prefix`. If frequencies tie, sort lexicographically.""",
        "thought_process": """A Trie (Prefix Tree) is the optimal structure for prefix-based search and autocomplete queries.

Node Design:
Each `TrieNode` contains:
- `children`: Dict mapping char -> TrieNode
- `top_words`: A cached list of the top words passing through or ending at this prefix node, sorted by `(-frequency, word)`.

Algorithm:
1. When inserting `(word, frequency)`, traverse the Trie character by character.
2. At each node along the path (including root), maintain the top candidate keywords. We can update the list of candidates, sort by `(-freq, word)`, and slice the top 3.
3. In `search_prefix(prefix)`, traverse down to the node corresponding to the last character of `prefix`. If any character is missing, return `[]`.
4. If found, return the pre-computed `top_words` in O(1) time relative to the prefix length.""",
        "code": """from typing import List, Dict

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        # Stores tuples of (-frequency, word) for top suggestions
        self.top_suggestions: List[tuple] = []

class KeywordTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, frequency: int) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
            # Update suggestions at current prefix
            node.top_suggestions = [item for item in node.top_suggestions if item[1] != word]
            node.top_suggestions.append((-frequency, word))
            node.top_suggestions.sort()
            if len(node.top_suggestions) > 3:
                node.top_suggestions.pop()

    def search_prefix(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return [word for _, word in node.top_suggestions]
""",
        "complexity": "Time Complexity: Insert is O(L * K log K) where L is keyword length and K = 3. Search is O(P) where P is prefix length. Space Complexity: O(N * L) where N is number of words and L is average word length."
    },
    {
        "id": 6,
        "title": "Real-Time Event Stream Deduplication",
        "topic": "Sliding Window / Hash Set / Deque",
        "difficulty": "Medium",
        "problem_statement": """AdsGency AI consumes conversion webhooks from Meta, Google, and TikTok. Due to network retries, duplicate events frequently arrive within a 10-minute sliding window. Given a stream of events `(event_id, timestamp)` arriving in chronological order, implement `EventDeduplicator` that filters out duplicate events within a 600-second window while keeping memory bounded.""",
        "thought_process": """To deduplicate streaming events with a time window constraint:
1. We maintain a Hash Set `seen_ids` for O(1) membership lookup.
2. We maintain a double-ended queue `event_queue` storing `(event_id, timestamp)` in chronological order.
3. For each incoming event `(event_id, timestamp)`:
   - Evict expired events: While `event_queue` is non-empty and `event_queue[0][1] <= timestamp - 600`, pop the oldest event `(old_id, old_time)` and remove `old_id` from `seen_ids`.
   - Check duplication: If `event_id` is in `seen_ids`, it is a duplicate—drop it and return `False`.
   - Otherwise, add `event_id` to `seen_ids`, append `(event_id, timestamp)` to `event_queue`, and return `True`.""",
        "code": """from collections import deque
from typing import Set, Tuple

class EventDeduplicator:
    def __init__(self, window_seconds: int = 600):
        self.window_seconds = window_seconds
        self.seen_ids: Set[str] = set()
        self.event_queue: deque[Tuple[str, float]] = deque()

    def process_event(self, event_id: str, timestamp: float) -> bool:
        # Evict events older than window_seconds
        cutoff = timestamp - self.window_seconds
        while self.event_queue and self.event_queue[0][1] <= cutoff:
            old_id, _ = self.event_queue.popleft()
            self.seen_ids.discard(old_id)

        # Check for duplicate
        if event_id in self.seen_ids:
            return False

        # Register new unique event
        self.seen_ids.add(event_id)
        self.event_queue.append((event_id, timestamp))
        return True
""",
        "complexity": "Time Complexity: Amortized O(1) per incoming event. Space Complexity: O(W) where W is the number of events received within the 10-minute window."
    },
    {
        "id": 7,
        "title": "Priority Queue for Multi-Platform Ad Bidding",
        "topic": "Heap / Priority Queue",
        "difficulty": "Medium",
        "problem_statement": """AdsGency AI manages real-time bids across multiple ad auctions. Each bid has an `auction_id`, a `bid_amount`, and an `expected_ctr`. The composite priority score of a bid is defined as `score = bid_amount * expected_ctr`. Implement `AdBidAuctionManager` to maintain the top-k highest priority bids across streaming updates.""",
        "thought_process": """To maintain the top-k highest scoring items from a continuous stream:
A Min-Heap of fixed size `k` is the optimal choice.

Algorithm:
1. Store elements in the min-heap as `(score, auction_id, bid_amount)`.
2. When a new bid arrives:
   - Calculate its score: `score = bid_amount * expected_ctr`.
   - If the heap has fewer than `k` items, push the bid.
   - If the heap has `k` items and the new bid's score is strictly greater than the heap root (the smallest score among current top-k), pop the root and push the new bid.
3. To retrieve current top bids, extract and sort the elements descending.""",
        "code": """import heapq
from typing import List, Tuple

class AdBidAuctionManager:
    def __init__(self, k: int):
        self.k = k
        # Min-heap storing tuples of (score, auction_id, bid_amount)
        self.min_heap: List[Tuple[float, str, float]] = []

    def submit_bid(self, auction_id: str, bid_amount: float, expected_ctr: float) -> None:
        score = round(bid_amount * expected_ctr, 4)

        if len(self.min_heap) < self.k:
            heapq.heappush(self.min_heap, (score, auction_id, bid_amount))
        elif score > self.min_heap[0][0]:
            heapq.heapreplace(self.min_heap, (score, auction_id, bid_amount))

    def get_top_bids(self) -> List[Tuple[str, float, float]]:
        # Return sorted descending by score
        return [(item[1], item[2], item[0]) for item in sorted(self.min_heap, reverse=True)]
""",
        "complexity": "Time Complexity: O(log k) for each bid submission. O(k log k) to inspect top bids. Space Complexity: O(k) for the bounded heap."
    },
    {
        "id": 8,
        "title": "Merge Overlapping Campaign Flight Schedules",
        "topic": "Intervals / Sorting",
        "difficulty": "Medium",
        "problem_statement": """Multiple ad sets run during specified start and end dates (intervals). Given an array of intervals `schedules` where `schedules[i] = [start_i, end_i]`, merge all overlapping campaign schedules and return an array of the non-overlapping intervals that cover all the schedules in the input.""",
        "thought_process": """This is the classic Merge Intervals problem, essential for calculating continuous active campaign flight dates.

Algorithm:
1. If the input list is empty or has 1 interval, return it immediately.
2. Sort the intervals based on their start times: `schedules.sort(key=lambda x: x[0])`.
3. Initialize an empty list `merged` and append the first interval.
4. Iterate through the remaining intervals `curr`:
   - Let `last = merged[-1]`.
   - If `curr[0] <= last[1]`, the intervals overlap. Update `last[1] = max(last[1], curr[1])`.
   - Otherwise, there is no overlap; append `curr` to `merged`.
5. Return `merged`.""",
        "code": """from typing import List

class CampaignScheduleMerger:
    def merge_schedules(self, schedules: List[List[int]]) -> List[List[int]]:
        if not schedules:
            return []

        # Sort by interval start time
        schedules.sort(key=lambda x: x[0])
        merged = [schedules[0]]

        for curr in schedules[1:]:
            last = merged[-1]
            # Overlap detected
            if curr[0] <= last[1]:
                last[1] = max(last[1], curr[1])
            else:
                merged.append(curr)

        return merged
""",
        "complexity": "Time Complexity: O(N log N) dominated by sorting the intervals. Space Complexity: O(N) to store the merged result."
    },
    {
        "id": 9,
        "title": "Detect Circular Delegation Loops in Multi-Agent Workflows",
        "topic": "Graph / DFS / Cycle Detection",
        "difficulty": "Medium",
        "problem_statement": """In AdsGency's multi-agent system, an agent can delegate sub-tasks to other agents. Given an integer `num_agents` (labeled `0` to `num_agents - 1`) and a list of directed delegation pairs `delegations` where `[u, v]` represents Agent `u` delegating to Agent `v`, determine whether the delegation network contains any circular deadlocks (cycles). Return `True` if a cycle exists, and `False` otherwise.""",
        "thought_process": """To detect a cycle in a directed graph, we can use Depth First Search (DFS) with a 3-color state tracking approach:
- State 0 (WHITE / Unvisited): Node has not been visited yet.
- State 1 (GRAY / Visiting): Node is currently in the active DFS recursion stack.
- State 2 (BLACK / Visited): Node and all its descendants have been completely processed.

Algorithm:
1. Build an adjacency list `graph`.
2. Maintain a `visited` array initialized to 0 for all nodes.
3. For each node from `0` to `num_agents - 1`:
   - If the node is in State 0, run DFS.
   - If DFS encounters a node in State 1 (currently in the active recursion call stack), a back-edge is found, meaning a cycle exists! Return `True`.
4. If all nodes reach State 2 without encountering a back-edge, return `False`.""",
        "code": """from typing import List

class MultiAgentDeadlockDetector:
    def has_circular_delegation(self, num_agents: int, delegations: List[List[int]]) -> bool:
        graph = {i: [] for i in range(num_agents)}
        for u, v in delegations:
            graph[u].append(v)

        # 0 = Unvisited, 1 = Visiting (in current path), 2 = Completely Visited
        state = [0] * num_agents

        def dfs(node: int) -> bool:
            state[node] = 1  # Mark visiting

            for neighbor in graph[node]:
                if state[neighbor] == 1:
                    return True  # Cycle detected
                if state[neighbor] == 0:
                    if dfs(neighbor):
                        return True

            state[node] = 2  # Mark completely processed
            return False

        for agent in range(num_agents):
            if state[agent] == 0:
                if dfs(agent):
                    return True

        return False
""",
        "complexity": "Time Complexity: O(V + E) where V = num_agents and E = len(delegations). Space Complexity: O(V + E) for graph storage and recursion call stack."
    },
    {
        "id": 10,
        "title": "Longest Substring Without Repeating Keywords",
        "topic": "Sliding Window / Two Pointers / Hash Map",
        "difficulty": "Medium",
        "problem_statement": """AdsGency AI generates comma-separated ad headline tags. Given a string `tags` containing characters, find the length of the longest contiguous substring without any repeating characters to maximize headline variety.""",
        "thought_process": """We use a dynamic sliding window with two pointers (`left` and `right`) and a Hash Map `last_seen` that tracks the most recent index of each character.

Algorithm:
1. Initialize `max_len = 0` and `left = 0`.
2. Iterate `right` from 0 to `len(tags) - 1`:
   - Let `char = tags[right]`.
   - If `char` is in `last_seen` and its last seen index is `>= left`, advance `left` to `last_seen[char] + 1` to exclude the duplicate.
   - Update `last_seen[char] = right`.
   - Update `max_len = max(max_len, right - left + 1)`.
3. Return `max_len`.""",
        "code": """class HeadlineVarietyFinder:
    def length_of_longest_unique_substring(self, s: str) -> int:
        last_seen = {}
        max_len = 0
        left = 0

        for right, char in enumerate(s):
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            max_len = max(max_len, right - left + 1)

        return max_len
""",
        "complexity": "Time Complexity: O(N) where N is string length, as both pointers traverse at most N steps. Space Complexity: O(min(N, M)) where M is the character alphabet size."
    },
    {
        "id": 11,
        "title": "Design In-Memory Key-Value Store with TTL & Transactions",
        "topic": "Design / Stack / Hash Map",
        "difficulty": "Hard",
        "problem_statement": """Implement an in-memory transactional key-value store `TransactionalKV` supporting `get`, `set`, `delete`, and transaction commands `begin`, `commit`, and `rollback`. Transactions can be nested. If a transaction is rolled back, all mutations made within it must be reverted.""",
        "thought_process": """To support nested transactions with rollback:
1. We maintain a primary database dictionary `store`.
2. We maintain a stack of transaction contexts `transaction_stack = []`.
3. When `begin()` is called, push an empty dictionary representing the delta/undo log for that transaction level.
4. When `set(key, value)` or `delete(key)` is called:
   - If inside a transaction (`transaction_stack` is non-empty), record the previous state of `key` in the top transaction's undo log (if not already recorded).
   - Apply the mutation to `store`.
5. When `rollback()` is called:
   - Pop the top transaction from the stack.
   - For every key in the undo log, restore its previous value in `store`.
6. When `commit()` is called:
   - Pop the top transaction. If there is an outer parent transaction, merge the undo log into the parent. If it was the outermost transaction, changes become permanent.""",
        "code": """from typing import Optional, Dict, List

class TransactionalKV:
    def __init__(self):
        self.store: Dict[str, str] = {}
        # Stack of undo logs: maps key -> previous_value (None if key was absent)
        self.transaction_stack: List[Dict[str, Optional[str]]] = []

    def get(self, key: str) -> Optional[str]:
        return self.store.get(key, None)

    def set(self, key: str, value: str) -> None:
        if self.transaction_stack:
            # Record original value before mutation if not yet recorded in current tx
            undo_log = self.transaction_stack[-1]
            if key not in undo_log:
                undo_log[key] = self.store.get(key, None)
        self.store[key] = value

    def delete(self, key: str) -> None:
        if self.transaction_stack:
            undo_log = self.transaction_stack[-1]
            if key not in undo_log:
                undo_log[key] = self.store.get(key, None)
        self.store.pop(key, None)

    def begin(self) -> None:
        self.transaction_stack.append({})

    def commit(self) -> bool:
        if not self.transaction_stack:
            return False
        committed_undo = self.transaction_stack.pop()
        # If nested, merge into parent transaction
        if self.transaction_stack:
            parent_undo = self.transaction_stack[-1]
            for key, val in committed_undo.items():
                if key not in parent_undo:
                    parent_undo[key] = val
        return True

    def rollback(self) -> bool:
        if not self.transaction_stack:
            return False
        undo_log = self.transaction_stack.pop()
        for key, prev_val in undo_log.items():
            if prev_val is None:
                self.store.pop(key, None)
            else:
                self.store[key] = prev_val
        return True
""",
        "complexity": "Time Complexity: O(1) for get, set, delete, and begin. O(K) for commit and rollback where K is the number of keys mutated in the transaction. Space Complexity: O(N + K) where N is total keys and K is uncommitted mutations."
    },
    {
        "id": 12,
        "title": "Top-K Frequent Ad Search Queries in Streaming Window",
        "topic": "Hash Map + Min-Heap",
        "difficulty": "Medium",
        "problem_statement": """Given a list of ad search keyword queries `queries` and an integer `k`, return the `k` most frequent queries. If two queries have the same frequency, the one with lower alphabetical order should come first.""",
        "thought_process": """1. Count the frequency of each search query using `collections.Counter`.
2. We need the top `k` elements based on `(frequency DESC, query ASC)`.
3. To achieve O(N log K) time complexity, we can use a Min-Heap of size `k`.
   - In Python, we define a wrapper class or tuple. For a min-heap, we want lower frequency to be popped first, and higher alphabetical string to be popped first in tie-breaks.
   - So we store `(freq, ReverseString(query))` or sort the frequencies directly using `heapq.nsmallest` / `heapq.nlargest`.
4. Alternatively, use Python's `heapq` with custom comparison or sort all unique keys by `(-freq, query)` and slice `[:k]`.""",
        "code": """from collections import Counter
import heapq
from typing import List

class FrequencyQueryItem:
    def __init__(self, query: str, freq: int):
        self.query = query
        self.freq = freq

    def __lt__(self, other: 'FrequencyQueryItem') -> bool:
        # Min-heap criteria: smaller freq first; if tie, lexicographically larger query first
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.query > other.query

class TopKQueryTracker:
    def top_k_queries(self, queries: List[str], k: int) -> List[str]:
        counts = Counter(queries)
        min_heap = []

        for query, freq in counts.items():
            item = FrequencyQueryItem(query, freq)
            heapq.heappush(min_heap, item)
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        # Extract items and sort descending by priority
        result = []
        while min_heap:
            result.append(heapq.heappop(min_heap))
        
        result.sort(key=lambda x: (-x.freq, x.query))
        return [x.query for x in result]
""",
        "complexity": "Time Complexity: O(N + U log K) where N is len(queries) and U is unique queries count. Space Complexity: O(U) for the frequency map and O(k) for the heap."
    },
    {
        "id": 13,
        "title": "Subarray Spend Sum Equals Target Budget",
        "topic": "Prefix Sums + Hash Map",
        "difficulty": "Medium",
        "problem_statement": """Given an array of integers `daily_spends` representing daily marketing costs and an integer `target_budget`, return the total number of continuous sub-periods (subarrays) where the cumulative ad spend equals exactly `target_budget`.""",
        "thought_process": """A brute-force solution checks all O(N^2) subarrays.
We can optimize this to O(N) using Prefix Sums and a Hash Map:

Let `prefix_sum[i]` be the cumulative sum from index 0 to `i`.
A subarray from `j + 1` to `i` has sum:
`sum(j+1...i) = prefix_sum[i] - prefix_sum[j]`
We want this to equal `target_budget`:
`prefix_sum[i] - prefix_sum[j] = target_budget`
Rearranging:
`prefix_sum[j] = prefix_sum[i] - target_budget`

Algorithm:
1. Maintain `running_sum = 0` and a hash map `prefix_counts` initialized with `{0: 1}` (representing an empty subarray).
2. For each value in `daily_spends`:
   - `running_sum += val`
   - If `(running_sum - target_budget)` exists in `prefix_counts`, add its frequency to `count`.
   - Increment `prefix_counts[running_sum]`.
3. Return `count`.""",
        "code": """from collections import defaultdict
from typing import List

class BudgetPacingAuditor:
    def count_target_spend_subarrays(self, daily_spends: List[int], target_budget: int) -> int:
        prefix_counts = defaultdict(int)
        prefix_counts[0] = 1  # Base case for subarray starting at index 0

        running_sum = 0
        total_subarrays = 0

        for spend in daily_spends:
            running_sum += spend
            complement = running_sum - target_budget
            if complement in prefix_counts:
                total_subarrays += prefix_counts[complement]
            prefix_counts[running_sum] += 1

        return total_subarrays
""",
        "complexity": "Time Complexity: O(N) single pass through the array. Space Complexity: O(N) to store prefix sum frequencies."
    },
    {
        "id": 14,
        "title": "Lowest Common Ancestor in Ad Taxonomy Category Tree",
        "topic": "Binary Tree / Tree Traversal",
        "difficulty": "Medium",
        "problem_statement": """AdsGency AI organizes ad verticals into a hierarchical taxonomy tree. Given the root of a binary taxonomy tree and two category nodes `p` and `q`, find the lowest common ancestor (LCA) node of `p` and `q`.""",
        "thought_process": """The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself).

Recursive Approach:
1. Base cases:
   - If `root` is `None`, return `None`.
   - If `root == p` or `root == q`, return `root`.
2. Recursively search left and right subtrees:
   - `left = lowestCommonAncestor(root.left, p, q)`
   - `right = lowestCommonAncestor(root.right, p, q)`
3. If both `left` and `right` return non-null, `p` and `q` reside in separate branches, so current `root` is their LCA!
4. If only one of `left` or `right` is non-null, return that non-null node.""",
        "code": """class TreeNode:
    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None

class AdTaxonomyNavigator:
    def lowest_common_ancestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q:
            return root

        left = self.lowest_common_ancestor(root.left, p, q)
        right = self.lowest_common_ancestor(root.right, p, q)

        # If p and q found in separate branches, root is LCA
        if left and right:
            return root

        # Otherwise return whichever side found a match
        return left if left else right
""",
        "complexity": "Time Complexity: O(N) where N is number of nodes in tree. Space Complexity: O(H) where H is tree height for recursion stack."
    },
    {
        "id": 15,
        "title": "Median of Real-Time Ad Click Latencies from Stream",
        "topic": "Two Heaps / Heap",
        "difficulty": "Hard",
        "problem_statement": """AdsGency AI monitors real-time ad click response latencies in milliseconds. Implement a data structure `MedianStreamFinder` that calculates the median latency dynamically in O(1) time as new latencies arrive.

Methods:
- `add_latency(val: int) -> None`: Adds a latency value from the streaming pipeline.
- `find_median() -> float`: Returns the median of all recorded latencies.""",
        "thought_process": """To compute the median dynamically in O(1) time:
We partition the stream into two halves using two heaps:
1. Max-Heap (`small`): Stores the smaller half of numbers. Root contains the maximum of the smaller half.
2. Min-Heap (`large`): Stores the larger half of numbers. Root contains the minimum of the larger half.

Balancing Invariants:
1. Every element in `small` must be <= every element in `large`.
2. `len(small)` must be either equal to `len(large)` (even count) or `len(large) + 1` (odd count).

Algorithm:
- When adding `val`:
  - Push to `small` (negated because Python heapq is min-heap).
  - Pop max from `small` and push to `large` to enforce invariant 1.
  - If `len(large) > len(small)`, pop min from `large` and push to `small` to enforce invariant 2.
- Finding median:
  - If odd total elements (`len(small) > len(large)`), median is `-small[0]`.
  - If even total elements, median is `(-small[0] + large[0]) / 2.0`.""",
        "code": """import heapq

class MedianStreamFinder:
    def __init__(self):
        # Max-heap for lower half (negated values)
        self.small = []
        # Min-heap for upper half
        self.large = []

    def add_latency(self, val: int) -> None:
        # Push to small max-heap
        heapq.heappush(self.small, -val)

        # Balance invariant 1: max of small <= min of large
        max_small = -heapq.heappop(self.small)
        heapq.heappush(self.large, max_small)

        # Balance invariant 2: len(small) >= len(large)
        if len(self.large) > len(self.small):
            min_large = heapq.heappop(self.large)
            heapq.heappush(self.small, -min_large)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
""",
        "complexity": "Time Complexity: O(log N) for add_latency; O(1) for find_median. Space Complexity: O(N) to store stream latencies in the two heaps."
    }
]
