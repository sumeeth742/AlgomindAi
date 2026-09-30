import type { ArrayStep } from "@/components/visualizers/ArrayPointerViz";
import type { StackStep } from "@/components/visualizers/StackViz";
import type { LinkedListStep } from "@/components/visualizers/LinkedListViz";
import type { TreeNode, TreeStep } from "@/components/visualizers/TreeViz";
import type { GraphNode, GraphEdge, GraphStep } from "@/components/visualizers/GraphViz";
import type { GridStep } from "@/components/visualizers/GridViz";
import type { HashMapStep } from "@/components/visualizers/HashMapViz";
import type { BitStep } from "@/components/visualizers/BitViz";
import type { QueueStep } from "@/components/visualizers/QueueViz";
import type { GrowthStep } from "@/components/visualizers/GrowthChartViz";

export type VisualizationConfig =
  | { type: "array"; array: (number | string)[]; steps: ArrayStep[]; valueLabel?: string }
  | { type: "stack"; steps: StackStep[] }
  | { type: "linkedlist"; steps: LinkedListStep[] }
  | { type: "tree"; nodes: TreeNode[]; rootId: string; steps: TreeStep[] }
  | { type: "graph"; nodes: GraphNode[]; edges: GraphEdge[]; steps: GraphStep[] }
  | { type: "grid"; rowLabels: string[]; colLabels: string[]; steps: GridStep[] }
  | { type: "hashmap"; steps: HashMapStep[] }
  | { type: "bits"; steps: BitStep[] }
  | { type: "queue"; steps: QueueStep[]; frontLabel?: string; backLabel?: string }
  | { type: "growth"; steps: GrowthStep[] };

