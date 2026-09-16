"""
Seed problem library.

Honesty note (spec section 87 / 81): this is a genuine, hand-authored starter
set -- not a claim of "250+ problems". Each problem carries a real
`reference_solution_python`, which `seed_all.py` actually *executes* against
`test_cases[].args` to compute `expected_output` at seed time. This means test
data can never silently drift from the reference implementation, and nothing
here is a fabricated expected value.

Difficulty ratings (concept/implementation/reasoning/pattern, each 1-5) are
authored estimates, not measured -- flagged here rather than presented as
empirically derived.
"""

PROBLEMS = [
    {
        "slug": "find-min-max",
        "title": "Track the Running Minimum and Maximum",
        "primary_skill": "ARRAYS_TRAVERSAL",
        "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a non-empty list of integers `nums`, return `[min_value, max_value]` found in a single pass.",
        "constraints": "1 <= len(nums) <= 10^5, -10^9 <= nums[i] <= 10^9",
        "examples": [{"input": "[3,1,4,1,5,9,2,6]", "output": "[1,9]", "explanation": "1 is smallest, 9 is largest."}],
        "function_name": "find_min_max",
        "starter_code": "def find_min_max(nums):\n    # return [min_value, max_value]\n    pass\n",
        "reference_solution": (
            "def find_min_max(nums):\n"
            "    lo, hi = nums[0], nums[0]\n"
            "    for x in nums[1:]:\n"
            "        if x < lo:\n            lo = x\n"
            "        if x > hi:\n            hi = x\n"
            "    return [lo, hi]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[3, 1, 4, 1, 5, 9, 2, 6]], "hidden": False, "explanation": "mixed values"},
            {"args": [[5]], "hidden": False, "explanation": "single element"},
            {"args": [[-3, -1, -7, -2]], "hidden": False, "explanation": "all negative"},
            {"args": [[2, 2, 2]], "hidden": True, "explanation": "all equal"},
            {"args": [[100, -100, 0, 50, -50]], "hidden": True, "explanation": "wide spread"},
        ],
        "hints": [
            "You don't need to sort the array -- one pass is enough.",
            "Keep two running variables, updating them as you see each element.",
            "Initialize both to `nums[0]`, then compare every later element against both.",
        ],
    },
    {
        "slug": "max-subarray-sum",
        "title": "Maximum Subarray Sum (Kadane's Technique)",
        "primary_skill": "ARRAYS_TRAVERSAL",
        "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an integer array `nums`, find the contiguous subarray with the largest sum and return that sum.",
        "constraints": "1 <= len(nums) <= 10^5",
        "examples": [{"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "[4,-1,2,1] sums to 6."}],
        "function_name": "max_subarray_sum",
        "starter_code": "def max_subarray_sum(nums):\n    pass\n",
        "reference_solution": (
            "def max_subarray_sum(nums):\n"
            "    best = nums[0]\n    cur = nums[0]\n"
            "    for x in nums[1:]:\n        cur = max(x, cur + x)\n        best = max(best, cur)\n"
            "    return best\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "hidden": False, "explanation": "classic case"},
            {"args": [[1]], "hidden": False, "explanation": "single positive"},
            {"args": [[-1, -2, -3]], "hidden": False, "explanation": "all negative -- must pick least-negative"},
            {"args": [[5, 4, -1, 7, 8]], "hidden": True, "explanation": "whole array is best"},
            {"args": [[-2, -1]], "hidden": True, "explanation": "two negatives"},
        ],
        "hints": [
            "Brute force checks every subarray in O(n^2) -- constraints need O(n).",
            "At each position, decide: extend the current subarray, or start fresh here?",
            "`cur = max(x, cur + x)` is the whole trick; track the best `cur` seen.",
        ],
    },
    {
        "slug": "range-sum-queries",
        "title": "Answer Range Sum Queries",
        "primary_skill": "ARRAYS_PREFIX_SUM",
        "pattern_skills": ["ARRAYS_PREFIX_SUM"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": (
            "Given `nums` and a list of inclusive range `queries` (each `[l, r]`), return a list of the sum of "
            "`nums[l..r]` for every query."
        ),
        "constraints": "1 <= len(nums) <= 10^5, 1 <= len(queries) <= 10^4",
        "examples": [{"input": "nums=[1,2,3,4,5], queries=[[0,2],[1,3]]", "output": "[6,9]", "explanation": "1+2+3=6, 2+3+4=9"}],
        "function_name": "range_sums",
        "starter_code": "def range_sums(nums, queries):\n    pass\n",
        "reference_solution": (
            "def range_sums(nums, queries):\n"
            "    prefix = [0] * (len(nums) + 1)\n"
            "    for i, x in enumerate(nums):\n        prefix[i + 1] = prefix[i] + x\n"
            "    return [prefix[r + 1] - prefix[l] for l, r in queries]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5], [[0, 2], [1, 3], [0, 4]]], "hidden": False, "explanation": "several ranges"},
            {"args": [[10, -2, 3], [[0, 0], [0, 2]]], "hidden": False, "explanation": "includes a negative"},
            {"args": [[1, 1, 1, 1], [[1, 2]]], "hidden": True, "explanation": "single query"},
        ],
        "hints": [
            "Recomputing each range sum from scratch is O(n) per query -- too slow for many queries.",
            "Precompute `prefix[i]` = sum of the first i elements, once.",
            "`sum(l, r) = prefix[r+1] - prefix[l]` answers any query in O(1).",
        ],
    },
    {
        "slug": "two-sum-indices",
        "title": "Two Sum -- Return the Indices",
        "primary_skill": "HASHING",
        "pattern_skills": ["HASHING"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given `nums` and `target`, return the indices `[i, j]` (i < j) of the two numbers that add up to target.",
        "constraints": "2 <= len(nums) <= 10^5, exactly one valid answer exists",
        "examples": [{"input": "nums=[2,7,11,15], target=9", "output": "[0,1]", "explanation": "2+7=9"}],
        "function_name": "two_sum",
        "starter_code": "def two_sum(nums, target):\n    pass\n",
        "reference_solution": (
            "def two_sum(nums, target):\n"
            "    seen = {}\n"
            "    for i, x in enumerate(nums):\n"
            "        need = target - x\n"
            "        if need in seen:\n            return [seen[need], i]\n"
            "        seen[x] = i\n"
            "    return [-1, -1]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 7, 11, 15], 9], "hidden": False, "explanation": "basic case"},
            {"args": [[3, 2, 4], 6], "hidden": False, "explanation": "answer not at the start"},
            {"args": [[3, 3], 6], "hidden": True, "explanation": "duplicate values"},
            {"args": [[1, 2, 3, 4, 5], 9], "hidden": True, "explanation": "answer near the end"},
        ],
        "hints": [
            "Checking every pair is O(n^2). What if you could look up a value in O(1)?",
            "As you scan, ask: have I already seen `target - current` before?",
            "Store each value's index in a hashmap as you go; check before you insert.",
        ],
    },
    {
        "slug": "count-anagram-groups",
        "title": "Count Anagram Groups",
        "primary_skill": "HASHING",
        "pattern_skills": ["HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a list of lowercase words, return the number of distinct anagram groups.",
        "constraints": "0 <= len(words) <= 10^4",
        "examples": [{"input": '["eat","tea","tan","ate","nat","bat"]', "output": "3", "explanation": "{eat,tea,ate}, {tan,nat}, {bat}"}],
        "function_name": "count_anagram_groups",
        "starter_code": "def count_anagram_groups(words):\n    pass\n",
        "reference_solution": (
            "def count_anagram_groups(words):\n"
            "    groups = set()\n"
            "    for w in words:\n        groups.add(''.join(sorted(w)))\n"
            "    return len(groups)\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [["eat", "tea", "tan", "ate", "nat", "bat"]], "hidden": False, "explanation": "three groups"},
            {"args": [["a"]], "hidden": False, "explanation": "single word"},
            {"args": [["abc", "cba", "bac", "xyz"]], "hidden": True, "explanation": "two groups"},
            {"args": [[]], "hidden": True, "explanation": "empty input"},
        ],
        "hints": [
            "Two words are anagrams if their sorted characters are identical.",
            "Use each word's sorted-character signature as a hashable key.",
            "Count distinct signatures with a set.",
        ],
    },
    {
        "slug": "two-sum-sorted",
        "title": "Two Sum on a Sorted Array",
        "primary_skill": "TWO_POINTER",
        "pattern_skills": ["TWO_POINTER"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given an ascending-sorted array `nums` and `target`, return indices `[i, j]` (i < j) of a pair summing to target using O(1) extra space.",
        "constraints": "2 <= len(nums) <= 10^5, nums is sorted ascending",
        "examples": [{"input": "nums=[1,2,3,4,6], target=6", "output": "[1,3]", "explanation": "2+4=6"}],
        "function_name": "two_sum_sorted",
        "starter_code": "def two_sum_sorted(nums, target):\n    pass\n",
        "reference_solution": (
            "def two_sum_sorted(nums, target):\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo < hi:\n"
            "        s = nums[lo] + nums[hi]\n"
            "        if s == target:\n            return [lo, hi]\n"
            "        elif s < target:\n            lo += 1\n"
            "        else:\n            hi -= 1\n"
            "    return [-1, -1]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 6], 6], "hidden": False, "explanation": "basic case"},
            {"args": [[2, 7, 11, 15], 9], "hidden": False, "explanation": "answer at the start"},
            {"args": [[1, 2, 3], 10], "hidden": True, "explanation": "no valid pair"},
            {"args": [[-3, -1, 0, 2, 5], 4], "hidden": True, "explanation": "negative numbers"},
        ],
        "hints": [
            "Hashing solves this in O(n) too -- but can you use the fact that it's sorted to use O(1) space?",
            "Start pointers at both ends. If the sum is too big, which pointer should move?",
            "sum < target -> move left pointer right. sum > target -> move right pointer left.",
        ],
    },
    {
        "slug": "max-sum-fixed-window",
        "title": "Maximum Sum of a Fixed-Size Window",
        "primary_skill": "SLIDING_WINDOW",
        "pattern_skills": ["SLIDING_WINDOW"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given `nums` and an integer `k`, return the maximum sum of any contiguous subarray of length exactly k.",
        "constraints": "1 <= k <= len(nums) <= 10^5",
        "examples": [{"input": "nums=[2,1,5,1,3,2], k=3", "output": "9", "explanation": "[5,1,3] sums to 9"}],
        "function_name": "max_sum_fixed_window",
        "starter_code": "def max_sum_fixed_window(nums, k):\n    pass\n",
        "reference_solution": (
            "def max_sum_fixed_window(nums, k):\n"
            "    window = sum(nums[:k])\n    best = window\n"
            "    for i in range(k, len(nums)):\n"
            "        window += nums[i] - nums[i - k]\n        best = max(best, window)\n"
            "    return best\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 1, 5, 1, 3, 2], 3], "hidden": False, "explanation": "basic case"},
            {"args": [[1, 1, 1, 1], 2], "hidden": False, "explanation": "uniform values"},
            {"args": [[5, -1, -2, 10], 2], "hidden": True, "explanation": "negative values inside window"},
            {"args": [[3, 3, 3], 1], "hidden": True, "explanation": "window size 1"},
        ],
        "hints": [
            "Recomputing the sum of every window from scratch is O(n*k).",
            "What changes between one window and the next? Only one element leaves, one enters.",
            "Slide: `window += nums[right] - nums[right - k]`.",
        ],
    },
    {
        "slug": "longest-substring-k-distinct",
        "title": "Longest Substring with At Most K Distinct Characters",
        "primary_skill": "SLIDING_WINDOW",
        "pattern_skills": ["SLIDING_WINDOW", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 4,
        "statement": "Given a string `s` and an integer `k`, return the length of the longest substring containing at most `k` distinct characters.",
        "constraints": "0 <= len(s) <= 10^5, 0 <= k <= 26",
        "examples": [{"input": 's="eceba", k=2', "output": "3", "explanation": "\"ece\" has 2 distinct chars, length 3"}],
        "function_name": "longest_substring_k_distinct",
        "starter_code": "def longest_substring_k_distinct(s, k):\n    pass\n",
        "reference_solution": (
            "def longest_substring_k_distinct(s, k):\n"
            "    if k == 0:\n        return 0\n"
            "    count = {}\n    left = 0\n    best = 0\n"
            "    for right, ch in enumerate(s):\n"
            "        count[ch] = count.get(ch, 0) + 1\n"
            "        while len(count) > k:\n"
            "            count[s[left]] -= 1\n"
            "            if count[s[left]] == 0:\n                del count[s[left]]\n"
            "            left += 1\n"
            "        best = max(best, right - left + 1)\n"
            "    return best\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["eceba", 2], "hidden": False, "explanation": "classic case"},
            {"args": ["aa", 1], "hidden": False, "explanation": "single distinct char allowed"},
            {"args": ["a", 0], "hidden": True, "explanation": "zero distinct chars allowed"},
            {"args": ["aabbcc", 2], "hidden": True, "explanation": "even distribution"},
        ],
        "hints": [
            "This is a *variable* window -- it grows and shrinks.",
            "Track character counts in the current window with a hashmap; the window is valid while distinct count <= k.",
            "When the window becomes invalid (too many distinct chars), shrink from the left until it's valid again.",
        ],
    },
    {
        "slug": "binary-search-basic",
        "title": "Binary Search",
        "primary_skill": "BINARY_SEARCH",
        "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given an ascending-sorted array of distinct integers `nums` and a `target`, return its index, or -1 if absent.",
        "constraints": "1 <= len(nums) <= 10^5",
        "examples": [{"input": "nums=[1,3,5,7,9,11], target=7", "output": "3", "explanation": "nums[3] == 7"}],
        "function_name": "binary_search",
        "starter_code": "def binary_search(nums, target):\n    pass\n",
        "reference_solution": (
            "def binary_search(nums, target):\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] == target:\n            return mid\n"
            "        elif nums[mid] < target:\n            lo = mid + 1\n"
            "        else:\n            hi = mid - 1\n"
            "    return -1\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[1, 3, 5, 7, 9, 11], 7], "hidden": False, "explanation": "target present"},
            {"args": [[1, 3, 5, 7, 9, 11], 2], "hidden": False, "explanation": "target absent"},
            {"args": [[1], 1], "hidden": True, "explanation": "single element"},
            {"args": [[-5, -1, 0, 3, 8], 8], "hidden": True, "explanation": "target at the end"},
        ],
        "hints": [
            "A linear scan is O(n); the sorted order lets you do better.",
            "At each step, compare the target against the middle element to discard half the array.",
            "Keep `lo`/`hi` bounds and stop when they cross.",
        ],
    },
    {
        "slug": "first-true-index",
        "title": "Binary Search on an Answer Space",
        "primary_skill": "BINARY_SEARCH",
        "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": (
            "`flags` is a list of 0s followed by 1s (monotonic). Return the index of the first 1, or -1 if there is none."
        ),
        "constraints": "0 <= len(flags) <= 10^5, flags is monotonic (all 0s before all 1s)",
        "examples": [{"input": "[0,0,0,1,1]", "output": "3", "explanation": "first 1 is at index 3"}],
        "function_name": "first_true_index",
        "starter_code": "def first_true_index(flags):\n    pass\n",
        "reference_solution": (
            "def first_true_index(flags):\n"
            "    lo, hi = 0, len(flags) - 1\n    ans = -1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if flags[mid] == 1:\n            ans = mid\n            hi = mid - 1\n"
            "        else:\n            lo = mid + 1\n"
            "    return ans\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[0, 0, 0, 1, 1]], "hidden": False, "explanation": "basic case"},
            {"args": [[1, 1, 1]], "hidden": False, "explanation": "all true"},
            {"args": [[0, 0, 0]], "hidden": True, "explanation": "all false"},
            {"args": [[0, 1]], "hidden": True, "explanation": "boundary of size 2"},
        ],
        "hints": [
            "This isn't 'search for a value' -- it's 'search for the boundary where a condition flips'.",
            "The condition `flags[i] == 1` is monotonic, which is exactly what makes binary search valid here.",
            "When you find a 1, it might not be the *first* one -- keep searching left, remembering the best answer so far.",
        ],
    },
    {
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "primary_skill": "STACK",
        "pattern_skills": ["STACK"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 2,
        "statement": "Given a string `s` containing only `()[]{}`, return True if the brackets are balanced and correctly nested.",
        "constraints": "0 <= len(s) <= 10^4",
        "examples": [{"input": '"([{}])"', "output": "true", "explanation": "correctly nested"}],
        "function_name": "is_valid_parentheses",
        "starter_code": "def is_valid_parentheses(s):\n    pass\n",
        "reference_solution": (
            "def is_valid_parentheses(s):\n"
            "    pairs = {')': '(', ']': '[', '}': '{'}\n    stack = []\n"
            "    for ch in s:\n"
            "        if ch in '([{':\n            stack.append(ch)\n"
            "        else:\n"
            "            if not stack or stack.pop() != pairs[ch]:\n                return False\n"
            "    return len(stack) == 0\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["()[]{}"], "hidden": False, "explanation": "all balanced"},
            {"args": ["(]"], "hidden": False, "explanation": "mismatched pair"},
            {"args": [""], "hidden": True, "explanation": "empty string"},
            {"args": ["((("], "hidden": True, "explanation": "unclosed brackets"},
        ],
        "hints": [
            "Think about what must be true of the *most recently opened, still-unclosed* bracket.",
            "A stack naturally tracks 'most recent unmatched item'.",
            "Push openers; on a closer, pop and check it matches -- and the stack must be empty at the end.",
        ],
    },
    {
        "slug": "daily-wait-days",
        "title": "Days Until a Warmer Temperature",
        "primary_skill": "STACK",
        "pattern_skills": ["STACK"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 4,
        "statement": (
            "Given daily temperatures `temps`, return a list where `answer[i]` is the number of days until a warmer "
            "temperature; 0 if there is none."
        ),
        "constraints": "1 <= len(temps) <= 10^5",
        "examples": [{"input": "[73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]", "explanation": "classic monotonic-stack case"}],
        "function_name": "daily_wait_days",
        "starter_code": "def daily_wait_days(temps):\n    pass\n",
        "reference_solution": (
            "def daily_wait_days(temps):\n"
            "    res = [0] * len(temps)\n    stack = []\n"
            "    for i, t in enumerate(temps):\n"
            "        while stack and temps[stack[-1]] < t:\n"
            "            j = stack.pop()\n            res[j] = i - j\n"
            "        stack.append(i)\n"
            "    return res\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[73, 74, 75, 71, 69, 72, 76, 73]], "hidden": False, "explanation": "classic case"},
            {"args": [[30, 40, 50, 60]], "hidden": False, "explanation": "strictly increasing"},
            {"args": [[90, 60, 30]], "hidden": True, "explanation": "strictly decreasing -- never warmer"},
        ],
        "hints": [
            "Checking every future day for each day is O(n^2).",
            "Keep a stack of day-indices whose warmer day hasn't been found yet.",
            "When today is warmer than the stack's top day, that's the answer for the top -- pop and record it.",
        ],
    },
    {
        "slug": "factorial-recursive",
        "title": "Factorial via Recursion",
        "primary_skill": "RECURSION",
        "pattern_skills": ["RECURSION"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Return n! (factorial of n) using recursion, not a loop.",
        "constraints": "0 <= n <= 15",
        "examples": [{"input": "5", "output": "120", "explanation": "5*4*3*2*1"}],
        "function_name": "factorial",
        "starter_code": "def factorial(n):\n    pass\n",
        "reference_solution": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n - 1)\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [0], "hidden": False, "explanation": "base case"},
            {"args": [1], "hidden": False, "explanation": "base case"},
            {"args": [5], "hidden": False, "explanation": "typical case"},
            {"args": [7], "hidden": True, "explanation": "larger input"},
        ],
        "hints": [
            "What is n! in terms of (n-1)!?",
            "Identify the base case first: what's 0! or 1!?",
            "`factorial(n) = n * factorial(n-1)`, with `factorial(0) = factorial(1) = 1`.",
        ],
    },
    {
        "slug": "fibonacci-memo",
        "title": "Nth Fibonacci Number (Memoized)",
        "primary_skill": "RECURSION",
        "pattern_skills": ["RECURSION", "DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Return the nth Fibonacci number (fib(0)=0, fib(1)=1) in O(n) time using memoized recursion.",
        "constraints": "0 <= n <= 30",
        "examples": [{"input": "10", "output": "55", "explanation": "0,1,1,2,3,5,8,13,21,34,55"}],
        "function_name": "fibonacci",
        "starter_code": "def fibonacci(n):\n    pass\n",
        "reference_solution": (
            "def fibonacci(n):\n"
            "    memo = {}\n"
            "    def helper(k):\n"
            "        if k <= 1:\n            return k\n"
            "        if k in memo:\n            return memo[k]\n"
            "        memo[k] = helper(k - 1) + helper(k - 2)\n        return memo[k]\n"
            "    return helper(n)\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [0], "hidden": False, "explanation": "base case"},
            {"args": [1], "hidden": False, "explanation": "base case"},
            {"args": [10], "hidden": False, "explanation": "typical case"},
            {"args": [20], "hidden": True, "explanation": "naive recursion would be exponential here"},
        ],
        "hints": [
            "Plain recursive Fibonacci recomputes the same subproblems exponentially many times.",
            "Cache results you've already computed so each subproblem is solved once.",
            "A dict keyed by `n` mapping to its Fibonacci value is enough.",
        ],
    },
    {
        "slug": "climb-stairs",
        "title": "Climbing Stairs",
        "primary_skill": "DP_BASICS",
        "pattern_skills": ["DP_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "You climb a staircase of `n` steps, taking 1 or 2 steps at a time. Return the number of distinct ways to reach the top.",
        "constraints": "1 <= n <= 45",
        "examples": [{"input": "4", "output": "5", "explanation": "1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2"}],
        "function_name": "climb_stairs",
        "starter_code": "def climb_stairs(n):\n    pass\n",
        "reference_solution": (
            "def climb_stairs(n):\n"
            "    if n <= 2:\n        return n\n"
            "    a, b = 1, 2\n"
            "    for _ in range(3, n + 1):\n        a, b = b, a + b\n"
            "    return b\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [1], "hidden": False, "explanation": "base case"},
            {"args": [2], "hidden": False, "explanation": "base case"},
            {"args": [5], "hidden": False, "explanation": "typical case"},
            {"args": [10], "hidden": True, "explanation": "larger input"},
        ],
        "hints": [
            "State: the number of ways to reach step `i` depends only on smaller steps.",
            "Transition: `ways(i) = ways(i-1) + ways(i-2)` -- you arrive at step i either from i-1 or i-2.",
            "Base cases: `ways(1) = 1`, `ways(2) = 2`.",
        ],
    },
    {
        "slug": "house-robber",
        "title": "House Robber",
        "primary_skill": "DP_BASICS",
        "pattern_skills": ["DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given the amount of money in each house `nums`, return the maximum sum you can rob without robbing two adjacent houses.",
        "constraints": "1 <= len(nums) <= 10^5",
        "examples": [{"input": "[1,2,3,1]", "output": "4", "explanation": "rob house 0 (1) and house 2 (3) = 4"}],
        "function_name": "house_robber",
        "starter_code": "def house_robber(nums):\n    pass\n",
        "reference_solution": (
            "def house_robber(nums):\n"
            "    prev, curr = 0, 0\n"
            "    for x in nums:\n        prev, curr = curr, max(curr, prev + x)\n"
            "    return curr\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 1]], "hidden": False, "explanation": "typical case"},
            {"args": [[2, 7, 9, 3, 1]], "hidden": False, "explanation": "skip house 1 and 3"},
            {"args": [[5]], "hidden": True, "explanation": "single house"},
            {"args": [[2, 1, 1, 2]], "hidden": True, "explanation": "ties in the DP"},
        ],
        "hints": [
            "State: the best amount considering only the first i houses.",
            "At each house, you either skip it (keep previous best) or rob it (best-so-far two houses back + this house).",
            "You only need the previous two states, not a full array -- O(1) space is possible.",
        ],
    },
    {
        "slug": "kth-largest-element",
        "title": "Kth Largest Element",
        "primary_skill": "HEAP",
        "pattern_skills": ["HEAP"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given `nums` and integer `k`, return the kth largest element (k=1 means the largest).",
        "constraints": "1 <= k <= len(nums) <= 10^5",
        "examples": [{"input": "nums=[3,2,1,5,6,4], k=2", "output": "5", "explanation": "sorted desc: 6,5,4,3,2,1 -- 2nd is 5"}],
        "function_name": "kth_largest",
        "starter_code": "def kth_largest(nums, k):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def kth_largest(nums, k):\n"
            "    heap = nums[:k]\n    heapq.heapify(heap)\n"
            "    for x in nums[k:]:\n"
            "        if x > heap[0]:\n            heapq.heapreplace(heap, x)\n"
            "    return heap[0]\n"
        ),
        "expected_complexity": "O(n log k)",
        "test_cases": [
            {"args": [[3, 2, 1, 5, 6, 4], 2], "hidden": False, "explanation": "typical case"},
            {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "hidden": False, "explanation": "with duplicates"},
            {"args": [[1], 1], "hidden": True, "explanation": "single element"},
        ],
        "hints": [
            "Full sort is O(n log n) -- can you avoid sorting the whole array?",
            "Keep a min-heap of the k largest elements seen so far; its root is your answer.",
            "If a new element beats the heap's smallest kept element, swap it in.",
        ],
    },
    {
        "slug": "top-k-frequent",
        "title": "Top K Frequent Elements",
        "primary_skill": "HEAP",
        "pattern_skills": ["HEAP", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": (
            "Given `nums` and `k`, return the k most frequent values, ordered by frequency (descending), "
            "breaking ties by value ascending."
        ),
        "constraints": "1 <= len(nums) <= 10^5, 1 <= k <= number of distinct values",
        "examples": [{"input": "nums=[1,1,1,2,2,3], k=2", "output": "[1,2]", "explanation": "1 appears 3x, 2 appears 2x"}],
        "function_name": "top_k_frequent",
        "starter_code": "def top_k_frequent(nums, k):\n    pass\n",
        "reference_solution": (
            "from collections import Counter\n"
            "def top_k_frequent(nums, k):\n"
            "    counts = Counter(nums)\n"
            "    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))\n"
            "    return [v for v, _ in items[:k]]\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[1, 1, 1, 2, 2, 3], 2], "hidden": False, "explanation": "typical case"},
            {"args": [[4, 4, 4, 6, 6], 1], "hidden": False, "explanation": "single most frequent"},
            {"args": [[1, 2, 3], 2], "hidden": True, "explanation": "all tied frequencies -- tie-break by value"},
        ],
        "hints": [
            "First count how often each value occurs -- a hashmap does this in O(n).",
            "You need the top k by frequency, not a full sort by frequency necessarily -- though sorting is simple and fine here.",
            "A heap of size k is the O(n log k) alternative once you're comfortable with the hashmap step.",
        ],
    },
    {
        "slug": "reverse-linked-list",
        "title": "Reverse a Linked List",
        "primary_skill": "LINKED_LIST",
        "pattern_skills": ["LINKED_LIST"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": (
            "Given the head of a singly linked list (as a list of values `[1,2,3]` meaning 1->2->3), reverse it "
            "in place and return the new head, represented the same way."
        ),
        "constraints": "0 <= number of nodes <= 5000",
        "examples": [{"input": "[1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "every next-pointer is flipped"}],
        "function_name": "reverse_linked_list",
        "starter_code": "# A ListNode class is provided: ListNode(val, next=None) with .val and .next\ndef reverse_linked_list(head):\n    pass\n",
        "reference_solution": (
            "def reverse_linked_list(head):\n"
            "    prev = None\n    curr = head\n"
            "    while curr:\n"
            "        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n"
            "    return prev\n"
        ),
        "io_transform": {"args": {"0": "linked_list"}, "result": "linked_list"},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5]], "hidden": False, "explanation": "typical case"},
            {"args": [[1]], "hidden": False, "explanation": "single node"},
            {"args": [[]], "hidden": True, "explanation": "empty list"},
        ],
        "hints": [
            "You can't just flip `.next` on a node without first saving where it used to point -- you'd lose the rest of the list.",
            "Track three pointers as you walk forward: the previous node, the current node, and the next node (saved before you overwrite `.next`).",
            "At each step: save `next = curr.next`, then `curr.next = prev`, then advance `prev = curr`, `curr = next`.",
        ],
    },
    {
        "slug": "merge-two-sorted-lists",
        "title": "Merge Two Sorted Linked Lists",
        "primary_skill": "LINKED_LIST",
        "pattern_skills": ["LINKED_LIST"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given two sorted linked lists (as value lists), merge them into one sorted linked list and return it.",
        "constraints": "0 <= length of each list <= 5000, both already sorted ascending",
        "examples": [{"input": "l1=[1,2,4], l2=[1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": "merged in sorted order"}],
        "function_name": "merge_two_sorted_lists",
        "starter_code": "# A ListNode class is provided: ListNode(val, next=None)\ndef merge_two_sorted_lists(l1, l2):\n    pass\n",
        "reference_solution": (
            "def merge_two_sorted_lists(l1, l2):\n"
            "    dummy = ListNode(0)\n    tail = dummy\n"
            "    while l1 and l2:\n"
            "        if l1.val <= l2.val:\n            tail.next = l1\n            l1 = l1.next\n"
            "        else:\n            tail.next = l2\n            l2 = l2.next\n"
            "        tail = tail.next\n"
            "    tail.next = l1 or l2\n"
            "    return dummy.next\n"
        ),
        "io_transform": {"args": {"0": "linked_list", "1": "linked_list"}, "result": "linked_list"},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 4], [1, 3, 4]], "hidden": False, "explanation": "typical case"},
            {"args": [[], []], "hidden": False, "explanation": "both empty"},
            {"args": [[], [0]], "hidden": True, "explanation": "one empty"},
        ],
        "hints": [
            "A 'dummy' sentinel head node avoids special-casing which list starts smallest.",
            "The ListNode class is available in your code -- use `ListNode(0)` as a throwaway starting point, then build off `.next`.",
            "Once one list runs out, the rest of the other list is already sorted -- just attach it directly.",
        ],
    },
    {
        "slug": "max-depth-binary-tree",
        "title": "Maximum Depth of a Binary Tree",
        "primary_skill": "TREES",
        "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 1,
        "statement": (
            "Given a binary tree in level-order form (`[3,9,20,null,null,15,7]`, `null` for a missing child), "
            "return its maximum depth (the number of nodes on the longest root-to-leaf path)."
        ),
        "constraints": "0 <= number of nodes <= 10^4",
        "examples": [{"input": "[3,9,20,null,null,15,7]", "output": "3", "explanation": "3 -> 20 -> 15 (or 7) is the longest path"}],
        "function_name": "max_depth",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef max_depth(root):\n    pass\n",
        "reference_solution": (
            "def max_depth(root):\n"
            "    if root is None:\n        return 0\n"
            "    return 1 + max(max_depth(root.left), max_depth(root.right))\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "hidden": False, "explanation": "typical case"},
            {"args": [[]], "hidden": False, "explanation": "empty tree"},
            {"args": [[1]], "hidden": True, "explanation": "single node"},
            {"args": [[1, None, 2]], "hidden": True, "explanation": "only a right child"},
        ],
        "hints": [
            "The depth of a tree is 1 (for the root) plus the deeper of its two subtrees' depths.",
            "This is naturally recursive: `max_depth(root) = 1 + max(max_depth(left), max_depth(right))`.",
            "Base case: an empty tree (`None`) has depth 0.",
        ],
    },
    {
        "slug": "invert-binary-tree",
        "title": "Invert a Binary Tree",
        "primary_skill": "TREES",
        "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a binary tree in level-order form, swap every node's left and right children (mirror the tree) and return the root.",
        "constraints": "0 <= number of nodes <= 10^4",
        "examples": [{"input": "[4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]", "explanation": "every left/right pair is swapped"}],
        "function_name": "invert_tree",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef invert_tree(root):\n    pass\n",
        "reference_solution": (
            "def invert_tree(root):\n"
            "    if root is None:\n        return None\n"
            "    root.left, root.right = invert_tree(root.right), invert_tree(root.left)\n"
            "    return root\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}, "result": "binary_tree"},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[4, 2, 7, 1, 3, 6, 9]], "hidden": False, "explanation": "typical case"},
            {"args": [[2, 1, 3]], "hidden": False, "explanation": "small tree"},
            {"args": [[]], "hidden": True, "explanation": "empty tree"},
        ],
        "hints": [
            "This is naturally recursive: invert the left and right subtrees, then swap them at the current node.",
            "You can invert bottom-up (invert children first, then swap) or top-down (swap first, then recurse) -- both work.",
            "`root.left, root.right = invert_tree(root.right), invert_tree(root.left)` does the swap and recursion in one line.",
        ],
    },
    {
        "slug": "valid-palindrome",
        "title": "Valid Palindrome",
        "primary_skill": "STRINGS",
        "pattern_skills": ["STRINGS", "TWO_POINTER"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 2,
        "statement": (
            "Given a string, return True if it's a palindrome after converting to lowercase and removing all "
            "non-alphanumeric characters."
        ),
        "constraints": "0 <= len(s) <= 10^5",
        "examples": [{"input": '"A man, a plan, a canal: Panama"', "output": "true", "explanation": "reads the same forwards and backwards after cleaning"}],
        "function_name": "is_palindrome",
        "starter_code": "def is_palindrome(s):\n    pass\n",
        "reference_solution": (
            "def is_palindrome(s):\n"
            "    filtered = [c.lower() for c in s if c.isalnum()]\n"
            "    return filtered == filtered[::-1]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["A man, a plan, a canal: Panama"], "hidden": False, "explanation": "classic case with punctuation"},
            {"args": ["race a car"], "hidden": False, "explanation": "not a palindrome"},
            {"args": [" "], "hidden": True, "explanation": "no alphanumeric characters -- vacuously true"},
        ],
        "hints": [
            "Punctuation, spaces, and case shouldn't count -- clean the string first.",
            "Build a filtered, lowercased list of only the alphanumeric characters.",
            "Compare the filtered sequence to its own reverse (or use two pointers from both ends).",
        ],
    },
    {
        "slug": "longest-common-prefix",
        "title": "Longest Common Prefix",
        "primary_skill": "STRINGS",
        "pattern_skills": ["STRINGS"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 2, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a list of strings, return the longest common prefix shared by all of them (or an empty string if none).",
        "constraints": "0 <= len(strs) <= 200",
        "examples": [{"input": '["flower","flow","flight"]', "output": '"fl"', "explanation": "all three start with 'fl'"}],
        "function_name": "longest_common_prefix",
        "starter_code": "def longest_common_prefix(strs):\n    pass\n",
        "reference_solution": (
            "def longest_common_prefix(strs):\n"
            "    if not strs:\n        return ''\n"
            "    prefix = strs[0]\n"
            "    for s in strs[1:]:\n"
            "        while not s.startswith(prefix):\n"
            "            prefix = prefix[:-1]\n"
            "            if not prefix:\n                return ''\n"
            "    return prefix\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [["flower", "flow", "flight"]], "hidden": False, "explanation": "typical case"},
            {"args": [["dog", "racecar", "car"]], "hidden": False, "explanation": "no common prefix"},
            {"args": [["single"]], "hidden": True, "explanation": "one string"},
            {"args": [["", "b"]], "hidden": True, "explanation": "one string is empty"},
        ],
        "hints": [
            "Start by assuming the whole first string is the answer, then shrink it.",
            "For each other string, shrink your candidate prefix from the right until the string actually starts with it.",
            "If the candidate prefix ever becomes empty, the answer is empty -- stop early.",
        ],
    },
    {
        "slug": "sliding-window-maximum",
        "title": "Sliding Window Maximum",
        "primary_skill": "QUEUE_DEQUE",
        "pattern_skills": ["QUEUE_DEQUE", "SLIDING_WINDOW"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given `nums` and window size `k`, return the maximum value in every window of size k as it slides from left to right.",
        "constraints": "1 <= k <= len(nums) <= 10^5",
        "examples": [{"input": "nums=[1,3,-1,-3,5,3,6,7], k=3", "output": "[3,3,5,5,6,7]", "explanation": "max of each window of size 3"}],
        "function_name": "max_sliding_window",
        "starter_code": "def max_sliding_window(nums, k):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def max_sliding_window(nums, k):\n"
            "    dq = deque()\n    result = []\n"
            "    for i, x in enumerate(nums):\n"
            "        while dq and nums[dq[-1]] < x:\n            dq.pop()\n"
            "        dq.append(i)\n"
            "        if dq[0] <= i - k:\n            dq.popleft()\n"
            "        if i >= k - 1:\n            result.append(nums[dq[0]])\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 3, -1, -3, 5, 3, 6, 7], 3], "hidden": False, "explanation": "classic case"},
            {"args": [[1], 1], "hidden": False, "explanation": "single element window"},
            {"args": [[9, 11], 2], "hidden": True, "explanation": "one window covering the whole array"},
        ],
        "hints": [
            "Recomputing the max of every window from scratch is O(n*k) -- too slow for the constraints.",
            "Keep a deque of *indices* whose values are in decreasing order -- the front is always the current window's max.",
            "Before adding a new index, pop from the back any indices whose values are smaller (they can never be the max again). Pop from the front any index that's fallen outside the window.",
        ],
    },
    {
        "slug": "count-connected-components",
        "title": "Count Connected Components in a Graph",
        "primary_skill": "GRAPHS",
        "pattern_skills": ["GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": (
            "Given `n` nodes labeled `0` to `n-1` and a list of undirected `edges`, return the number of connected components."
        ),
        "constraints": "1 <= n <= 2000, 0 <= len(edges) <= 5000",
        "examples": [{"input": "n=5, edges=[[0,1],[1,2],[3,4]]", "output": "2", "explanation": "{0,1,2} and {3,4}"}],
        "function_name": "count_components",
        "starter_code": "def count_components(n, edges):\n    pass\n",
        "reference_solution": (
            "def count_components(n, edges):\n"
            "    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n"
            "        return x\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n            parent[ra] = rb\n"
            "    for a, b in edges:\n        union(a, b)\n"
            "    return len({find(x) for x in range(n)})\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [5, [[0, 1], [1, 2], [3, 4]]], "hidden": False, "explanation": "two components"},
            {"args": [4, []], "hidden": False, "explanation": "no edges -- every node is its own component"},
            {"args": [3, [[0, 1], [1, 2]]], "hidden": True, "explanation": "one component"},
        ],
        "hints": [
            "You could do a BFS/DFS from every unvisited node, counting how many searches you start.",
            "Union-Find (disjoint set union) is an alternative: union the two endpoints of every edge.",
            "The number of distinct root parents after processing all edges is the number of components.",
        ],
    },
    {
        "slug": "shortest-path-bfs",
        "title": "Shortest Path in an Unweighted Graph",
        "primary_skill": "GRAPHS",
        "pattern_skills": ["GRAPHS", "QUEUE_DEQUE"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given `n` nodes, undirected `edges`, a `start` node and an `end` node, return the number of edges on the "
            "shortest path from start to end, or -1 if end is unreachable."
        ),
        "constraints": "1 <= n <= 2000",
        "examples": [{"input": "n=6, edges=[[0,1],[1,2],[2,3],[3,4],[0,5]], start=0, end=4", "output": "4", "explanation": "0-1-2-3-4"}],
        "function_name": "shortest_path_length",
        "starter_code": "def shortest_path_length(n, edges, start, end):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def shortest_path_length(n, edges, start, end):\n"
            "    graph = {i: [] for i in range(n)}\n"
            "    for a, b in edges:\n        graph[a].append(b)\n        graph[b].append(a)\n"
            "    visited = {start}\n    q = deque([(start, 0)])\n"
            "    while q:\n"
            "        node, dist = q.popleft()\n"
            "        if node == end:\n            return dist\n"
            "        for nei in graph[node]:\n"
            "            if nei not in visited:\n                visited.add(nei)\n                q.append((nei, dist + 1))\n"
            "    return -1\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [6, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5]], 0, 4], "hidden": False, "explanation": "path of length 4"},
            {"args": [4, [[0, 1], [2, 3]], 0, 3], "hidden": False, "explanation": "unreachable -- disconnected components"},
            {"args": [3, [[0, 1], [1, 2]], 0, 2], "hidden": True, "explanation": "path of length 2"},
        ],
        "hints": [
            "DFS can find *a* path, but not necessarily the *shortest* one -- what algorithm explores level by level?",
            "BFS naturally finds shortest paths in an unweighted graph because it explores all nodes at distance d before any at distance d+1.",
            "Track each node's distance from the start as you enqueue it, and stop as soon as you dequeue the end node.",
        ],
    },
    {
        "slug": "max-non-overlapping-intervals",
        "title": "Maximum Non-Overlapping Intervals",
        "primary_skill": "GREEDY",
        "pattern_skills": ["GREEDY"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": "Given a list of `[start, end]` intervals, return the maximum number of intervals you can select such that no two overlap.",
        "constraints": "0 <= len(intervals) <= 10^5",
        "examples": [{"input": "[[1,2],[2,3],[3,4],[1,3]]", "output": "3", "explanation": "[1,2],[2,3],[3,4] don't overlap"}],
        "function_name": "max_non_overlapping",
        "starter_code": "def max_non_overlapping(intervals):\n    pass\n",
        "reference_solution": (
            "def max_non_overlapping(intervals):\n"
            "    intervals = sorted(intervals, key=lambda iv: iv[1])\n"
            "    count = 0\n    last_end = float('-inf')\n"
            "    for s, e in intervals:\n"
            "        if s >= last_end:\n            count += 1\n            last_end = e\n"
            "    return count\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[[1, 2], [2, 3], [3, 4], [1, 3]]], "hidden": False, "explanation": "typical case"},
            {"args": [[[1, 2], [1, 2], [1, 2]]], "hidden": False, "explanation": "all identical -- can only keep one"},
            {"args": [[[1, 100], [11, 22], [1, 11], [2, 12]]], "hidden": True, "explanation": "sorting by start would pick the wrong first interval"},
        ],
        "hints": [
            "Sorting by start time seems natural, but consider [[1,100],[2,3]] -- picking [1,100] first blocks everything else.",
            "Sort by *end* time instead, and greedily take any interval that starts at or after the last one you took ends.",
            "Prove to yourself why this works: the interval ending soonest always leaves the most room for future picks.",
        ],
    },
    {
        "slug": "generate-subsets",
        "title": "Generate All Subsets",
        "primary_skill": "BACKTRACKING",
        "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a list of distinct integers, return all possible subsets (the power set), in any order.",
        "constraints": "0 <= len(nums) <= 10",
        "examples": [{"input": "[1,2,3]", "output": "[[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]", "explanation": "all 2^3 = 8 subsets, any order accepted"}],
        "function_name": "generate_subsets",
        "starter_code": "def generate_subsets(nums):\n    pass\n",
        "reference_solution": (
            "def generate_subsets(nums):\n"
            "    result = []\n"
            "    def backtrack(start, path):\n"
            "        result.append(path[:])\n"
            "        for i in range(start, len(nums)):\n"
            "            path.append(nums[i])\n            backtrack(i + 1, path)\n            path.pop()\n"
            "    backtrack(0, [])\n"
            "    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(2^n)",
        "test_cases": [
            {"args": [[1, 2, 3]], "hidden": False, "explanation": "typical case, 8 subsets"},
            {"args": [[]], "hidden": False, "explanation": "empty input -- only the empty subset"},
            {"args": [[5]], "hidden": True, "explanation": "single element -- 2 subsets"},
        ],
        "hints": [
            "At each element, you have exactly two choices: include it, or don't.",
            "That's a decision tree of depth n with 2 branches per level -- classic backtracking.",
            "Record the current partial subset at *every* node of the recursion, not just at the leaves -- every partial state is itself a valid subset.",
        ],
    },
    {
        "slug": "generate-permutations",
        "title": "Generate All Permutations",
        "primary_skill": "BACKTRACKING",
        "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a list of distinct integers, return all possible orderings (permutations), in any order.",
        "constraints": "0 <= len(nums) <= 8",
        "examples": [{"input": "[1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]", "explanation": "all 3! = 6 orderings, any order accepted"}],
        "function_name": "generate_permutations",
        "starter_code": "def generate_permutations(nums):\n    pass\n",
        "reference_solution": (
            "def generate_permutations(nums):\n"
            "    result = []\n"
            "    def backtrack(path, remaining):\n"
            "        if not remaining:\n            result.append(path[:])\n            return\n"
            "        for i in range(len(remaining)):\n"
            "            backtrack(path + [remaining[i]], remaining[:i] + remaining[i + 1:])\n"
            "    backtrack([], nums)\n"
            "    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(n!)",
        "test_cases": [
            {"args": [[1, 2, 3]], "hidden": False, "explanation": "typical case, 6 permutations"},
            {"args": [[1]], "hidden": False, "explanation": "single element"},
            {"args": [[1, 2]], "hidden": True, "explanation": "two elements -- 2 permutations"},
        ],
        "hints": [
            "At each position in the output, you choose one of the remaining (not-yet-used) numbers.",
            "Recurse with the chosen number added to the current path and removed from the remaining pool.",
            "Base case: once no numbers remain, the current path is a complete permutation.",
        ],
    },
    {
        "slug": "single-number",
        "title": "Single Number (XOR Trick)",
        "primary_skill": "BIT_MANIPULATION",
        "pattern_skills": ["BIT_MANIPULATION"],
        "difficulty": "easy",
        "concept_difficulty": 3, "implementation_difficulty": 1, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an array where every element appears exactly twice except for one, find that single element, using O(1) extra space.",
        "constraints": "1 <= len(nums) <= 10^5",
        "examples": [{"input": "[4,1,2,1,2]", "output": "4", "explanation": "4 is the only element appearing once"}],
        "function_name": "single_number",
        "starter_code": "def single_number(nums):\n    pass\n",
        "reference_solution": "def single_number(nums):\n    result = 0\n    for x in nums:\n        result ^= x\n    return result\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 2, 1]], "hidden": False, "explanation": "typical case"},
            {"args": [[4, 1, 2, 1, 2]], "hidden": False, "explanation": "single element not adjacent to its pair"},
            {"args": [[1]], "hidden": True, "explanation": "only one element total"},
        ],
        "hints": [
            "A hashmap frequency count solves this in O(n) time and O(n) space -- but the constraint asks for O(1) space.",
            "XOR has two useful properties here: `x ^ x = 0`, and `x ^ 0 = x`.",
            "XOR every element together -- every pair cancels to 0, leaving only the unpaired value.",
        ],
    },
    {
        "slug": "count-set-bits",
        "title": "Count Set Bits",
        "primary_skill": "BIT_MANIPULATION",
        "pattern_skills": ["BIT_MANIPULATION"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a non-negative integer `n`, return the number of 1-bits in its binary representation.",
        "constraints": "0 <= n <= 2^31 - 1",
        "examples": [{"input": "11", "output": "3", "explanation": "11 is 1011 in binary -- three 1-bits"}],
        "function_name": "count_set_bits",
        "starter_code": "def count_set_bits(n):\n    pass\n",
        "reference_solution": "def count_set_bits(n):\n    count = 0\n    while n:\n        n &= n - 1\n        count += 1\n    return count\n",
        "expected_complexity": "O(1)",
        "test_cases": [
            {"args": [0], "hidden": False, "explanation": "no bits set"},
            {"args": [11], "hidden": False, "explanation": "1011 in binary"},
            {"args": [128], "hidden": True, "explanation": "a single high bit -- 10000000"},
            {"args": [255], "hidden": True, "explanation": "all 8 low bits set"},
        ],
        "hints": [
            "You could check each of the 32 bits individually with `n & 1` and shift right each time.",
            "There's a faster trick: `n & (n - 1)` always clears exactly the lowest set bit.",
            "Repeat `n &= n - 1` and count iterations until n becomes 0 -- that count is the number of set bits.",
        ],
    },
    {
        "slug": "redundant-connection",
        "title": "Redundant Connection",
        "primary_skill": "UNION_FIND",
        "pattern_skills": ["UNION_FIND"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "A tree with n nodes had one extra edge added, creating exactly one cycle. Given the resulting list "
            "of edges (1-indexed nodes), return the edge that can be removed to make it a valid tree again -- if "
            "multiple answers exist, return the one that occurs last in the input."
        ),
        "constraints": "3 <= n <= 1000, edges form exactly one cycle",
        "examples": [{"input": "[[1,2],[1,3],[2,3]]", "output": "[2,3]", "explanation": "removing edge [2,3] leaves a valid tree"}],
        "function_name": "find_redundant_connection",
        "starter_code": "def find_redundant_connection(edges):\n    pass\n",
        "reference_solution": (
            "def find_redundant_connection(edges):\n"
            "    n = len(edges)\n    parent = list(range(n + 1))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n"
            "        return x\n"
            "    for u, v in edges:\n"
            "        ru, rv = find(u), find(v)\n"
            "        if ru == rv:\n            return [u, v]\n"
            "        parent[ru] = rv\n"
            "    return []\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[[1, 2], [1, 3], [2, 3]]], "hidden": False, "explanation": "simple triangle"},
            {"args": [[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], "hidden": False, "explanation": "cycle among 4 nodes"},
            {"args": [[[1, 2], [1, 3], [1, 4], [3, 4]]], "hidden": True, "explanation": "cycle formed later in the list"},
        ],
        "hints": [
            "Process edges in order, and ask: does this edge connect two nodes that are *already* connected?",
            "Union-Find answers 'already connected?' without a full traversal -- union each edge's endpoints as you go.",
            "The first edge where both endpoints already share a root is the redundant one.",
        ],
    },
    {
        "slug": "number-of-provinces",
        "title": "Number of Provinces",
        "primary_skill": "UNION_FIND",
        "pattern_skills": ["UNION_FIND"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": (
            "Given an n x n matrix `is_connected` where `is_connected[i][j] = 1` means city i and city j are "
            "directly connected, return the number of provinces (groups of directly or indirectly connected cities)."
        ),
        "constraints": "1 <= n <= 200",
        "examples": [{"input": "[[1,1,0],[1,1,0],[0,0,1]]", "output": "2", "explanation": "cities 0,1 form one province; city 2 is its own"}],
        "function_name": "find_provinces",
        "starter_code": "def find_provinces(is_connected):\n    pass\n",
        "reference_solution": (
            "def find_provinces(is_connected):\n"
            "    n = len(is_connected)\n    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n"
            "        return x\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n            parent[ra] = rb\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if is_connected[i][j] == 1:\n                union(i, j)\n"
            "    return len({find(x) for x in range(n)})\n"
        ),
        "expected_complexity": "O(n^2)",
        "test_cases": [
            {"args": [[[1, 1, 0], [1, 1, 0], [0, 0, 1]]], "hidden": False, "explanation": "two provinces"},
            {"args": [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], "hidden": False, "explanation": "no connections -- every city its own province"},
            {"args": [[[1, 1, 1], [1, 1, 1], [1, 1, 1]]], "hidden": True, "explanation": "fully connected -- one province"},
        ],
        "hints": [
            "This is the same connectivity question as connected components, but the graph is given as a matrix, not an edge list.",
            "Union every pair (i, j) where is_connected[i][j] == 1.",
            "The number of distinct roots after all unions is the number of provinces.",
        ],
    },
    {
        "slug": "course-schedule",
        "title": "Course Schedule",
        "primary_skill": "TOPOLOGICAL_SORT",
        "pattern_skills": ["TOPOLOGICAL_SORT", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given `num_courses` and a list of prerequisite pairs `[course, prereq]`, return True if it's possible "
            "to finish all courses (i.e. the prerequisite graph has no cycle)."
        ),
        "constraints": "1 <= num_courses <= 2000",
        "examples": [{"input": "num_courses=2, prerequisites=[[1,0]]", "output": "true", "explanation": "take 0, then 1"}],
        "function_name": "can_finish",
        "starter_code": "def can_finish(num_courses, prerequisites):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def can_finish(num_courses, prerequisites):\n"
            "    graph = {i: [] for i in range(num_courses)}\n    indegree = [0] * num_courses\n"
            "    for course, prereq in prerequisites:\n"
            "        graph[prereq].append(course)\n        indegree[course] += 1\n"
            "    q = deque([i for i in range(num_courses) if indegree[i] == 0])\n"
            "    visited = 0\n"
            "    while q:\n"
            "        node = q.popleft()\n        visited += 1\n"
            "        for nei in graph[node]:\n"
            "            indegree[nei] -= 1\n"
            "            if indegree[nei] == 0:\n                q.append(nei)\n"
            "    return visited == num_courses\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [2, [[1, 0]]], "hidden": False, "explanation": "no cycle"},
            {"args": [2, [[1, 0], [0, 1]]], "hidden": False, "explanation": "a 2-cycle -- impossible"},
            {"args": [4, [[1, 0], [2, 0], [3, 1], [3, 2]]], "hidden": True, "explanation": "diamond-shaped dependency, no cycle"},
        ],
        "hints": [
            "This is really asking: does the prerequisite graph (a directed graph) contain a cycle?",
            "Kahn's algorithm processes nodes with no remaining prerequisites first, removing their outgoing edges as it goes.",
            "If every course eventually gets processed, there's no cycle; if some are left stuck, they're part of one.",
        ],
    },
    {
        "slug": "eventual-safe-states",
        "title": "Eventual Safe States",
        "primary_skill": "TOPOLOGICAL_SORT",
        "pattern_skills": ["TOPOLOGICAL_SORT", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": (
            "Given a directed graph as an adjacency list `graph` (graph[i] lists i's outgoing neighbors), a node is "
            "'safe' if every path starting there eventually reaches a terminal node (no path from it can cycle "
            "forever). Return the sorted list of all safe nodes."
        ),
        "constraints": "1 <= len(graph) <= 10^4",
        "examples": [{"input": "[[1,2],[2,3],[5],[0],[5],[],[]]", "output": "[2,4,5,6]", "explanation": "nodes 2,4,5,6 only lead to terminal nodes"}],
        "function_name": "eventual_safe_nodes",
        "starter_code": "def eventual_safe_nodes(graph):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def eventual_safe_nodes(graph):\n"
            "    n = len(graph)\n    rev = {i: [] for i in range(n)}\n    outdegree = [0] * n\n"
            "    for u in range(n):\n"
            "        for v in graph[u]:\n            rev[v].append(u)\n"
            "        outdegree[u] = len(graph[u])\n"
            "    q = deque([i for i in range(n) if outdegree[i] == 0])\n"
            "    safe = [False] * n\n"
            "    while q:\n"
            "        node = q.popleft()\n        safe[node] = True\n"
            "        for u in rev[node]:\n"
            "            outdegree[u] -= 1\n"
            "            if outdegree[u] == 0:\n                q.append(u)\n"
            "    return [i for i in range(n) if safe[i]]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[[1, 2], [2, 3], [5], [0], [5], [], []]], "hidden": False, "explanation": "classic case with one cycle (0<->3)"},
            {"args": [[[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]], "hidden": False, "explanation": "only node 4 is safe"},
            {"args": [[[], []]], "hidden": True, "explanation": "no edges -- both nodes trivially safe"},
        ],
        "hints": [
            "A terminal node (no outgoing edges) is trivially safe.",
            "Work backward from terminal nodes using the *reverse* graph -- this is topological sort applied in reverse.",
            "A node becomes safe once every one of its outgoing edges has been shown to lead somewhere safe.",
        ],
    },
    {
        "slug": "network-delay-time",
        "title": "Network Delay Time",
        "primary_skill": "DIJKSTRA",
        "pattern_skills": ["DIJKSTRA", "HEAP", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "`times[i] = [u, v, w]` means a signal from node u reaches node v in w time. Given `n` nodes labeled "
            "1..n and a starting node `k`, return the time for the signal to reach every node, or -1 if impossible."
        ),
        "constraints": "1 <= n <= 100, all weights positive",
        "examples": [{"input": "times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2", "output": "2", "explanation": "node 4 (farthest) is reached at time 2"}],
        "function_name": "network_delay_time",
        "starter_code": "def network_delay_time(times, n, k):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def network_delay_time(times, n, k):\n"
            "    graph = {i: [] for i in range(1, n + 1)}\n"
            "    for u, v, w in times:\n        graph[u].append((v, w))\n"
            "    dist = {i: float('inf') for i in range(1, n + 1)}\n    dist[k] = 0\n"
            "    heap = [(0, k)]\n"
            "    while heap:\n"
            "        d, node = heapq.heappop(heap)\n"
            "        if d > dist[node]:\n            continue\n"
            "        for nei, w in graph[node]:\n"
            "            nd = d + w\n"
            "            if nd < dist[nei]:\n                dist[nei] = nd\n                heapq.heappush(heap, (nd, nei))\n"
            "    maxd = max(dist.values())\n"
            "    return maxd if maxd < float('inf') else -1\n"
        ),
        "expected_complexity": "O((V+E) log V)",
        "test_cases": [
            {"args": [[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], "hidden": False, "explanation": "classic case"},
            {"args": [[[1, 2, 1]], 2, 1], "hidden": False, "explanation": "single edge"},
            {"args": [[[1, 2, 1]], 2, 2], "hidden": True, "explanation": "node 1 is unreachable from 2"},
        ],
        "hints": [
            "You need the shortest time to *every* node from a single source -- that's single-source shortest path.",
            "All weights are positive here, so Dijkstra applies directly.",
            "The answer is the *maximum* over all nodes' shortest distances -- the last node to receive the signal.",
        ],
    },
    {
        "slug": "dijkstra-shortest-path",
        "title": "Shortest Path Between Two Nodes (Weighted)",
        "primary_skill": "DIJKSTRA",
        "pattern_skills": ["DIJKSTRA", "HEAP", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": (
            "Given `n` nodes, a list of undirected weighted `edges` as `[u, v, w]`, a `source`, and a `destination`, "
            "return the shortest distance between them, or -1 if unreachable."
        ),
        "constraints": "1 <= n <= 1000, all weights non-negative",
        "examples": [{"input": "n=5, edges=[[0,1,4],[0,2,1],[2,1,1],[1,3,1],[2,3,5]], source=0, destination=3", "output": "3", "explanation": "path 0->2->1->3 costs 1+1+1=3"}],
        "function_name": "dijkstra_shortest_path",
        "starter_code": "def dijkstra_shortest_path(n, edges, source, destination):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def dijkstra_shortest_path(n, edges, source, destination):\n"
            "    graph = {i: [] for i in range(n)}\n"
            "    for u, v, w in edges:\n        graph[u].append((v, w))\n        graph[v].append((u, w))\n"
            "    dist = [float('inf')] * n\n    dist[source] = 0\n"
            "    heap = [(0, source)]\n"
            "    while heap:\n"
            "        d, node = heapq.heappop(heap)\n"
            "        if d > dist[node]:\n            continue\n"
            "        for nei, w in graph[node]:\n"
            "            nd = d + w\n"
            "            if nd < dist[nei]:\n                dist[nei] = nd\n                heapq.heappush(heap, (nd, nei))\n"
            "    return dist[destination] if dist[destination] != float('inf') else -1\n"
        ),
        "expected_complexity": "O((V+E) log V)",
        "test_cases": [
            {"args": [5, [[0, 1, 4], [0, 2, 1], [2, 1, 1], [1, 3, 1], [2, 3, 5]], 0, 3], "hidden": False, "explanation": "a detour beats the direct-looking path"},
            {"args": [3, [[0, 1, 1], [1, 2, 1]], 0, 2], "hidden": False, "explanation": "simple chain"},
            {"args": [3, [[0, 1, 1]], 0, 2], "hidden": True, "explanation": "unreachable"},
        ],
        "hints": [
            "Build an adjacency list including weights for both directions (undirected).",
            "Use a min-heap keyed by current known distance, always expanding the closest unfinalized node.",
            "You can stop early the moment you pop the destination node -- its distance is now guaranteed final.",
        ],
    },
    {
        "slug": "zero-one-knapsack",
        "title": "0/1 Knapsack",
        "primary_skill": "DP_KNAPSACK",
        "pattern_skills": ["DP_KNAPSACK", "DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given item `weights`, `values`, and a knapsack `capacity`, return the maximum total value achievable without exceeding the capacity (each item used at most once).",
        "constraints": "1 <= len(weights) <= 100, 1 <= capacity <= 1000",
        "examples": [{"input": "weights=[1,3,4,5], values=[1,4,5,7], capacity=7", "output": "9", "explanation": "items of weight 3 and 4 (value 4+5=9) fit exactly"}],
        "function_name": "knapsack",
        "starter_code": "def knapsack(weights, values, capacity):\n    pass\n",
        "reference_solution": (
            "def knapsack(weights, values, capacity):\n"
            "    n = len(weights)\n    dp = [0] * (capacity + 1)\n"
            "    for i in range(n):\n"
            "        for c in range(capacity, weights[i] - 1, -1):\n"
            "            dp[c] = max(dp[c], values[i] + dp[c - weights[i]])\n"
            "    return dp[capacity]\n"
        ),
        "expected_complexity": "O(n * capacity)",
        "test_cases": [
            {"args": [[1, 3, 4, 5], [1, 4, 5, 7], 7], "hidden": False, "explanation": "typical case"},
            {"args": [[2, 3, 4], [3, 4, 5], 5], "hidden": False, "explanation": "small case"},
            {"args": [[1, 2, 3], [6, 10, 12], 5], "hidden": True, "explanation": "value-dense items"},
        ],
        "hints": [
            "State: the best value achievable using the first i items with capacity c.",
            "For each item, you either skip it, or take it (if it fits) and add its value to the best achievable with the remaining capacity.",
            "Iterate the capacity dimension *backward* when using a 1D rolling array, so each item is only considered once.",
        ],
    },
    {
        "slug": "coin-change-min-coins",
        "title": "Coin Change (Minimum Coins)",
        "primary_skill": "DP_KNAPSACK",
        "pattern_skills": ["DP_KNAPSACK", "DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given `coins` (unlimited supply of each denomination) and a target `amount`, return the minimum number of coins needed to make that amount, or -1 if impossible.",
        "constraints": "1 <= len(coins) <= 20, 0 <= amount <= 10^4",
        "examples": [{"input": "coins=[1,2,5], amount=11", "output": "3", "explanation": "5+5+1=11 using 3 coins"}],
        "function_name": "coin_change",
        "starter_code": "def coin_change(coins, amount):\n    pass\n",
        "reference_solution": (
            "def coin_change(coins, amount):\n"
            "    dp = [0] + [float('inf')] * amount\n"
            "    for a in range(1, amount + 1):\n"
            "        for c in coins:\n"
            "            if c <= a and dp[a - c] + 1 < dp[a]:\n                dp[a] = dp[a - c] + 1\n"
            "    return dp[amount] if dp[amount] != float('inf') else -1\n"
        ),
        "expected_complexity": "O(amount * len(coins))",
        "test_cases": [
            {"args": [[1, 2, 5], 11], "hidden": False, "explanation": "typical case"},
            {"args": [[2], 3], "hidden": False, "explanation": "impossible -- odd amount, only even coin"},
            {"args": [[1], 0], "hidden": True, "explanation": "zero amount needs zero coins"},
        ],
        "hints": [
            "This is the unbounded-knapsack shape: each coin denomination can be reused any number of times.",
            "State: the minimum coins needed to make amount a. Transition: try using one of each coin, plus the best answer for the remainder.",
            "Unlike 0/1 knapsack, the capacity (amount) loop runs forward here, since reuse is allowed.",
        ],
    },
    {
        "slug": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "primary_skill": "DP_STRING",
        "pattern_skills": ["DP_STRING", "DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given two strings `text1` and `text2`, return the length of their longest common subsequence (characters in the same relative order, not necessarily contiguous).",
        "constraints": "0 <= len(text1), len(text2) <= 1000",
        "examples": [{"input": 'text1="abcde", text2="ace"', "output": "3", "explanation": '"ace" is a common subsequence'}],
        "function_name": "longest_common_subsequence",
        "starter_code": "def longest_common_subsequence(text1, text2):\n    pass\n",
        "reference_solution": (
            "def longest_common_subsequence(text1, text2):\n"
            "    m, n = len(text1), len(text2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if text1[i - 1] == text2[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1] + 1\n"
            "            else:\n                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n"
            "    return dp[m][n]\n"
        ),
        "expected_complexity": "O(m * n)",
        "test_cases": [
            {"args": ["abcde", "ace"], "hidden": False, "explanation": "typical case"},
            {"args": ["abc", "abc"], "hidden": False, "explanation": "identical strings"},
            {"args": ["abc", "def"], "hidden": True, "explanation": "no common characters"},
        ],
        "hints": [
            "Build a 2D table comparing every prefix of text1 against every prefix of text2.",
            "If the current characters match, extend the diagonal's answer by 1.",
            "If they don't match, take the best of dropping a character from either string.",
        ],
    },
    {
        "slug": "edit-distance",
        "title": "Edit Distance",
        "primary_skill": "DP_STRING",
        "pattern_skills": ["DP_STRING", "DP_BASICS"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given two strings `word1` and `word2`, return the minimum number of insert/delete/replace operations needed to turn `word1` into `word2`.",
        "constraints": "0 <= len(word1), len(word2) <= 500",
        "examples": [{"input": 'word1="horse", word2="ros"', "output": "3", "explanation": "replace h->r, delete r, delete e"}],
        "function_name": "min_edit_distance",
        "starter_code": "def min_edit_distance(word1, word2):\n    pass\n",
        "reference_solution": (
            "def min_edit_distance(word1, word2):\n"
            "    m, n = len(word1), len(word2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(m + 1):\n        dp[i][0] = i\n"
            "    for j in range(n + 1):\n        dp[0][j] = j\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if word1[i - 1] == word2[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1]\n"
            "            else:\n                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n"
            "    return dp[m][n]\n"
        ),
        "expected_complexity": "O(m * n)",
        "test_cases": [
            {"args": ["horse", "ros"], "hidden": False, "explanation": "classic case"},
            {"args": ["intention", "execution"], "hidden": False, "explanation": "longer strings"},
            {"args": ["", "abc"], "hidden": True, "explanation": "one string empty -- pure insertions"},
        ],
        "hints": [
            "Base cases: turning an empty string into a string of length k always takes k insertions (or vice versa for deletions).",
            "On a matching character, no operation is needed -- carry forward the diagonal's answer.",
            "On a mismatch, consider all three operations (insert, delete, replace) and take whichever leads to the smallest subproblem answer, plus 1.",
        ],
    },
    {
        "slug": "meeting-rooms-ii",
        "title": "Meeting Rooms II",
        "primary_skill": "ADVANCED_PATTERNS",
        "pattern_skills": ["ADVANCED_PATTERNS", "HEAP", "GREEDY"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given meeting time intervals `[[start, end], ...]`, return the minimum number of conference rooms required so no two overlapping meetings share a room.",
        "constraints": "0 <= len(intervals) <= 10^4",
        "examples": [{"input": "[[0,30],[5,10],[15,20]]", "output": "2", "explanation": "meetings [5,10] and [15,20] both overlap [0,30], but never each other"}],
        "function_name": "min_meeting_rooms",
        "starter_code": "def min_meeting_rooms(intervals):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def min_meeting_rooms(intervals):\n"
            "    if not intervals:\n        return 0\n"
            "    intervals = sorted(intervals)\n    heap = []\n"
            "    for s, e in intervals:\n"
            "        if heap and heap[0] <= s:\n            heapq.heapreplace(heap, e)\n"
            "        else:\n            heapq.heappush(heap, e)\n"
            "    return len(heap)\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[[0, 30], [5, 10], [15, 20]]], "hidden": False, "explanation": "classic case"},
            {"args": [[[7, 10], [2, 4]]], "hidden": False, "explanation": "no overlap -- one room suffices"},
            {"args": [[[1, 5], [8, 9], [8, 9]]], "hidden": True, "explanation": "two meetings starting at the same time"},
        ],
        "hints": [
            "Think of this as a sweep line: sort meetings by start time, and track end times of currently-ongoing meetings in a min-heap.",
            "If the earliest-ending ongoing meeting has already finished by the time the next one starts, they can reuse the same room.",
            "The heap's size at the end (or its peak size during the sweep) is the number of rooms needed.",
        ],
    },
    {
        "slug": "range-difference-array",
        "title": "Apply Range Updates (Difference Array)",
        "primary_skill": "ADVANCED_PATTERNS",
        "pattern_skills": ["ADVANCED_PATTERNS", "ARRAYS_PREFIX_SUM"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given an array of length `n` (initially all zeros) and a list of `updates`, each `[start, end, val]` "
            "meaning 'add val to every index from start to end inclusive', return the final array after applying all updates."
        ),
        "constraints": "1 <= n <= 10^5, 0 <= len(updates) <= 10^4",
        "examples": [{"input": "n=5, updates=[[1,3,2],[2,4,3]]", "output": "[0,2,5,5,3]", "explanation": "overlapping ranges add up"}],
        "function_name": "apply_range_updates",
        "starter_code": "def apply_range_updates(n, updates):\n    pass\n",
        "reference_solution": (
            "def apply_range_updates(n, updates):\n"
            "    diff = [0] * (n + 1)\n"
            "    for s, e, v in updates:\n"
            "        diff[s] += v\n        diff[e + 1] -= v\n"
            "    result = []\n    running = 0\n"
            "    for i in range(n):\n"
            "        running += diff[i]\n        result.append(running)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n + updates)",
        "test_cases": [
            {"args": [5, [[1, 3, 2], [2, 4, 3]]], "hidden": False, "explanation": "overlapping ranges"},
            {"args": [3, [[0, 2, 5]]], "hidden": False, "explanation": "single range covering everything"},
            {"args": [4, []], "hidden": True, "explanation": "no updates at all"},
        ],
        "hints": [
            "Applying each update by looping over its whole range is O(n) per update -- too slow for many updates.",
            "Instead, just record the *change in slope* at the boundaries: +v where the range starts, -v right after it ends.",
            "A single prefix-sum pass at the end materializes every update's effect simultaneously.",
        ],
    },
]
