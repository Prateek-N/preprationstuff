# -*- coding: utf-8 -*-
"""
Amazon Advertising in Live Events - AI Engineer Preparation
Part 1: Top 30 High-Frequency Amazon DSA Practice Questions in Python
Candidate: Ashutosh Rudraksh
"""

dsa_questions = [
    # Q1: LRU Cache with TTL
    {
        "id": 1,
        "title": "Design In-Memory LRU Cache with Time-To-Live (TTL)",
        "topic": "Hash Map + Doubly Linked List",
        "difficulty": "Medium-Hard",
        "problem_statement": """Design and implement a data structure for a Least Recently Used (LRU) Cache that supports a Time-To-Live (TTL) expiration mechanism for each key-value pair.
The cache must support the following operations:
- `get(key: str) -> int`: Returns the value of the key if it exists and has not expired. If the key does not exist or has expired, return -1. Accessing a non-expired key marks it as most recently used.
- `put(key: str, value: int, ttl_ms: int) -> None`: Inserts or updates the key with the given value and time-to-live in milliseconds. If inserting exceeds the capacity, evict the least recently used non-expired key. If all non-expired keys exceed capacity, evict the LRU key regardless.
- `clean_expired() -> None`: Optional maintenance routine to purge expired keys.
Both `get` and `put` operations must run in O(1) average time complexity.""",
        "thought_process": """To achieve O(1) get and put operations while maintaining LRU ordering, the standard approach combines a hash table with a doubly linked list. The hash table maps each key to its corresponding Node in the linked list, allowing O(1) key lookups. The doubly linked list maintains the temporal access order: the head represents the most recently accessed node, while the tail represents the least recently accessed node.

To incorporate TTL (Time-To-Live), each node stores an absolute expiration timestamp (`expire_at = current_time + ttl_ms`). When `get(key)` is invoked, we first check if the key exists in our hash map. If present, we compare its expiration timestamp with the current time. If it has expired, we remove the node from both the hash map and the linked list, returning -1. If valid, we move the node to the head of the doubly linked list and return its value.

For `put(key, value, ttl_ms)`, if the key already exists, we update its value and new expiration timestamp, then move it to the head. If it is a new key and the cache has reached maximum capacity, we evict the node at the tail (the least recently used item). We also maintain dummy head and tail sentinel nodes in the doubly linked list to eliminate edge cases during pointer manipulations.""",
        "code": """import time
from typing import Optional, Dict

class Node:
    def __init__(self, key: str = "", val: int = 0, expire_at: float = 0.0):
        # Store key, value, and expiration timestamp
        self.key = key
        self.val = val
        self.expire_at = expire_at
        # Pointers for doubly linked list
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCacheWithTTL:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Hash map mapping key -> Node
        self.lookup: Dict[str, Node] = {}
        # Sentinel dummy nodes for O(1) insertions and removals
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        # Detach node from current linked list position
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node: Node) -> None:
        # Insert node right after the dummy head (most recently used)
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str) -> int:
        if key not in self.lookup:
            return -1
        
        node = self.lookup[key]
        now = time.time()
        
        # Check if the entry has expired
        if now > node.expire_at:
            # Clean up expired node from both map and linked list
            self._remove(node)
            del self.lookup[key]
            return -1
        
        # Move accessed node to front (mark as most recently used)
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: str, value: int, ttl_ms: int) -> None:
        now = time.time()
        expire_at = now + (ttl_ms / 1000.0)
        
        if key in self.lookup:
            # Update existing node
            node = self.lookup[key]
            node.val = value
            node.expire_at = expire_at
            self._remove(node)
            self._add_to_front(node)
        else:
            # If at capacity, evict least recently used (node before tail)
            if len(self.lookup) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.lookup[lru.key]
            
            # Create and insert new node
            new_node = Node(key, value, expire_at)
            self.lookup[key] = new_node
            self._add_to_front(new_node)
""",
        "complexity": """- **Time Complexity:** O(1) average for both `get` and `put`. Node lookups in the hash map take O(1) time, and pointer adjustments in the doubly linked list take O(1) time.
- **Space Complexity:** O(C) where C is the maximum cache capacity. We store at most C key-node mappings in the dictionary and C nodes in the doubly linked list."""
    },

    # Q2: Sliding Window Maximum
    {
        "id": 2,
        "title": "Sliding Window Maximum / Real-Time Ad Telemetry Spikes",
        "topic": "Monotonic Deque",
        "difficulty": "Hard",
        "problem_statement": """You are monitoring an event stream of viewer request metrics during a live broadcast (e.g., Thursday Night Football ad impression bids per second). You are given an array of integers `nums` representing the incoming stream metrics, and an integer `k` representing the sliding window duration in seconds.
Return the maximum metric observed in each sliding window of size `k` as the window moves from left to right across the stream.
You must solve the problem in O(N) time complexity.""",
        "thought_process": """A naive brute-force search looks at all k elements in each window, leading to O(N * k) time, which will breach real-time streaming constraints when k is large. A max-heap achieves O(N log k) time by tracking elements with their indices, but evicting stale elements outside the window requires heap maintenance.

To achieve optimal O(N) time, we use a Monotonic Deque (double-ended queue). The deque will store the indices of the array elements such that the values corresponding to these indices are in strictly descending order:
1. Stale Index Removal: Before inserting the current element at index `i`, we pop indices from the front of the deque if they fall outside the current window (`index <= i - k`).
2. Monotonic Property Maintenance: We pop indices from the back of the deque as long as their corresponding values are less than or equal to `nums[i]`. This is because `nums[i]` is both newer and larger than those elements, meaning those smaller elements can never be the maximum of any future window.
3. Front Element is Maximum: After pushing `i` to the back, the index at the front of the deque will always point to the maximum element in the current window once `i >= k - 1`.""",
        "code": """from collections import deque
from typing import List

def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    # Monotonic deque storing indices of candidate maximums
    dq = deque()
    result = []
    
    for i, num in enumerate(nums):
        # Step 1: Remove indices that are out of the current sliding window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # Step 2: Maintain descending order in deque
        # Pop elements from back that are smaller than current element
        while dq and nums[dq[-1]] <= num:
            dq.pop()
            
        # Step 3: Add current element index to the deque
        dq.append(i)
        
        # Step 4: Record current window max once window reaches size k
        if i >= k - 1:
            result.append(nums[dq[0]])
            
    return result
""",
        "complexity": """- **Time Complexity:** O(N), where N is the length of `nums`. Each index is pushed onto the deque exactly once and popped from either the front or back at most once.
- **Space Complexity:** O(k) auxiliary space for the deque, which stores at most k indices at any given moment."""
    },

    # Q3: Merge K Sorted Streams
    {
        "id": 3,
        "title": "Merge K Sorted Event Streams / Impression Log Aggregator",
        "topic": "Min-Heap / Priority Queue",
        "difficulty": "Hard",
        "problem_statement": """You are given an array of `k` sorted lists of event logs, where each log is represented by a timestamp and payload `(timestamp: int, event_id: str)`. Each individual stream is sorted in ascending order of timestamp.
Merge all `k` sorted streams into one unified sorted event stream and return it.
Ensure the solution scales efficiently when `k` is large (e.g., thousands of distributed partition workers).""",
        "thought_process": """When merging multiple sorted streams, comparing all k heads sequentially takes O(k) per element, leading to O(N * k) total time where N is the total number of events across all streams.

Instead, we use a Min-Heap (Priority Queue) of size k:
1. Initialization: We push the first element of each non-empty stream into the min-heap. The heap stores tuples of `(timestamp, stream_index, element_index)`.
2. Extract Minimum: In each step, we extract the root of the min-heap, which is guaranteed to be the smallest timestamp across all current stream heads. We append its event to our output stream.
3. Advance Stream: We advance the pointer in the stream from which the minimum was extracted. If that stream has more elements, we push its next element into the min-heap.
4. Termination: We repeat this process until the heap is empty. This guarantees that at any point, the heap holds at most k elements, giving an extraction and insertion cost of O(log k).""",
        "code": """import heapq
from typing import List, Tuple

def merge_k_sorted_streams(streams: List[List[Tuple[int, str]]]) -> List[Tuple[int, str]]:
    # Min-heap to track the smallest current element across k streams
    # Heap stores: (timestamp, stream_idx, elem_idx, payload)
    min_heap = []
    
    # Initialize heap with the first element from each non-empty stream
    for stream_idx, stream in enumerate(streams):
        if stream:
            timestamp, payload = stream[0]
            # Use stream_idx to break ties deterministically without comparing payloads
            heapq.heappush(min_heap, (timestamp, stream_idx, 0, payload))
            
    merged_results = []
    
    # Process elements in order of timestamp
    while min_heap:
        timestamp, stream_idx, elem_idx, payload = heapq.heappop(min_heap)
        merged_results.append((timestamp, payload))
        
        # If the stream has a next element, push it into the heap
        next_elem_idx = elem_idx + 1
        if next_elem_idx < len(streams[stream_idx]):
            next_timestamp, next_payload = streams[stream_idx][next_elem_idx]
            heapq.heappush(min_heap, (next_timestamp, stream_idx, next_elem_idx, next_payload))
            
    return merged_results
""",
        "complexity": """- **Time Complexity:** O(N log k), where N is the total number of items across all k streams and k is the number of streams. Each of the N items is pushed and popped from a heap of size at most k.
- **Space Complexity:** O(k) auxiliary space for the min-heap, plus O(N) to store the output merged stream."""
    },

    # Q4: Trapping Rain Water
    {
        "id": 4,
        "title": "Trapping Rain Water / Buffer Capacity Analysis",
        "topic": "Two Pointers",
        "difficulty": "Hard",
        "problem_statement": """Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
In distributed streaming systems, this algorithm is analogous to calculating buffer reserve capacities between bursty load peaks.""",
        "thought_process": """The volume of water trapped at any single index `i` is determined by the minimum of the maximum height to its left and the maximum height to its right, minus its own height:
`water[i] = max(0, min(left_max[i], right_max[i]) - height[i])`.

Precomputing `left_max` and `right_max` arrays takes O(N) time and O(N) space. However, we can optimize space to O(1) using the Two-Pointer technique:
1. We initialize two pointers: `left = 0` and `right = n - 1`, along with `left_max = 0` and `right_max = 0`.
2. If `height[left] <= height[right]`, we know that the water level at `left` is bounded by `left_max` (since `height[right]` is at least as large, ensuring a right wall exists). We update `left_max` and accumulate trapped water `left_max - height[left]`, then advance `left += 1`.
3. Otherwise, if `height[left] > height[right]`, the water level at `right` is bounded by `right_max`. We update `right_max` and accumulate `right_max - height[right]`, then decrement `right -= 1`.
4. We stop when `left >= right`.""",
        "code": """from typing import List

def trap(height: List[int]) -> int:
    if not height:
        return 0
        
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    total_water = 0
    
    # Process elevation bars inwards from both ends
    while left < right:
        if height[left] <= height[right]:
            # Left side is the limiting factor
            if height[left] >= left_max:
                left_max = height[left]
            else:
                total_water += left_max - height[left]
            left += 1
        else:
            # Right side is the limiting factor
            if height[right] >= right_max:
                right_max = height[right]
            else:
                total_water += right_max - height[right]
            right -= 1
            
    return total_water
""",
        "complexity": """- **Time Complexity:** O(N), as each bar is visited at most once by either the left or right pointer.
- **Space Complexity:** O(1), requiring only a few integer variables."""
    },

    # Q5: Course Schedule II
    {
        "id": 5,
        "title": "Course Schedule II / Automated Pipeline Dependency DAG & Cycle Detection",
        "topic": "Graph / Topological Sort (Kahn's BFS)",
        "difficulty": "Medium",
        "problem_statement": """There are a total of `numCourses` tasks you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take task `b` first if you want to take task `a`.
Return the ordering of tasks you should take to finish all tasks. If there are many valid answers, return any of them. If it is impossible to finish all tasks (due to a circular dependency), return an empty array.""",
        "thought_process": """This problem requires finding a valid topological ordering of a Directed Acyclic Graph (DAG) and detecting any cycles.
We apply Kahn's Algorithm (BFS-based Topological Sort):
1. Graph Representation: We build an adjacency list representing directed edges `prereq -> dependent` and maintain an `in_degree` array tracking how many incoming edges (unmet prerequisites) each task has.
2. Initialize Queue: Any task with `in_degree == 0` has no prerequisites and is ready to execute immediately. We enqueue all such tasks.
3. Process Tasks: While the queue is not empty, we pop task `u`, append it to our topological execution order, and iterate through all its dependent neighbors `v`. For each neighbor, we decrement `in_degree[v] -= 1`.
4. Trigger Dependent Tasks: If `in_degree[v]` drops to 0, all of task `v`'s prerequisites have been satisfied, so we push `v` into the queue.
5. Cycle Check: After the queue is empty, if the length of the execution order equals `numCourses`, no cycles exist and the order is valid. If it is less than `numCourses`, a circular dependency exists, so we return `[]`.""",
        "code": """from collections import deque, defaultdict
from typing import List

def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    adj = defaultdict(list)
    in_degree = [0] * numCourses
    
    # Build graph: prereq (b) -> dependent (a)
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
        
    # Queue all courses that have no prerequisites
    queue = deque([c for c in range(numCourses) if in_degree[c] == 0])
    order = []
    
    while queue:
        curr = queue.popleft()
        order.append(curr)
        
        # Decrement in-degree for all downstream dependent tasks
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # If not all courses could be ordered, a circular dependency exists
    if len(order) == numCourses:
        return order
    return []
""",
        "complexity": """- **Time Complexity:** O(V + E), where V is `numCourses` and E is the number of dependency constraints in `prerequisites`.
- **Space Complexity:** O(V + E) to store the adjacency list, in-degree array, and BFS queue."""
    },

    # Q6: Lowest Common Ancestor
    {
        "id": 6,
        "title": "Lowest Common Ancestor in a Binary Tree / Ad Category Taxonomy Hierarchy",
        "topic": "Tree DFS / Recursion",
        "difficulty": "Medium",
        "problem_statement": """Given a binary tree representing a hierarchical categorization taxonomy (e.g., ad product taxonomy: Sports -> Equipment -> Footwear), find the lowest common ancestor (LCA) of two given nodes `p` and `q`.
The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node `T` in the tree that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself).""",
        "thought_process": """We can solve this problem elegantly using post-order depth-first search (DFS):
1. Base Case: If the current root is `None`, or matches either target node `p` or `q`, we return the current root immediately. If we hit `p` or `q`, that node is an ancestor candidate.
2. Recursive Traversal: We recursively search the left subtree and the right subtree:
   - `left_result = lowestCommonAncestor(root.left, p, q)`
   - `right_result = lowestCommonAncestor(root.right, p, q)`
3. Decision Logic:
   - If both `left_result` and `right_result` are non-null, it means `p` is in one subtree and `q` is in the other subtree. Therefore, the current `root` is the Lowest Common Ancestor.
   - If only one of the subtrees returns a non-null node, both targets reside within that subtree (or one target is an ancestor of the other), so we bubble up that non-null node.
   - If both are null, neither node exists in the current subtree, so return `None`.""",
        "code": """class TreeNode:
    def __init__(self, x: int):
        self.val = x
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> Optional['TreeNode']:
    # Base case: empty node or found one of the targets
    if not root or root == p or root == q:
        return root
        
    # Search recursively in both left and right subtrees
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    # If both subtrees returned a match, current node is the LCA
    if left and right:
        return root
        
    # Otherwise return the non-null child (or None if both are None)
    return left if left else right
""",
        "complexity": """- **Time Complexity:** O(N), where N is the number of nodes in the binary tree. In the worst case, every node in the tree is visited.
- **Space Complexity:** O(H), where H is the height of the tree (O(log N) for balanced trees, O(N) for degenerate trees) representing recursion call stack space."""
    },

    # Q7: Word Break II
    {
        "id": 7,
        "title": "Word Break II / Ad Creative Keyword & Tag Segmentation",
        "topic": "Trie / Backtracking with Memoization",
        "difficulty": "Hard",
        "problem_statement": """Given a string `s` and a dictionary of strings `wordDict`, add spaces in `s` to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.
Note that the same word in the dictionary may be reused multiple times in the segmentation.
This is heavily used when parsing unsegmented campaign search keywords and live audio transcript tokens.""",
        "thought_process": """To avoid redundant subproblem evaluations, we use Depth-First Search (DFS) with Memoization:
1. State Definition: Let `dfs(start_index)` return all valid sentence segmentations for the substring `s[start_index:]`.
2. Memoization Table: We cache `memo[start_index] = list_of_sentences` to ensure each suffix is computed only once.
3. Recursive Step: At index `start`, we iterate through all possible prefixes `word = s[start:end]`. If `word` is in `wordDict` (stored as a set for O(1) membership check), we recursively evaluate the remaining suffix `dfs(end)`.
4. String Combination: For each sentence returned by `dfs(end)`, we prepend `word + " "` to form full sentences. If `end == len(s)`, the prefix itself completes the string.
5. Base Case: When `start == len(s)`, return `[""]`.""",
        "code": """from typing import List, Dict

def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    word_set = set(wordDict)
    # Memoization cache: start_idx -> list of segmented sentences
    memo: Dict[int, List[str]] = {}
    
    def dfs(start: int) -> List[str]:
        if start in memo:
            return memo[start]
            
        # Base case: reached end of string
        if start == len(s):
            return [""]
            
        sentences = []
        for end in range(start + 1, len(s) + 1):
            prefix = s[start:end]
            if prefix in word_set:
                # Recursively parse the remainder of the string
                rest_sentences = dfs(end)
                for rest in rest_sentences:
                    if rest:
                        sentences.append(prefix + " " + rest)
                    else:
                        sentences.append(prefix)
                        
        memo[start] = sentences
        return sentences
        
    return dfs(0)
""",
        "complexity": """- **Time Complexity:** O(N * 2^N) in the worst case (e.g., s = 'aaaa', wordDict = ['a', 'aa', 'aaa']), but practically O(N^2 + M) on average with memoization where N is the length of `s` and M is the number of valid sentences.
- **Space Complexity:** O(N * 2^N) to store all combinations in memoization, with O(N) recursive call stack depth."""
    },

    # Q8: Median from Data Stream
    {
        "id": 8,
        "title": "Find Median from High-Throughput Real-Time Bidding Stream",
        "topic": "Two Heaps (Max-Heap & Min-Heap)",
        "difficulty": "Hard",
        "problem_statement": """The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.
Design a data structure that supports the following two operations for a continuous real-time data stream of ad bid prices:
- `addNum(num: int) -> None`: Adds an integer number from the data stream.
- `findMedian() -> float`: Returns the median of all elements so far in O(1) time.""",
        "thought_process": """To compute the median in O(1) time dynamically as new numbers arrive, we partition the data stream into two halves:
1. Max-Heap (`small`): Stores the smaller half of the numbers. The root contains the largest of the small numbers.
2. Min-Heap (`large`): Stores the larger half of the numbers. The root contains the smallest of the large numbers.

Balancing Invariants:
1. Every element in `small` must be <= every element in `large`.
2. The sizes of both heaps must remain balanced: either `len(small) == len(large)` (even count) or `len(small) == len(large) + 1` (odd count).

Operations:
- `addNum(num)`: We first push `num` onto `small` (negated because Python's `heapq` is a min-heap). To ensure invariant 1, we pop the max from `small` and push it to `large`. If `len(large) > len(small)`, we pop the min from `large` back to `small` to maintain invariant 2.
- `findMedian()`: If `len(small) > len(large)`, the median is simply the top of `small`. If sizes are equal, the median is the average of both heap roots.""",
        "code": """import heapq

class MedianFinder:
    def __init__(self):
        # Max-heap (simulated with negative numbers) stores the smaller half
        self.small = []
        # Min-heap stores the larger half
        self.large = []

    def addNum(self, num: int) -> None:
        # Step 1: Add to small (max-heap)
        heapq.heappush(self.small, -num)
        
        # Step 2: Ensure all elements in small are <= elements in large
        largest_small = -heapq.heappop(self.small)
        heapq.heappush(self.large, largest_small)
        
        # Step 3: Maintain size balance (small can have at most 1 more element than large)
        if len(self.large) > len(self.small):
            smallest_large = heapq.heappop(self.large)
            heapq.heappush(self.small, -smallest_large)

    def findMedian(self) -> float:
        # If odd number of elements, small has the extra middle element
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        # If even number of elements, average of both roots
        return (-self.small[0] + self.large[0]) / 2.0
""",
        "complexity": """- **Time Complexity:** O(log N) for `addNum` because of heap pushes and pops; O(1) for `findMedian` by directly inspecting the heap roots.
- **Space Complexity:** O(N) to store all N incoming numbers across the two heaps."""
    },

    # Q9: Meeting Rooms II
    {
        "id": 9,
        "title": "Meeting Rooms II / Live Broadcast Commercial Break Resource Allocator",
        "topic": "Min-Heap / Interval Sweep",
        "difficulty": "Medium",
        "problem_statement": """Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, find the minimum number of conference rooms (or parallel encoder/transcoder channels) required to broadcast all scheduled intervals without conflicts.""",
        "thought_process": """Two events that overlap in time cannot share the same encoder channel or room. Therefore, the problem asks for the maximum number of concurrent overlapping intervals at any point in time.

Approach using a Min-Heap:
1. Sort Intervals: Sort all intervals by their start times. This allows us to process intervals chronologically as they begin.
2. Min-Heap for Active Rooms: We use a min-heap to track the end times of active rooms. The room with the earliest end time will always be at the top of the heap.
3. Allocation Logic:
   - For each interval `[start, end]`, we check if the earliest finishing room has already freed up (`heap[0] <= start`).
   - If it has, we can reuse that room: we pop the old end time from the heap and push the new `end` time.
   - If not, all current rooms are occupied, so we must allocate a new room: we simply push `end` onto the heap.
4. The maximum size reached by the heap equals the minimum number of rooms needed.""",
        "code": """import heapq
from typing import List

def minMeetingRooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
        
    # Sort intervals primarily by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min-heap to store the end times of currently active rooms
    end_times_heap = []
    
    # Allocate the first room
    heapq.heappush(end_times_heap, intervals[0][1])
    
    for start, end in intervals[1:]:
        # If the earliest ending room is free before this meeting starts, reuse it
        if end_times_heap[0] <= start:
            heapq.heappop(end_times_heap)
            
        # Push the new meeting's end time
        heapq.heappush(end_times_heap, end)
        
    # The number of allocated rooms is the size of the heap
    return len(end_times_heap)
""",
        "complexity": """- **Time Complexity:** O(N log N) dominated by sorting the N intervals. Processing each interval involves heap operations taking O(log N).
- **Space Complexity:** O(N) to hold the end times in the min-heap."""
    },

    # Q10: Longest Substring Without Repeating Characters
    {
        "id": 10,
        "title": "Longest Substring Without Repeating Characters",
        "topic": "Sliding Window + Hash Map",
        "difficulty": "Medium",
        "problem_statement": """Given a string `s`, find the length of the longest substring without duplicate characters.
In live telemetry tracking, this pattern is used to extract maximal contiguous valid token sequences without repeated identifiers.""",
        "thought_process": """We use a Sliding Window technique maintained by two pointers `left` and `right`, accompanied by a hash map `char_index` storing the most recent index where each character appeared:
1. As the `right` pointer iterates through the string from `0` to `len(s) - 1`, we check if the character `s[right]` was seen previously.
2. If `s[right]` exists in `char_index` and its previous position is `>= left`, we have encountered a duplicate within the current window. We move `left` forward to `char_index[s[right]] + 1` to exclude the previous instance.
3. We update `char_index[s[right]] = right` with the new occurrence.
4. The window length at any step is `right - left + 1`. We track the maximum window length observed.""",
        "code": """def lengthOfLongestSubstring(s: str) -> int:
    char_index = {}
    left = 0
    max_len = 0
    
    for right, char in enumerate(s):
        # If duplicate character found within current window, jump left pointer
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
            
        # Update latest position of character
        char_index[char] = right
        
        # Calculate current window size
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len
            
    return max_len
""",
        "complexity": """- **Time Complexity:** O(N), where N is the length of `s`. Each character is visited once by the right pointer, and the left pointer jumps forward monotonically.
- **Space Complexity:** O(min(N, M)), where M is the character set size (e.g., ASCII 128 or Unicode charset)."""
    },

    # Q11: Number of Islands
    {
        "id": 11,
        "title": "Number of Connected Server Clusters / Islands in Ad Network Topology",
        "topic": "Graph BFS / DFS",
        "difficulty": "Medium",
        "problem_statement": """Given an `m x n` 2D binary grid `grid` which represents a map of '1's (active nodes/servers) and '0's (network boundaries), return the number of isolated server clusters (islands).
An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.""",
        "thought_process": """We can solve this problem using Breadth-First Search (BFS) or Depth-First Search (DFS) to explore and sink each connected component:
1. We iterate through every cell `(r, c)` in the `m x n` grid.
2. When we encounter a cell with value `'1'`, we increment our cluster counter `islands_count += 1`.
3. We then launch a BFS or DFS starting from `(r, c)`. To avoid allocating an extra `visited` set, we can mutate the cell in place by setting it to `'0'` (sinking the island).
4. The traversal explores all 4 cardinal directions (up, down, left, right). For every neighbor that is `'1'`, we mark it as `'0'` and continue traversal until the entire connected component is exhausted.""",
        "code": """from collections import deque
from typing import List

def numIslands(grid: List[List[str]]) -> int:
    if not grid or not grid[0]:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    island_count = 0
    
    def bfs(start_r: int, start_c: int) -> None:
        queue = deque([(start_r, start_c)])
        grid[start_r][start_c] = '0'  # Mark visited by sinking the cell
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))
                    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                island_count += 1
                bfs(r, c)
                
    return island_count
""",
        "complexity": """- **Time Complexity:** O(M * N), where M is the number of rows and N is the number of columns. Every cell is visited at most a constant number of times.
- **Space Complexity:** O(min(M, N)) auxiliary space for the BFS queue in the worst-case scenario where the entire grid is land."""
    },

    # Q12: In-Memory Key-Value Store with Transactions
    {
        "id": 12,
        "title": "Design In-Memory Key-Value Store with Nested Transaction Support",
        "topic": "Hash Map + Rollback Stack",
        "difficulty": "Hard",
        "problem_statement": """Design an in-memory Key-Value store supporting nested ACID-like transactions with the following operations:
- `set(key: str, value: str)`: Sets the key to value.
- `get(key: str) -> Optional[str]`: Retrieves the value of the key, or None if it doesn't exist.
- `delete(key: str)`: Deletes the key.
- `begin()`: Starts a new transaction block. Transactions can be nested.
- `commit() -> bool`: Commits all changes made in the current transaction block. If no transaction is active, return False.
- `rollback() -> bool`: Reverts all changes made in the most recent transaction block. If no transaction is active, return False.""",
        "thought_process": """To support nested transactions with instant rollback capability, we maintain:
1. `global_store`: A dictionary representing the committed baseline key-value mappings.
2. `transaction_stack`: A list of dictionaries representing the delta modifications made within each active transaction level. Each entry in the stack maps `key -> previous_value` before the transaction mutated it.
3. Operations:
   - `begin()`: Push an empty undo dictionary `{}` onto `transaction_stack`.
   - `set(key, val)`: If inside a transaction, record `key`'s previous state in the current transaction's undo map (only on the first modification of that key within the transaction). Then update the current store.
   - `rollback()`: Pop the top transaction from the stack. For each key in its undo map, restore the previous value (or delete the key if it did not exist before).
   - `commit()`: Pop the top transaction from the stack. If there is still an outer transaction on the stack, merge the undo entries downwards; otherwise, the changes become permanent.""",
        "code": """from typing import Optional, Dict, List

class TransactionalKVStore:
    def __init__(self):
        self.store: Dict[str, str] = {}
        # Stack of transaction rollback dictionaries
        # Each dict maps key -> previous_value (or None if key didn't exist before)
        self.transaction_stack: List[Dict[str, Optional[str]]] = []

    def get(self, key: str) -> Optional[str]:
        return self.store.get(key, None)

    def set(self, key: str, value: str) -> None:
        if self.transaction_stack:
            # If inside transaction and key hasn't been logged yet in this frame
            current_frame = self.transaction_stack[-1]
            if key not in current_frame:
                current_frame[key] = self.store.get(key, None)
        self.store[key] = value

    def delete(self, key: str) -> None:
        if key not in self.store:
            return
        if self.transaction_stack:
            current_frame = self.transaction_stack[-1]
            if key not in current_frame:
                current_frame[key] = self.store.get(key, None)
        del self.store[key]

    def begin(self) -> None:
        # Start new transaction scope
        self.transaction_stack.append({})

    def rollback(self) -> bool:
        if not self.transaction_stack:
            return False
        # Pop the latest transaction frame and restore states
        frame = self.transaction_stack.pop()
        for key, prev_val in frame.items():
            if prev_val is None:
                self.store.pop(key, None)
            else:
                self.store[key] = prev_val
        return True

    def commit(self) -> bool:
        if not self.transaction_stack:
            return False
        committed_frame = self.transaction_stack.pop()
        # If there is an enclosing parent transaction, merge unrecorded previous states
        if self.transaction_stack:
            parent_frame = self.transaction_stack[-1]
            for key, prev_val in committed_frame.items():
                if key not in parent_frame:
                    parent_frame[key] = prev_val
        return True
""",
        "complexity": """- **Time Complexity:** O(1) for `get`, `begin`, and `set`/`delete` operations. O(K) for `rollback` and `commit`, where K is the number of keys mutated within the rolling transaction scope.
- **Space Complexity:** O(U) where U is the total number of uncommitted transaction state mutations stored across the stack."""
    },

    # Q13: Serialize and Deserialize Binary Tree
    {
        "id": 13,
        "title": "Serialize and Deserialize Binary Tree for Distributed State Replication",
        "topic": "Tree DFS / Serialization",
        "difficulty": "Hard",
        "problem_statement": """Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
Design an algorithm to serialize and deserialize a binary tree. Ensure the encoded string is compact and reconstruction handles null nodes correctly.""",
        "thought_process": """Pre-order Depth-First Search (DFS) provides a clean, unambiguous serialization format:
1. Serialization (`serialize`):
   - We traverse the tree in pre-order (`root -> left -> right`).
   - If a node is null, we append a sentinel string `"#"` to our list of tokens.
   - If a node is non-null, we append `str(node.val)`.
   - We join all tokens using a delimiter like `","`.
2. Deserialization (`deserialize`):
   - We split the serialized string by `","` into an iterator or queue of tokens.
   - We recursively build the tree:
     - Pop the next token from the front of the queue.
     - If the token is `"#"`, return `None`.
     - Otherwise, instantiate a new `TreeNode(int(token))`.
     - Recursively call `node.left = build()` and `node.right = build()`.
     - Return the reconstructed node.""",
        "code": """class TreeNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        tokens = []
        def dfs(node: Optional[TreeNode]):
            if not node:
                tokens.append("#")
                return
            tokens.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
            
        dfs(root)
        return ",".join(tokens)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = iter(data.split(","))
        
        def build() -> Optional[TreeNode]:
            val = next(tokens)
            if val == "#":
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
            
        return build()
""",
        "complexity": """- **Time Complexity:** O(N) for both serialization and deserialization, where N is the number of nodes in the binary tree.
- **Space Complexity:** O(N) memory to store the serialized string and recursive call stack."""
    },

    # Q14: Search in Rotated Sorted Array
    {
        "id": 14,
        "title": "Search in Rotated Sorted Array / Partition Offset Lookup",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "problem_statement": """There is an integer array `nums` sorted in ascending order (with distinct values) that has been rotated at an unknown pivot index `k` (`1 <= k < nums.length`).
Given the array `nums` after rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.
You must write an algorithm with O(log n) runtime complexity.""",
        "thought_process": """Even though the array has been rotated, dividing the array in half will always yield at least one sorted half:
1. We set `low = 0` and `high = len(nums) - 1`.
2. Compute `mid = (low + high) // 2`. If `nums[mid] == target`, we return `mid`.
3. Check which half is sorted:
   - Left Half Sorted (`nums[low] <= nums[mid]`): If `target` falls within the range `[nums[low], nums[mid])`, we search the left half (`high = mid - 1`); otherwise, search the right half (`low = mid + 1`).
   - Right Half Sorted (`nums[mid] < nums[high]`): If `target` falls within the range `(nums[mid], nums[high]]`, we search the right half (`low = mid + 1`); otherwise, search the left half (`high = mid - 1`).
4. If `low > high`, target is not present, so return -1.""",
        "code": """from typing import List

def search(nums: List[int], target: int) -> int:
    low, high = 0, len(nums) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
            
        # Determine if left half is sorted
        if nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]:
                high = mid - 1  # Target is within sorted left half
            else:
                low = mid + 1   # Target is in right half
        # Otherwise, right half must be sorted
        else:
            if nums[mid] < target <= nums[high]:
                low = mid + 1   # Target is within sorted right half
            else:
                high = mid - 1  # Target is in left half
                
    return -1
""",
        "complexity": """- **Time Complexity:** O(log N) as the search space is halved in every iteration.
- **Space Complexity:** O(1) auxiliary space using iterative two-pointer binary search."""
    },

    # Q15: Kth Largest Element in an Array
    {
        "id": 15,
        "title": "Kth Largest Element in an Array / Quickselect for Ad Auction Clearing Price",
        "topic": "Quickselect / Min-Heap",
        "difficulty": "Medium",
        "problem_statement": """Given an integer array `nums` and an integer `k`, return the `k`-th largest element in the array.
Note that it is the `k`-th largest element in sorted order, not the `k`-th distinct element.
Can you solve it in O(N) average time complexity?""",
        "thought_process": """There are two primary approaches:
1. Min-Heap of Size k: Maintain a min-heap of size `k`. Push each element into the heap; if heap size exceeds `k`, pop the minimum. At the end, the root is the k-th largest element. This takes O(N log k) time and O(k) space.
2. Quickselect Algorithm (Optimal):
   - Finding the k-th largest element is equivalent to finding the element at index `target_idx = len(nums) - k` in a sorted array.
   - We use the partition logic of Quicksort: choose a random pivot, partition elements into smaller and larger sections.
   - If the pivot ends up at `target_idx`, we are done.
   - If pivot index > `target_idx`, recurse on the left partition.
   - If pivot index < `target_idx`, recurse on the right partition.
   - On average, the work done is N + N/2 + N/4 + ... = 2N = O(N).""",
        "code": """import random
from typing import List

def findKthLargest(nums: List[int], k: int) -> int:
    target_idx = len(nums) - k
    
    def quickselect(left: int, right: int) -> int:
        pivot_idx = random.randint(left, right)
        pivot_val = nums[pivot_idx]
        
        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        
        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot_val:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1
                
        # Move pivot to final resting place
        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        
        if store_idx == target_idx:
            return nums[store_idx]
        elif store_idx < target_idx:
            return quickselect(store_idx + 1, right)
        else:
            return quickselect(left, store_idx - 1)
            
    return quickselect(0, len(nums) - 1)
""",
        "complexity": """- **Time Complexity:** O(N) average runtime using randomized Quickselect; O(N^2) worst case (extremely rare with random pivot selection).
- **Space Complexity:** O(1) auxiliary space (in-place partitioning) with O(log N) average recursion call stack."""
    },

    # Q16: Subarray Sum Equals K
    {
        "id": 16,
        "title": "Subarray Sum Equals K / Ad Campaign Budget Window Identification",
        "topic": "Prefix Sum + Hash Map",
        "difficulty": "Medium",
        "problem_statement": """Given an array of integers `nums` and an integer `k`, return the total number of continuous subarrays whose sum equals `k`.
This matches calculating continuous event stream intervals that consume exact campaign budget allocations.""",
        "thought_process": """A brute-force calculation evaluates all O(N^2) subarrays.
We can optimize this to O(N) using Prefix Sums and a Hash Map:
1. Let `prefix_sum[i]` be the cumulative sum of elements from index 0 to `i`.
2. The sum of a subarray from `j + 1` to `i` is given by: `sum(j+1 .. i) = prefix_sum[i] - prefix_sum[j]`.
3. We want this subarray sum to equal `k`:
   `prefix_sum[i] - prefix_sum[j] = k`  <=>  `prefix_sum[j] = prefix_sum[i] - k`.
4. As we iterate through `nums`, we maintain running cumulative sum `current_sum` and a hash map `prefix_counts` recording how many times each prefix sum has occurred.
5. In each step:
   - Check if `current_sum - k` exists in `prefix_counts`. If so, add its frequency to our result.
   - Increment `prefix_counts[current_sum] += 1`.
6. Base Case: Initialize `prefix_counts = {0: 1}` to account for subarrays starting at index 0 whose sum equals `k`.""",
        "code": """from typing import List
from collections import defaultdict

def subarraySum(nums: List[int], k: int) -> int:
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1  # Base case for subarrays starting at index 0
    
    current_sum = 0
    total_subarrays = 0
    
    for num in nums:
        current_sum += num
        # If (current_sum - k) was seen before, add the number of occurrences
        needed_prefix = current_sum - k
        if needed_prefix in prefix_counts:
            total_subarrays += prefix_counts[needed_prefix]
            
        prefix_counts[current_sum] += 1
        
    return total_subarrays
""",
        "complexity": """- **Time Complexity:** O(N), where N is the length of `nums`. We traverse the array once, performing O(1) hash map operations.
- **Space Complexity:** O(N) to store prefix sum counts in the hash map."""
    },

    # Q17: Word Search II
    {
        "id": 17,
        "title": "Word Search II / Live Broadcast Closed Caption Sensitive Word Detection",
        "topic": "Trie + 2D Backtracking",
        "difficulty": "Hard",
        "problem_statement": """Given an `m x n` board of characters and a list of strings `words`, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
In live broadcast moderation, this enables simultaneous scanning of video frame text grids for prohibited or brand-unsafe terms.""",
        "thought_process": """Running individual 2D DFS for every single word results in repeated board traversals.
Instead, we index all search words into a Prefix Tree (Trie) and traverse the board once:
1. Build Trie: Insert all `words` into a Trie. Each terminal node stores the complete word string for O(1) retrieval.
2. DFS Traversal: For each cell `(r, c)` on the board, if `board[r][c]` matches a root child in the Trie, launch a backtracking search.
3. Pruning:
   - Mark the current cell visited by setting `board[r][c] = '#'` to prevent reusing it.
   - Explore all 4 orthogonal directions.
   - Once a word is found, add it to the output set and set `node.word = None` to prevent duplicate matches.
   - Trie Pruning: If a leaf Trie node has no children after exploration, delete it from its parent to prune future traversal branches.
   - Restore cell character `board[r][c] = original_char` during backtrack.""",
        "code": """from typing import List, Dict

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.word: Optional[str] = None

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Step 1: Build the Trie
        root = TrieNode()
        for word in words:
            curr = root
            for char in word:
                if char not in curr.children:
                    curr.children[char] = TrieNode()
                curr = curr.children[char]
            curr.word = word
            
        rows, cols = len(board), len(board[0])
        result = []
        
        # Step 2: Backtracking search
        def backtrack(r: int, c: int, parent_node: TrieNode):
            char = board[r][c]
            curr_node = parent_node.children[char]
            
            # Check if current node completes a word
            if curr_node.word:
                result.append(curr_node.word)
                curr_node.word = None  # Avoid duplicate entries
                
            # Mark cell visited
            board[r][c] = '#'
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in curr_node.children:
                    backtrack(nr, nc, curr_node)
                    
            # Restore cell character
            board[r][c] = char
            
            # Prune leaf node to optimize remaining searches
            if not curr_node.children:
                parent_node.children.pop(char)
                
        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root.children:
                    backtrack(r, c, root)
                    
        return result
""",
        "complexity": """- **Time Complexity:** O(M * N * 4^(L-1)), where M*N is board size and L is maximum word length. Pruning significantly lowers this in practice.
- **Space Complexity:** O(W * L) to construct the Trie, where W is the number of words and L is average word length."""
    },

    # Q18: Alien Dictionary
    {
        "id": 18,
        "title": "Alien Dictionary / Custom Ad Priority & Tier Ordering Resolution",
        "topic": "Graph / Topological Sort",
        "difficulty": "Hard",
        "problem_statement": """There is a new alien language that uses the Latin alphabet. However, the order among letters is unknown to you.
You are given a list of strings `words` from the alien language's dictionary, where the strings are claimed to be sorted lexicographically by the rules of this new language.
Derive the order of letters in this language. If the order is invalid (e.g., contains a cycle or prefix conflict), return `""`. If there are multiple valid orders, return any of them.""",
        "thought_process": """This problem maps directly to building a Directed Graph of character precedence and finding a Topological Order:
1. Character Extraction: Every unique character in all words is a node in the graph. Initialize `in_degree[char] = 0`.
2. Edge Extraction: Compare adjacent pairs of words `w1` and `w2`:
   - Prefix Conflict: If `len(w1) > len(w2)` and `w1.startswith(w2)`, the ordering is fundamentally invalid (e.g., "apple" before "app"), return `""`.
   - Find First Difference: Find the first index `i` where `w1[i] != w2[i]`. A directed edge exists from `w1[i] -> w2[i]`.
   - If the edge hasn't been added yet, add it to `adj[w1[i]]` and increment `in_degree[w2[i]] += 1`.
3. Topological Sort (BFS): Enqueue all characters with `in_degree == 0`. Process characters, decrementing neighbor in-degrees.
4. Validation: If the length of the topological order matches the number of unique characters, return the joined string; otherwise, a cycle exists, return `""`.""",
        "code": """from collections import deque, defaultdict
from typing import List

def alienOrder(words: List[str]) -> str:
    adj = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    # Compare adjacent words to infer character ordering
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        # Check invalid prefix case
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
            
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
                
    # Kahn's BFS
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    order = []
    
    while queue:
        curr = queue.popleft()
        order.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(order) == len(in_degree):
        return "".join(order)
    return ""
""",
        "complexity": """- **Time Complexity:** O(C), where C is the total length of all words in the input. Comparing adjacent words takes at most O(C) operations.
- **Space Complexity:** O(1) auxiliary space (bounded by the alphabet size, at most 26 lowercase English letters)."""
    },

    # Q19: Reorganize String
    {
        "id": 19,
        "title": "Reorganize String / Commercial Ad Pod Competitive Separation",
        "topic": "Max-Heap + Greedy",
        "difficulty": "Medium",
        "problem_statement": """Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same.
Return any possible rearrangement of `s` or return `""` if not possible.
In broadcast ad pod construction, this ensures competitive separation: two ads from competing automotive brands are never placed back-to-back.""",
        "thought_process": """If any character appears more than `(len(s) + 1) // 2` times, by the Pigeonhole Principle it is impossible to separate all instances, so we immediately return `""`.

Greedy Approach with a Max-Heap:
1. Count character frequencies using `collections.Counter(s)`.
2. Push all characters and their counts into a Max-Heap (stored as `(-count, char)`).
3. In each step, we pop the most frequent character `char1` from the heap and append it to our result.
4. To avoid placing two identical characters consecutively, we cannot immediately push `char1` back. Instead, we pop the second most frequent character `char2`, append it to the result, decrement both frequencies, and push any remaining counts back into the heap.
5. If only one character remains in the heap with count 1, append it to conclude.""",
        "code": """import heapq
from collections import Counter

def reorganizeString(s: str) -> str:
    counts = Counter(s)
    max_freq = max(counts.values())
    
    # Pigeonhole principle check
    if max_freq > (len(s) + 1) // 2:
        return ""
        
    # Max-heap storing (-count, char)
    max_heap = [(-count, char) for char, count in counts.items()]
    heapq.heapify(max_heap)
    
    result = []
    
    while len(max_heap) >= 2:
        cnt1, ch1 = heapq.heappop(max_heap)
        cnt2, ch2 = heapq.heappop(max_heap)
        
        result.append(ch1)
        result.append(ch2)
        
        # Decrement counts (stored as negative values)
        if cnt1 + 1 < 0:
            heapq.heappush(max_heap, (cnt1 + 1, ch1))
        if cnt2 + 1 < 0:
            heapq.heappush(max_heap, (cnt2 + 1, ch2))
            
    if max_heap:
        result.append(max_heap[0][1])
        
    return "".join(result)
""",
        "complexity": """- **Time Complexity:** O(N log A), where N is the length of `s` and A is the alphabet size (at most 26 for English letters). Since A <= 26, this is effectively O(N).
- **Space Complexity:** O(A) auxiliary space for the heap and hash map."""
    },

    # Q20: Minimum Window Substring
    {
        "id": 20,
        "title": "Minimum Window Substring / Minimum Telemetry Range Covering Target Signals",
        "topic": "Sliding Window with Frequency Map",
        "difficulty": "Hard",
        "problem_statement": """Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `""`.""",
        "thought_process": """We use a variable-size sliding window with two pointers `left` and `right`:
1. Target Counts: Store frequency of each character in `t` in `target_counts`. Let `required = len(target_counts)` be the number of unique characters that must meet target frequency.
2. Window Expansion: Move `right` pointer forward. If `s[right]` is in `target_counts`, increment `window_counts[s[right]]`. If `window_counts[s[right]] == target_counts[s[right]]`, increment `formed += 1`.
3. Window Contraction: As long as `formed == required` (all characters satisfied), the current window `s[left:right+1]` is valid:
   - Check if current window is smaller than previously recorded minimum; if so, update minimum window indices.
   - Shrink window from the left by advancing `left += 1`, decrementing `window_counts[s[left]]`. If `window_counts` drops below `target_counts`, decrement `formed -= 1`.
4. Return the recorded minimum substring.""",
        "code": """from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not s or not t:
        return ""
        
    target_counts = Counter(t)
    required = len(target_counts)
    
    left = 0
    formed = 0
    window_counts = {}
    
    # Store: (window_length, start_idx, end_idx)
    min_window = (float('inf'), None, None)
    
    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1
            
        # Try to contract window until it's no longer valid
        while left <= right and formed == required:
            # Update minimum window record
            if (right - left + 1) < min_window[0]:
                min_window = (right - left + 1, left, right)
                
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                formed -= 1
                
            left += 1
            
    return "" if min_window[0] == float('inf') else s[min_window[1]:min_window[2] + 1]
""",
        "complexity": """- **Time Complexity:** O(M + N), where M = len(s) and N = len(t). Each character in `s` is visited at most twice (once by right, once by left).
- **Space Complexity:** O(M + N) to maintain frequency maps."""
    },

    # Q21: Decode String
    {
        "id": 21,
        "title": "Decode String / Nested Macro Expansion in Dynamic Ad Templates",
        "topic": "Stack",
        "difficulty": "Medium",
        "problem_statement": """Given an encoded string, return its decoded string.
The encoding rule is: `k[encoded_string]`, where the `encoded_string` inside the square brackets is being repeated exactly `k` times. Note that `k` is guaranteed to be a positive integer.
You may assume that the input string is always valid; no extra white spaces, square brackets are well-formed, etc.""",
        "thought_process": """When dealing with nested patterns like `3[a2[c]]` (which yields `accaccacc`), a Stack is ideal for tracking context:
1. State Variables: Maintain `curr_str = ""` and `curr_num = 0`.
2. Iteration:
   - Digits (`char.isdigit()`): Build multi-digit numbers: `curr_num = curr_num * 10 + int(char)`.
   - Open Bracket (`[`): A new nested context begins. We push `(curr_str, curr_num)` onto our stack, then reset `curr_str = ""` and `curr_num = 0`.
   - Close Bracket (`]`): A nested context concludes. We pop `(prev_str, repeat_count)` from the stack. The new `curr_str` becomes `prev_str + curr_str * repeat_count`.
   - Letters: Append `char` directly to `curr_str`.
3. Return `curr_str` at the end.""",
        "code": """def decodeString(s: str) -> str:
    stack = []
    curr_str = ""
    curr_num = 0
    
    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == '[':
            # Push current string and repeat multiplier onto stack
            stack.append((curr_str, curr_num))
            curr_str = ""
            curr_num = 0
        elif char == ']':
            prev_str, repeat_k = stack.pop()
            curr_str = prev_str + curr_str * repeat_k
        else:
            curr_str += char
            
    return curr_str
""",
        "complexity": """- **Time Complexity:** O(Total Output Length) to construct and duplicate strings.
- **Space Complexity:** O(D) where D is the maximum nesting depth of square brackets."""
    },

    # Q22: All Nodes Distance K in Binary Tree
    {
        "id": 22,
        "title": "All Nodes Distance K in Binary Tree / Broadcast Infrastructure Blast Radius Analysis",
        "topic": "Tree to Graph Conversion + BFS",
        "difficulty": "Medium",
        "problem_statement": """Given the `root` of a binary tree, the value of a target node `target`, and an integer `k`, return an array of the values of all nodes that have a distance `k` from the target node in any direction (including parent directions).""",
        "thought_process": """In a standard binary tree, node pointers only go downwards to children. To search in all directions (including upwards toward parents), we can:
1. Map Parent Pointers: Run a DFS to build a `parent` dictionary mapping each node to its parent node.
2. BFS from Target: Launch a Breadth-First Search (BFS) starting at the `target` node:
   - Keep a `visited` set to avoid cycling back.
   - At each step of the BFS, expand in all 3 possible directions: `node.left`, `node.right`, and `node.parent`.
   - Increment distance level at each BFS wave.
3. When the BFS reaches distance level `k`, the contents of the queue represent all nodes at distance `k`.""",
        "code": """from collections import deque
from typing import List, Optional

class TreeNode:
    def __init__(self, x: int):
        self.val = x
        self.left = None
        self.right = None

def distanceK(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    parents = {}
    
    # DFS to record parent pointers for all nodes
    def find_parents(node: Optional[TreeNode], parent: Optional[TreeNode]):
        if not node:
            return
        parents[node] = parent
        find_parents(node.left, node)
        find_parents(node.right, node)
        
    find_parents(root, None)
    
    # BFS starting from the target node
    queue = deque([(target, 0)])
    visited = {target}
    result = []
    
    while queue:
        node, dist = queue.popleft()
        
        if dist == k:
            result.append(node.val)
            continue
            
        # Explore left, right, and parent neighbors
        for neighbor in [node.left, node.right, parents.get(node)]:
            if neighbor and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
                
    return result
""",
        "complexity": """- **Time Complexity:** O(N), where N is the number of nodes in the binary tree.
- **Space Complexity:** O(N) to store parent pointers, visited set, and BFS queue."""
    },

    # Q23: Median of Two Sorted Arrays
    {
        "id": 23,
        "title": "Find Median of Two Sorted Arrays / Distributed P99 Auction Latency Calculation",
        "topic": "Binary Search on Partitions",
        "difficulty": "Hard",
        "problem_statement": """Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.
The overall run time complexity should be O(log (m+n)).""",
        "thought_process": """Merging the two arrays takes O(m + n) time. To achieve O(log(min(m, n))), we binary search for the correct partition cut across the smaller array:
1. Ensure `nums1` is the smaller array (if not, swap). Let `m = len(nums1)` and `n = len(nums2)`.
2. The combined left half must contain `(m + n + 1) // 2` elements.
3. If we pick `cut1` elements from `nums1`, we must pick `cut2 = ((m + n + 1) // 2) - cut1` elements from `nums2`.
4. Partition Boundaries:
   - `left1 = nums1[cut1 - 1]` (or -inf if cut1 == 0)
   - `right1 = nums1[cut1]` (or +inf if cut1 == m)
   - `left2 = nums2[cut2 - 1]` (or -inf if cut2 == 0)
   - `right2 = nums2[cut2]` (or +inf if cut2 == n)
5. Validation:
   - If `left1 <= right2` and `left2 <= right1`, the partition is valid!
     - If total length is odd, median is `max(left1, left2)`.
     - If even, median is `(max(left1, left2) + min(right1, right2)) / 2.0`.
   - If `left1 > right2`, we took too many elements from `nums1`, so move binary search left (`high = cut1 - 1`).
   - Otherwise, move binary search right (`low = cut1 + 1`).""",
        "code": """from typing import List

def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    # Ensure nums1 is smaller to minimize binary search range
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
        
    m, n = len(nums1), len(nums2)
    low, high = 0, m
    total_left = (m + n + 1) // 2
    
    while low <= high:
        cut1 = (low + high) // 2
        cut2 = total_left - cut1
        
        left1 = float('-inf') if cut1 == 0 else nums1[cut1 - 1]
        right1 = float('inf') if cut1 == m else nums1[cut1]
        
        left2 = float('-inf') if cut2 == 0 else nums2[cut2 - 1]
        right2 = float('inf') if cut2 == n else nums2[cut2]
        
        # Valid partition found
        if left1 <= right2 and left2 <= right1:
            if (m + n) % 2 == 1:
                return float(max(left1, left2))
            return (max(left1, left2) + min(right1, right2)) / 2.0
        elif left1 > right2:
            high = cut1 - 1
        else:
            low = cut1 + 1
            
    return 0.0
""",
        "complexity": """- **Time Complexity:** O(log(min(m, n))) by performing binary search strictly over the shorter array.
- **Space Complexity:** O(1) auxiliary space."""
    },

    # Q24: Binary Tree Maximum Path Sum
    {
        "id": 24,
        "title": "Binary Tree Maximum Path Sum / Ad Campaign Multi-Touch Attribution Path Value",
        "topic": "Tree Post-Order DFS",
        "difficulty": "Hard",
        "problem_statement": """A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.
The path sum of a path is the sum of the node's values in the path.
Given the `root` of a binary tree, return the maximum path sum of any non-empty path.""",
        "thought_process": """For any node in the tree, there are two distinct concepts:
1. Max Single Branch Gain (`max_gain`): The maximum sum path starting from this node and extending down through either its left OR right subtree (cannot branch in both directions if extending to the parent). This value is returned to the parent: `node.val + max(0, left_gain, right_gain)`.
2. Arch Path Through Node: A path that arches through the current node using both left and right branches: `current_arch_sum = node.val + max(0, left_gain) + max(0, right_gain)`. This arch path cannot be extended upwards, but it might be the global maximum path.

We use post-order DFS to compute `max_gain` from leaves up to the root while maintaining a global `max_sum` variable tracking the highest arch sum seen anywhere.""",
        "code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root: Optional[TreeNode]) -> int:
    max_sum = float('-inf')
    
    def dfs(node: Optional[TreeNode]) -> int:
        nonlocal max_sum
        if not node:
            return 0
            
        # Ignore subtrees with negative contribution
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        
        # Max path arched at current node
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        # Return max single branch gain to parent
        return node.val + max(left_gain, right_gain)
        
    dfs(root)
    return max_sum
""",
        "complexity": """- **Time Complexity:** O(N), where N is the number of nodes in the binary tree.
- **Space Complexity:** O(H) call stack space, where H is tree height."""
    },

    # Q25: Task Scheduler
    {
        "id": 25,
        "title": "Task Scheduler / Live Sports Commercial Slot Pacer with Cooldown",
        "topic": "Greedy / Max-Heap / Frequency Math",
        "difficulty": "Medium",
        "problem_statement": """Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.
However, there is a non-negative integer `n` that represents the cooldown period between two same tasks (the same task must be separated by at least `n` units of time).
Return the least number of units of times that the CPU will take to finish all the given tasks.""",
        "thought_process": """We can solve this problem in O(N) time using mathematical slot framing:
1. Find the highest task frequency `max_freq` and count how many tasks share this maximum frequency `max_count`.
2. Construct execution frames: The task with `max_freq` requires `max_freq - 1` gaps between its executions.
3. Each gap has size `n`. Therefore, the number of empty slots within these blocks is:
   `empty_slots = (max_freq - 1) * (n - (max_count - 1))`.
4. Calculate remaining tasks that can fill these slots:
   `available_tasks = len(tasks) - (max_freq * max_count)`.
5. The number of idle units is `max(0, empty_slots - available_tasks)`.
6. Total time is simply `len(tasks) + idles`.""",
        "code": """from collections import Counter
from typing import List

def leastInterval(tasks: List[str], n: int) -> int:
    task_counts = Counter(tasks)
    max_freq = max(task_counts.values())
    
    # Count how many tasks appear with max_freq
    max_freq_tasks = sum(1 for count in task_counts.values() if count == max_freq)
    
    # Calculate minimal intervals needed based on the most frequent task
    part_count = max_freq - 1
    part_length = n - (max_freq_tasks - 1)
    empty_slots = part_count * part_length
    available_tasks = len(tasks) - (max_freq * max_freq_tasks)
    idles = max(0, empty_slots - available_tasks)
    
    return len(tasks) + idles
""",
        "complexity": """- **Time Complexity:** O(N), where N is the number of tasks.
- **Space Complexity:** O(1) auxiliary space (at most 26 uppercase task keys)."""
    },

    # Q26: Longest Increasing Subsequence
    {
        "id": 26,
        "title": "Longest Increasing Subsequence / Viewer Retention Trend Analysis",
        "topic": "Patience Sorting / Binary Search",
        "difficulty": "Medium",
        "problem_statement": """Given an integer array `nums`, return the length of the longest strictly increasing subsequence.
Solve in O(N log N) runtime complexity.""",
        "thought_process": """A naive dynamic programming approach takes O(N^2) time. We can achieve O(N log N) using Patience Sorting with Binary Search:
1. Maintain an array `tails`, where `tails[i]` stores the smallest tail of all increasing subsequences of length `i + 1` found so far.
2. For each number `x` in `nums`:
   - Use `bisect_left(tails, x)` to find the smallest element in `tails` that is `>= x`.
   - If `x` is larger than all elements in `tails`, append `x` (extending the longest subsequence length by 1).
   - If `tails[idx] >= x`, replace `tails[idx] = x`. This lowers the bar for future numbers to extend subsequences of that length.
3. The length of `tails` at the end is the length of the LIS.""",
        "code": """import bisect
from typing import List

def lengthOfLIS(nums: List[int]) -> int:
    tails = []
    
    for num in nums:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
            
    return len(tails)
""",
        "complexity": """- **Time Complexity:** O(N log N), where N is the length of `nums`. For each of the N numbers, we perform a binary search taking O(log N).
- **Space Complexity:** O(N) to store the `tails` array."""
    },

    # Q27: Network Delay Time
    {
        "id": 27,
        "title": "Network Delay Time / Multi-Region Broadcast Ad Signal Propagation",
        "topic": "Graph / Dijkstra's Algorithm",
        "difficulty": "Medium",
        "problem_statement": """You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (u_i, v_i, w_i)`, where `u_i` is the source node, `v_i` is the target node, and `w_i` is the time it takes for a signal to travel from source to target.
We will send a signal from a given node `k`. Return the minimum time it takes for all the `n` nodes to receive the signal. If it is impossible for all `n` nodes to receive the signal, return `-1`.""",
        "thought_process": """This problem asks for the Single-Source Shortest Path to all nodes on a directed graph with positive edge weights, which is solved using Dijkstra's Algorithm:
1. Build adjacency list `adj[u]` storing `(neighbor, travel_time)`.
2. Maintain a `min_heap` initialized with `(0, k)` representing `(accumulated_time, current_node)`.
3. Track `shortest_dist[node]` to store the minimum known latency to reach each node.
4. Process nodes greedily from the min-heap:
   - If node already reached with a shorter latency, skip.
   - Otherwise, record `shortest_dist[curr] = curr_time`.
   - Traverse neighbors and push `(curr_time + weight, neighbor)` to heap.
5. If `len(shortest_dist) == n`, return `max(shortest_dist.values())`; otherwise, some nodes are unreachable, return `-1`.""",
        "code": """import heapq
from collections import defaultdict
from typing import List

def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
        
    min_heap = [(0, k)]
    shortest_dist = {}
    
    while min_heap:
        curr_time, node = heapq.heappop(min_heap)
        
        if node in shortest_dist:
            continue
            
        shortest_dist[node] = curr_time
        
        for neighbor, weight in adj[node]:
            if neighbor not in shortest_dist:
                heapq.heappush(min_heap, (curr_time + weight, neighbor))
                
    if len(shortest_dist) == n:
        return max(shortest_dist.values())
    return -1
""",
        "complexity": """- **Time Complexity:** O(E log V), where E is the number of edges and V is the number of nodes (`n`).
- **Space Complexity:** O(V + E) to store the adjacency list and priority queue."""
    },

    # Q28: Basic Calculator II
    {
        "id": 28,
        "title": "Basic Calculator II / Dynamic Real-Time Bidding Formula Evaluator",
        "topic": "Stack / Expression Evaluation",
        "difficulty": "Medium",
        "problem_statement": """Given a string `s` which represents an expression, evaluate this expression and return its value.
The integer division should truncate toward zero.
You may assume that the given expression is always valid. All intermediate results will be in the range of `[-2^31, 2^31 - 1]`.
Operators include `+`, `-`, `*`, `/` and spaces.""",
        "thought_process": """Multiplication and division have higher precedence than addition and subtraction:
1. Traverse string while accumulating digits into `curr_num`.
2. When an operator or the end of the string is encountered:
   - If previous operator was `+`: push `curr_num` onto stack.
   - If `-`: push `-curr_num` onto stack.
   - If `*`: pop the last number from stack, multiply with `curr_num`, and push result back.
   - If `/`: pop last number, divide by `curr_num` (using integer truncation toward zero: `int(prev / curr_num)`), and push back.
   - Update operator to the newly encountered character and reset `curr_num = 0`.
3. Return `sum(stack)`.""",
        "code": """def calculate(s: str) -> int:
    stack = []
    curr_num = 0
    op = '+'
    
    for i, char in enumerate(s):
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
            
        # Process on operator or at the end of the string
        if (not char.isdigit() and char != ' ') or i == len(s) - 1:
            if op == '+':
                stack.append(curr_num)
            elif op == '-':
                stack.append(-curr_num)
            elif op == '*':
                stack.append(stack.pop() * curr_num)
            elif op == '/':
                prev = stack.pop()
                stack.append(int(prev / curr_num))  # Truncate towards zero
                
            op = char
            curr_num = 0
            
    return sum(stack)
""",
        "complexity": """- **Time Complexity:** O(N), where N is the length of string `s`.
- **Space Complexity:** O(N) auxiliary space for the evaluation stack."""
    },

    # Q29: Maximal Square
    {
        "id": 29,
        "title": "Maximal Square / 2D Display Screen Layout Space Optimization",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "problem_statement": """Given an `m x n` binary matrix filled with `0`'s and `1`'s, find the largest square containing only `1`'s and return its area.""",
        "thought_process": """We use 2D Dynamic Programming:
1. Let `dp[r][c]` represent the side length of the largest square whose bottom-right corner is at cell `(r, c)`.
2. If `matrix[r][c] == '1'`:
   - A square ending at `(r, c)` can only be formed if squares of size `k` exist ending at `(r-1, c)`, `(r, c-1)`, and `(r-1, c-1)`.
   - Transition: `dp[r][c] = 1 + min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1])`.
3. If `matrix[r][c] == '0'`: `dp[r][c] = 0`.
4. Keep track of `max_side` seen across all cells.
5. Return `max_side * max_side`.""",
        "code": """from typing import List

def maximalSquare(matrix: List[List[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
        
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    max_side = 0
    
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if matrix[r - 1][c - 1] == '1':
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                if dp[r][c] > max_side:
                    max_side = dp[r][c]
                    
    return max_side * max_side
""",
        "complexity": """- **Time Complexity:** O(M * N), where M and N are matrix dimensions.
- **Space Complexity:** O(M * N) (can be reduced to O(N) using a single 1D rolling array)."""
    },

    # Q30: Rate Limiter Sliding Window Counter
    {
        "id": 30,
        "title": "Distributed Rate Limiter / Sliding Window Counter",
        "topic": "Sliding Window / In-Memory Queue",
        "difficulty": "Medium",
        "problem_statement": """Design a Rate Limiter that allows at most `max_requests` requests per client within any sliding window of `window_size_seconds`.
Implement `allow_request(client_id: str, timestamp: float) -> bool` which returns `True` if the request is permitted, or `False` if dropped due to rate limiting.""",
        "thought_process": """To prevent sudden boundary burst vulnerabilities that afflict fixed-window algorithms, we use the Sliding Window Log approach:
1. For each `client_id`, maintain a double-ended queue `deque` of past request timestamps.
2. When a request arrives at `timestamp`:
   - Compute cutoff time: `cutoff = timestamp - window_size_seconds`.
   - Evict all timestamps from the front of the client's deque that are `<= cutoff`.
   - Check current deque length: if `len(dq) < max_requests`, append `timestamp` and return `True`.
   - Otherwise, the client has exceeded their quota, so drop request and return `False`.""",
        "code": """import time
from collections import defaultdict, deque
from typing import Dict

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_size_seconds: float):
        self.max_requests = max_requests
        self.window_size_seconds = window_size_seconds
        # Maps client_id -> deque of request timestamps
        self.client_logs: Dict[str, deque] = defaultdict(deque)

    def allow_request(self, client_id: str, timestamp: Optional[float] = None) -> bool:
        now = timestamp if timestamp is not None else time.time()
        cutoff = now - self.window_size_seconds
        dq = self.client_logs[client_id]
        
        # Purge stale requests outside current sliding window
        while dq and dq[0] <= cutoff:
            dq.popleft()
            
        # Check quota
        if len(dq) < self.max_requests:
            dq.append(now)
            return True
            
        return False
""",
        "complexity": """- **Time Complexity:** O(1) amortized per request. Each timestamp is added once and evicted at most once.
- **Space Complexity:** O(C * R), where C is the number of active clients and R is `max_requests` per window."""
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(dsa_questions)} DSA questions successfully.")