// Every trace below mirrors the exact worked example already written in that
// skill's lesson markdown, so the animation and the prose agree with each other
// instead of introducing a second, disconnected example. All 28 DSA skills have
// one -- some reuse a visually-similar component (e.g. a heap borrows the
// "changing collection of boxes" queue view) rather than a bespoke one for every
// single concept, but every skill has something concrete and hand-verified.
export const VISUALIZATIONS: Record<string, VisualizationConfig> = {
  PROGRAMMING_BASICS: {
    type: "array",
    array: [10, 20, 30],
    valueLabel: "total",
    steps: [
      { pointers: { x: 0 }, highlight: [0], note: "x=10: total = 0 + 10 = 10", runningValue: "10" },
      { pointers: { x: 1 }, highlight: [1], note: "x=20: total = 10 + 20 = 30", runningValue: "30" },
      { pointers: { x: 2 }, highlight: [2], note: "x=30: total = 30 + 30 = 60", runningValue: "60" },
      { pointers: {}, highlight: [0, 1, 2], note: "Loop finished. Final total = 60.", runningValue: "60" },
    ],
  },

  ALGORITHMIC_THINKING: {
    type: "growth",
    steps: [
      { n: 10, note: "At n=10, all three are small and roughly comparable.", values: [
        { label: "O(n)", ops: 10, color: "#059669" }, { label: "O(n log n)", ops: 33, color: "#0284c7" }, { label: "O(n²)", ops: 100, color: "#dc2626" },
      ] },
      { n: 100, note: "At n=100, O(n²) is already 100x bigger than O(n).", values: [
        { label: "O(n)", ops: 100, color: "#059669" }, { label: "O(n log n)", ops: 664, color: "#0284c7" }, { label: "O(n²)", ops: 10000, color: "#dc2626" },
      ] },
      { n: 1000, note: "At n=1,000, O(n²) has ballooned to a million operations.", values: [
        { label: "O(n)", ops: 1000, color: "#059669" }, { label: "O(n log n)", ops: 9966, color: "#0284c7" }, { label: "O(n²)", ops: 1000000, color: "#dc2626" },
      ] },
      { n: 100000, note: "At n=100,000, O(n²) needs 10 billion operations -- far too slow. O(n log n) is still fast.", values: [
        { label: "O(n)", ops: 100000, color: "#059669" }, { label: "O(n log n)", ops: 1660000, color: "#0284c7" }, { label: "O(n²)", ops: 10000000000, color: "#dc2626" },
      ] },
    ],
  },

  ARRAYS_TRAVERSAL: {
    type: "array",
    array: [-2, 1, -3, 4, -1, 2, 1, -5, 4],
    valueLabel: "current_sum / best",
    steps: [
      { pointers: { i: 0 }, highlight: [0], note: "Start: current_sum = -2, best = -2", runningValue: "-2 / -2" },
      { pointers: { i: 1 }, highlight: [1], note: "x=1: extending gives 1, which beats starting fresh -- current_sum=1", runningValue: "1 / 1" },
      { pointers: { i: 2 }, highlight: [2], note: "x=-3: current_sum drops to -2, but best stays at 1", runningValue: "-2 / 1" },
      { pointers: { i: 3 }, highlight: [3], note: "x=4: better to start fresh here -- current_sum=4, new best!", runningValue: "4 / 4" },
      { pointers: { i: 4 }, highlight: [3, 4], note: "x=-1: extend -- current_sum=3", runningValue: "3 / 4" },
      { pointers: { i: 5 }, highlight: [3, 4, 5], note: "x=2: extend -- current_sum=5, new best!", runningValue: "5 / 5" },
      { pointers: { i: 6 }, highlight: [3, 4, 5, 6], note: "x=1: extend -- current_sum=6, new best!", runningValue: "6 / 6" },
      { pointers: { i: 7 }, highlight: [3, 4, 5, 6, 7], note: "x=-5: current_sum drops to 1, best stays 6", runningValue: "1 / 6" },
      { pointers: { i: 8 }, highlight: [8], note: "x=4: better to start fresh -- current_sum=4, best stays 6", runningValue: "4 / 6" },
      { pointers: {}, highlight: [3, 4, 5, 6], note: "Done -- max subarray sum is 6, from the highlighted [4, -1, 2, 1]", runningValue: "-- / 6" },
    ],
  },

  ARRAYS_PREFIX_SUM: {
    type: "array",
    array: [1, 2, 3, 4, 5],
    valueLabel: "prefix sum so far",
    steps: [
      { pointers: { i: 0 }, highlight: [0], note: "prefix[1] = 0 + nums[0] = 1", runningValue: "1" },
      { pointers: { i: 1 }, highlight: [0, 1], note: "prefix[2] = 1 + nums[1] = 3", runningValue: "3" },
      { pointers: { i: 2 }, highlight: [0, 1, 2], note: "prefix[3] = 3 + nums[2] = 6", runningValue: "6" },
      { pointers: { i: 3 }, highlight: [0, 1, 2, 3], note: "prefix[4] = 6 + nums[3] = 10", runningValue: "10" },
      { pointers: { i: 4 }, highlight: [0, 1, 2, 3, 4], note: "prefix[5] = 10 + nums[4] = 15", runningValue: "15" },
      { pointers: {}, highlight: [1, 2, 3], note: "Now sum(1..3) = prefix[4] - prefix[1] = 10 - 1 = 9, no re-adding needed", runningValue: "9" },
    ],
  },

  HASHING: {
    type: "hashmap",
    steps: [
      { entries: [], note: "Start scanning nums=[2,7,11,15], target=9." },
      { entries: [{ key: 2, value: 0 }], note: "x=2 (index 0): need 9-2=7, not in map. Insert 2 -> 0." },
      { entries: [{ key: 2, value: 0 }], highlightKey: 2, note: "x=7 (index 1): need 9-7=2. 2 IS in the map! Match -- return [0, 1]." },
    ],
  },

  TWO_POINTER: {
    type: "array",
    array: [1, 2, 3, 4, 6],
    valueLabel: "sum",
    steps: [
      { pointers: { L: 0, R: 4 }, highlight: [0, 4], note: "sum = 1+6 = 7, too big -- move R left", runningValue: "7" },
      { pointers: { L: 0, R: 3 }, highlight: [0, 3], note: "sum = 1+4 = 5, too small -- move L right", runningValue: "5" },
      { pointers: { L: 1, R: 3 }, highlight: [1, 3], note: "sum = 2+4 = 6 -- match! Return indices [1, 3]", runningValue: "6" },
    ],
  },

  SLIDING_WINDOW: {
    type: "array",
    array: ["e", "c", "e", "b", "a"],
    valueLabel: "distinct chars / best length",
    steps: [
      { pointers: { L: 0, R: 0 }, highlight: [0], note: 'Window "e" -- 1 distinct char, valid', runningValue: "1 / 1" },
      { pointers: { L: 0, R: 1 }, highlight: [0, 1], note: 'Window "ec" -- 2 distinct, valid, best=2', runningValue: "2 / 2" },
      { pointers: { L: 0, R: 2 }, highlight: [0, 1, 2], note: 'Window "ece" -- still 2 distinct, best=3', runningValue: "2 / 3" },
      { pointers: { L: 0, R: 3 }, highlight: [0, 1, 2, 3], note: 'Window "eceb" -- 3 distinct, INVALID -- must shrink', runningValue: "3 / 3" },
      { pointers: { L: 1, R: 3 }, highlight: [1, 2, 3], note: 'Shrunk to "ceb" -- still 3 distinct, keep shrinking', runningValue: "3 / 3" },
      { pointers: { L: 2, R: 3 }, highlight: [2, 3], note: 'Shrunk to "eb" -- 2 distinct, valid again', runningValue: "2 / 3" },
      { pointers: { L: 2, R: 4 }, highlight: [2, 3, 4], note: 'Window "eba" -- 2 distinct, valid, best stays 3', runningValue: "2 / 3" },
    ],
  },

  BINARY_SEARCH: {
    type: "array",
    array: [1, 3, 5, 7, 9, 11],
    valueLabel: "nums[mid]",
    steps: [
      { pointers: { lo: 0, mid: 2, hi: 5 }, highlight: [2], note: "mid=2, nums[2]=5 < 7 -- search the right half", runningValue: "5" },
      { pointers: { lo: 3, mid: 4, hi: 5 }, highlight: [4], note: "mid=4, nums[4]=9 > 7 -- search the left half", eliminated: [0, 2], runningValue: "9" },
      { pointers: { lo: 3, mid: 3, hi: 3 }, highlight: [3], note: "mid=3, nums[3]=7 -- found! Return index 3", eliminated: [4, 5], runningValue: "7" },
    ],
  },

  STACK: {
    type: "stack",
    steps: [
      { stack: [], note: 'Scanning "([{}])" left to right', action: "none" },
      { stack: ["("], note: "'(' is an opener -- push it", action: "push" },
      { stack: ["(", "["], note: "'[' is an opener -- push it", action: "push" },
      { stack: ["(", "[", "{"], note: "'{' is an opener -- push it", action: "push" },
      { stack: ["(", "["], note: "'}' closes -- pop '{' and check it matches. It does.", action: "pop" },
      { stack: ["("], note: "']' closes -- pop '[' and check it matches. It does.", action: "pop" },
      { stack: [], note: "')' closes -- pop '(' and check it matches. It does.", action: "pop" },
      { stack: [], note: "Stack is empty at the end -- every bracket matched. Valid!", action: "none" },
    ],
  },

  RECURSION: {
    type: "stack",
    steps: [
      { stack: ["factorial(4)"], action: "push", note: "Call factorial(4) -- push it, waiting on factorial(3)." },
      { stack: ["factorial(4)", "factorial(3)"], action: "push", note: "factorial(4) calls factorial(3) -- push it, waiting." },
      { stack: ["factorial(4)", "factorial(3)", "factorial(2)"], action: "push", note: "factorial(3) calls factorial(2) -- push it, waiting." },
      { stack: ["factorial(4)", "factorial(3)", "factorial(2)", "factorial(1)"], action: "push", note: "factorial(2) calls factorial(1) -- base case! Returns 1 immediately." },
      { stack: ["factorial(4)", "factorial(3)", "factorial(2)"], action: "pop", note: "factorial(1) returned 1. Pop it -- factorial(2) computes 2*1=2." },
      { stack: ["factorial(4)", "factorial(3)"], action: "pop", note: "factorial(2) returned 2. Pop it -- factorial(3) computes 3*2=6." },
      { stack: ["factorial(4)"], action: "pop", note: "factorial(3) returned 6. Pop it -- factorial(4) computes 4*6=24." },
      { stack: [], action: "pop", note: "factorial(4) returned 24. Call stack empty -- done!" },
    ],
  },

  DP_BASICS: {
    type: "grid",
    rowLabels: ["ways(i)"],
    colLabels: ["1", "2", "3", "4", "5"],
    steps: [
      { grid: [[1, null, null, null, null]], current: [0, 0], note: "Base case: ways(1) = 1 way (a single 1-step)." },
      { grid: [[1, 2, null, null, null]], current: [0, 1], note: "Base case: ways(2) = 2 ways (1+1, or 2)." },
      { grid: [[1, 2, 3, null, null]], current: [0, 2], note: "ways(3) = ways(2) + ways(1) = 2 + 1 = 3." },
      { grid: [[1, 2, 3, 5, null]], current: [0, 3], note: "ways(4) = ways(3) + ways(2) = 3 + 2 = 5." },
      { grid: [[1, 2, 3, 5, 8]], current: [0, 4], note: "ways(5) = ways(4) + ways(3) = 5 + 3 = 8. Answer: 8 ways." },
    ],
  },

  HEAP: {
    type: "queue",
    frontLabel: "min",
    backLabel: "",
    steps: [
      { queue: [2, 3], action: "none", note: "Push first k=2 elements into a min-heap: {2,3}. Min=2." },
      { queue: [2, 3], action: "none", note: "Next: 1. Since 1 < heap min (2), it can't be a top-2 value -- skip." },
      { queue: [3, 5], action: "enqueue", note: "Next: 5. Since 5 > heap min (2), swap it in -- pop 2, push 5. Heap={3,5}, min=3." },
      { queue: [5, 6], action: "enqueue", note: "Next: 6. Since 6 > heap min (3), swap it in -- pop 3, push 6. Heap={5,6}, min=5." },
      { queue: [5, 6], action: "none", note: "Next: 4. Since 4 < heap min (5), skip." },
      { queue: [5, 6], action: "none", note: "Done. Heap={5,6} -- the minimum (5) is the 2nd largest element overall." },
    ],
  },

  STRINGS: {
    type: "array",
    array: ["r", "a", "c", "e", "a", "c", "a", "r"],
    valueLabel: "comparison",
    steps: [
      { pointers: { L: 0, R: 7 }, highlight: [0, 7], note: "'r' == 'r' -- match, keep going", runningValue: "match" },
      { pointers: { L: 1, R: 6 }, highlight: [1, 6], note: "'a' == 'a' -- match, keep going", runningValue: "match" },
      { pointers: { L: 2, R: 5 }, highlight: [2, 5], note: "'c' == 'c' -- match, keep going", runningValue: "match" },
      { pointers: { L: 3, R: 4 }, highlight: [3, 4], note: "'e' != 'a' -- mismatch! \"raceacar\" is not a palindrome.", runningValue: "mismatch" },
    ],
  },

  LINKED_LIST: {
    type: "linkedlist",
    steps: [
      {
        nodes: [{ id: "n1", val: 1, next: "n2" }, { id: "n2", val: 2, next: "n3" }, { id: "n3", val: 3, next: null }],
        pointers: { prev: null, curr: "n1" },
        note: "Start: prev=null, curr=1. Save curr.next (=2) before overwriting anything.",
      },
      {
        nodes: [{ id: "n1", val: 1, next: null }, { id: "n2", val: 2, next: "n3" }, { id: "n3", val: 3, next: null }],
        pointers: { prev: "n1", curr: "n2" },
        note: "1.next now points to prev (null). Advance: prev=1, curr=2.",
      },
      {
        nodes: [{ id: "n1", val: 1, next: null }, { id: "n2", val: 2, next: "n1" }, { id: "n3", val: 3, next: null }],
        pointers: { prev: "n2", curr: "n3" },
        note: "2.next now points to prev (1) -- the link reverses. Advance: prev=2, curr=3.",
      },
      {
        nodes: [{ id: "n1", val: 1, next: null }, { id: "n2", val: 2, next: "n1" }, { id: "n3", val: 3, next: "n2" }],
        pointers: { prev: "n3", curr: null },
        note: "3.next now points to prev (2). curr is null -- done. New head is 3: 3 → 2 → 1.",
      },
    ],
  },

  QUEUE_DEQUE: {
    type: "queue",
    steps: [
      { queue: [], action: "none", note: "Start: queue is empty." },
      { queue: ["A"], action: "enqueue", note: "Enqueue A (arrives first)." },
      { queue: ["A", "B"], action: "enqueue", note: "Enqueue B." },
      { queue: ["A", "B", "C"], action: "enqueue", note: "Enqueue C." },
      { queue: ["B", "C"], action: "dequeue", note: "Dequeue -- A leaves first (FIFO), since it arrived first." },
      { queue: ["C"], action: "dequeue", note: "Dequeue -- B leaves next." },
      { queue: [], action: "dequeue", note: "Dequeue -- C leaves. Order processed: A, B, C -- same as arrival order." },
    ],
  },

  TREES: {
    type: "tree",
    rootId: "n3",
    nodes: [
      { id: "n3", val: 3, left: "n9", right: "n20" },
      { id: "n9", val: 9, left: null, right: null },
      { id: "n20", val: 20, left: "n15", right: "n7" },
      { id: "n15", val: 15, left: null, right: null },
      { id: "n7", val: 7, left: null, right: null },
    ],
    steps: [
      { visited: [], current: "n3", note: "Preorder = root, left, right. Visit the root first: 3." },
      { visited: ["n3"], current: "n9", note: "Go left to 9 -- it's a leaf, nothing further down this branch." },
      { visited: ["n3", "n9"], current: "n20", note: "Back up, go right from 3 to 20." },
      { visited: ["n3", "n9", "n20"], current: "n15", note: "From 20, go left to 15." },
      { visited: ["n3", "n9", "n20", "n15"], current: "n7", note: "Back up, go right from 20 to 7." },
      { visited: ["n3", "n9", "n20", "n15", "n7"], current: null, note: "Traversal complete: 3, 9, 20, 15, 7." },
    ],
  },

  BST: {
    type: "tree",
    rootId: "n8",
    nodes: [
      { id: "n8", val: 8, left: "n3", right: "n10" },
      { id: "n3", val: 3, left: "n1", right: "n6" },
      { id: "n10", val: 10, left: null, right: "n14" },
      { id: "n1", val: 1, left: null, right: null },
      { id: "n6", val: 6, left: "n4", right: "n7" },
      { id: "n14", val: 14, left: null, right: null },
      { id: "n4", val: 4, left: null, right: null },
      { id: "n7", val: 7, left: null, right: null },
    ],
    steps: [
      { visited: [], current: "n8", note: "Searching for 6. Start at root: 8. Is 6 < 8? Yes -- go left." },
      { visited: ["n8"], current: "n3", note: "At 3. Is 6 > 3? Yes -- go right (everything right of 3 is bigger)." },
      { visited: ["n8", "n3"], current: "n6", note: "At 6 -- found it! Two comparisons found the target in this 8-node tree." },
    ],
  },

  TRIE: {
    type: "tree",
    rootId: "root",
    nodes: [
      { id: "root", val: "•", left: "c", right: null },
      { id: "c", val: "c", left: "a", right: null },
      { id: "a", val: "a", left: "r", right: "t" },
      { id: "r", val: "r*", left: null, right: null },
      { id: "t", val: "t*", left: null, right: null },
    ],
    steps: [
      { visited: [], current: "root", note: "Insert 'car'. Start at the root." },
      { visited: ["root"], current: "c", note: "Follow/create branch 'c'." },
      { visited: ["root", "c"], current: "a", note: "Follow/create branch 'a'." },
      { visited: ["root", "c", "a"], current: "r", note: "Create branch 'r', mark it as a word end: 'car' is now stored." },
      { visited: ["root", "c", "a", "r"], current: "t", note: "Insert 'cat': reuse the existing 'c'→'a' path, branch to new 't', mark word end: 'cat' stored." },
      { visited: ["root", "c", "a", "r", "t"], current: null, note: "The trie now stores both 'car' and 'cat', sharing the 'ca' prefix path." },
    ],
  },

  GRAPHS: {
    type: "graph",
    nodes: [{ id: "0", label: 0 }, { id: "1", label: 1 }, { id: "2", label: 2 }, { id: "3", label: 3 }],
    edges: [{ from: "0", to: "1" }, { from: "0", to: "2" }, { from: "1", to: "3" }, { from: "2", to: "3" }],
    steps: [
      { visited: [], current: "0", frontier: ["0"], note: "Start BFS at node 0. Add it to the queue." },
      { visited: ["0"], current: "0", frontier: ["1", "2"], note: "Visit 0. Enqueue its neighbors 1 and 2." },
      { visited: ["0", "1"], current: "1", frontier: ["2", "3"], note: "Dequeue 1, visit it. Enqueue its unvisited neighbor 3." },
      { visited: ["0", "1", "2"], current: "2", frontier: ["3"], note: "Dequeue 2, visit it. Its neighbor 3 is already queued." },
      { visited: ["0", "1", "2", "3"], current: "3", frontier: [], note: "Dequeue 3, visit it. BFS complete -- order: 0, 1, 2, 3." },
    ],
  },

  GREEDY: {
    type: "array",
    array: ["[1,11]", "[2,12]", "[11,22]", "[1,100]"],
    valueLabel: "picked count",
    steps: [
      { pointers: {}, highlight: [0], note: "Sorted by END time. Take [1,11] first -- count=1, last_end=11.", runningValue: "1" },
      { pointers: {}, highlight: [1], note: "[2,12] starts at 2, before last_end=11 -- overlaps, skip.", runningValue: "1" },
      { pointers: {}, highlight: [0, 2], note: "[11,22] starts at 11 >= last_end=11 -- take it! count=2, last_end=22.", runningValue: "2" },
      { pointers: {}, highlight: [3], note: "[1,100] starts at 1, before last_end=22 -- overlaps, skip.", runningValue: "2" },
      { pointers: {}, highlight: [0, 2], note: "Done. Max non-overlapping intervals = 2: [1,11] and [11,22].", runningValue: "2" },
    ],
  },

  BACKTRACKING: {
    type: "tree",
    rootId: "root",
    nodes: [
      { id: "root", val: "{}", left: "n1", right: "n2" },
      { id: "n1", val: "{1}", left: "n1a", right: "n1b" },
      { id: "n2", val: "{}", left: "n2a", right: "n2b" },
      { id: "n1a", val: "{1,2}", left: null, right: null },
      { id: "n1b", val: "{1}", left: null, right: null },
      { id: "n2a", val: "{2}", left: null, right: null },
      { id: "n2b", val: "{}", left: null, right: null },
    ],
    steps: [
      { visited: [], current: "root", note: "Start with the empty subset {}." },
      { visited: ["root"], current: "n1", note: "Choice: include 1 -> {1}." },
      { visited: ["root", "n1"], current: "n1a", note: "Choice: include 2 -> {1,2}. Record it -- one full subset found." },
      { visited: ["root", "n1", "n1a"], current: "n1b", note: "Backtrack, choice: exclude 2 -> stays {1}. Record it." },
      { visited: ["root", "n1", "n1a", "n1b"], current: "n2", note: "Backtrack to root, choice: exclude 1 -> {}." },
      { visited: ["root", "n1", "n1a", "n1b", "n2"], current: "n2a", note: "Choice: include 2 -> {2}. Record it." },
      { visited: ["root", "n1", "n1a", "n1b", "n2", "n2a"], current: "n2b", note: "Choice: exclude 2 -> {}. Record it. All 4 subsets found." },
    ],
  },

  BIT_MANIPULATION: {
    type: "bits",
    steps: [
      { bits: [0, 0, 0, 0], decimal: 0, note: "Start: result = 0000 (0)." },
      { bits: [0, 1, 0, 0], decimal: 4, highlight: [1], note: "XOR with 4 (0100): 0000 ^ 0100 = 0100." },
      { bits: [0, 1, 0, 1], decimal: 5, highlight: [3], note: "XOR with 1 (0001): 0100 ^ 0001 = 0101." },
      { bits: [0, 1, 1, 1], decimal: 7, highlight: [2], note: "XOR with 2 (0010): 0101 ^ 0010 = 0111." },
      { bits: [0, 1, 1, 0], decimal: 6, highlight: [3], note: "XOR with 1 (0001): 0111 ^ 0001 = 0110." },
      { bits: [0, 1, 0, 0], decimal: 4, highlight: [2], note: "XOR with 2 (0010): 0110 ^ 0010 = 0100." },
      { bits: [0, 1, 0, 0], decimal: 4, note: "All elements processed. Every paired value canceled out -- 4 is the single number." },
    ],
  },

  UNION_FIND: {
    type: "graph",
    nodes: [{ id: "0", label: 0 }, { id: "1", label: 1 }, { id: "2", label: 2 }, { id: "3", label: 3 }, { id: "4", label: 4 }],
    edges: [{ from: "0", to: "1" }, { from: "1", to: "2" }, { from: "3", to: "4" }],
    steps: [
      { groups: { "0": 0, "1": 1, "2": 2, "3": 3, "4": 4 }, note: "Start: every node is its own group." },
      { groups: { "0": 0, "1": 0, "2": 2, "3": 3, "4": 4 }, current: "1", note: "Union(0,1): merge into one group." },
      { groups: { "0": 0, "1": 0, "2": 0, "3": 3, "4": 4 }, current: "2", note: "Union(1,2): 2 joins the same group as 0 and 1." },
      { groups: { "0": 0, "1": 0, "2": 0, "3": 3, "4": 3 }, current: "4", note: "Union(3,4): merge into a second group." },
      { groups: { "0": 0, "1": 0, "2": 0, "3": 3, "4": 3 }, note: "Done. Two groups remain: {0,1,2} and {3,4} -- 2 connected components." },
    ],
  },

  TOPOLOGICAL_SORT: {
    type: "graph",
    nodes: [{ id: "0", label: 0 }, { id: "1", label: 1 }, { id: "2", label: 2 }, { id: "3", label: 3 }],
    edges: [
      { from: "0", to: "1", directed: true }, { from: "0", to: "2", directed: true },
      { from: "1", to: "3", directed: true }, { from: "2", to: "3", directed: true },
    ],
    steps: [
      { visited: [], note: "In-degrees: 0:0, 1:1, 2:1, 3:2. Start with the only in-degree-0 node: 0." },
      { visited: ["0"], current: "0", note: "Process 0. Decrement in-degree of 1 and 2 -- both now 0, ready." },
      { visited: ["0", "1"], current: "1", frontier: ["2"], note: "Process 1. Decrement in-degree of 3 -- now 1, not ready yet." },
      { visited: ["0", "1", "2"], current: "2", note: "Process 2. Decrement in-degree of 3 -- now 0, ready!" },
      { visited: ["0", "1", "2", "3"], current: "3", note: "Process 3. All 4 processed -- valid order: 0, 1, 2, 3. No cycle." },
    ],
  },

  DIJKSTRA: {
    type: "graph",
    nodes: [{ id: "0", label: 0 }, { id: "1", label: 1 }, { id: "2", label: 2 }],
    edges: [
      { from: "0", to: "1", weight: 4, directed: true }, { from: "0", to: "2", weight: 1, directed: true },
      { from: "2", to: "1", weight: 1, directed: true },
    ],
    steps: [
      { distances: { "0": 0, "1": "∞", "2": "∞" }, current: "0", note: "Start at 0, dist=0. All others unknown." },
      { distances: { "0": 0, "1": 4, "2": 1 }, current: "0", note: "Relax 0's neighbors: dist[1]=4, dist[2]=1." },
      { distances: { "0": 0, "1": 4, "2": 1 }, current: "2", visited: ["0"], note: "Pop closest unvisited: 2 (dist=1). Finalize it." },
      { distances: { "0": 0, "1": 2, "2": 1 }, current: "2", visited: ["0", "2"], note: "Relax 2's neighbor 1: 1+1=2 < 4 -- update dist[1]=2!" },
      { distances: { "0": 0, "1": 2, "2": 1 }, current: "1", visited: ["0", "2", "1"], note: "Pop closest: 1 (dist=2). Done -- shortest path to 1 goes via 2." },
    ],
  },

  DP_KNAPSACK: {
    type: "grid",
    rowLabels: ["none", "+(w1,v1)", "+(w3,v4)", "+(w4,v5)"],
    colLabels: ["0", "1", "2", "3", "4", "5"],
    steps: [
      { grid: [[0, 0, 0, 0, 0, 0], [null, null, null, null, null, null], [null, null, null, null, null, null], [null, null, null, null, null, null]], current: [0, 5], note: "Base row: 0 items -> 0 value at any capacity." },
      { grid: [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [null, null, null, null, null, null], [null, null, null, null, null, null]], current: [1, 5], note: "Item (w1,v1) fits in any capacity >= 1, adding value 1." },
      { grid: [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 4, 5, 5], [null, null, null, null, null, null]], current: [2, 5], note: "Item (w3,v4): at capacity 5, best = max(skip=1, take 4+row1[2]=5) = 5." },
      { grid: [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 4, 5, 5], [0, 1, 1, 4, 5, 6]], current: [3, 5], note: "Item (w4,v5): at capacity 5, best = max(skip=5, take 5+row2[1]=6) = 6. Answer: 6." },
    ],
  },

  DP_STRING: {
    type: "grid",
    rowLabels: ["", "a", "b", "c", "d", "e"],
    colLabels: ["", "a", "c", "e"],
    steps: [
      { grid: [[0, 0, 0, 0], [null, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]], current: [0, 0], note: "Row for empty text1 prefix: always 0 (nothing to match)." },
      { grid: [[0, 0, 0, 0], [0, 1, 1, 1], [null, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]], current: [1, 3], note: "Row 'a': matches text2's 'a' at j=1, extending to 1; carries forward after." },
      { grid: [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [null, null, null, null], [null, null, null, null], [null, null, null, null]], current: [2, 3], note: "Row 'b': no match, so each cell carries the best from above or the left." },
      { grid: [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [null, null, null, null], [null, null, null, null]], current: [3, 2], note: "Row 'c': matches text2's 'c' at j=2 -- diagonal+1 = 1+1 = 2." },
      { grid: [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2], [null, null, null, null]], current: [4, 2], note: "Row 'd': no match, carries forward the best values." },
      { grid: [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 3]], current: [5, 3], note: "Row 'e': matches text2's 'e' at j=3 -- diagonal+1 = 2+1 = 3. Final LCS length: 3 ('ace')." },
    ],
  },

  ADVANCED_PATTERNS: {
    type: "array",
    array: ["t=0 start", "t=5 start", "t=10 end", "t=15 start", "t=20 end", "t=30 end"],
    valueLabel: "active meetings",
    steps: [
      { pointers: {}, highlight: [0], note: "t=0: a meeting starts.", runningValue: "active=1, max=1" },
      { pointers: {}, highlight: [0, 1], note: "t=5: another starts.", runningValue: "active=2, max=2" },
      { pointers: {}, highlight: [1], note: "t=10: a meeting ends.", runningValue: "active=1, max=2" },
      { pointers: {}, highlight: [1, 3], note: "t=15: another starts.", runningValue: "active=2, max=2" },
      { pointers: {}, highlight: [3], note: "t=20: a meeting ends.", runningValue: "active=1, max=2" },
      { pointers: {}, highlight: [], note: "t=30: last meeting ends. Peak simultaneous meetings = 2 -- need 2 rooms.", runningValue: "active=0, max=2" },
    ],
  },
};
