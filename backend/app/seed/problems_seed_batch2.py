"""
Second batch of seeded problems -- see problems_seed.py for the honesty note on
how expected outputs are generated (by executing each reference solution, never
hand-typed). This batch focuses on filling out skills that had thin coverage
(1-2 problems) after the first pass, and adds several classic LeetCode-style
problems as original, independently-written statements and solutions.
"""

PROBLEMS_BATCH2 = [
    {
        "slug": "move-zeroes",
        "title": "Move Zeroes to the End",
        "primary_skill": "ARRAYS_TRAVERSAL", "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 2, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given an array `nums`, move all 0s to the end while keeping the relative order of the non-zero elements. Return the resulting array.",
        "constraints": "0 <= len(nums) <= 10^4",
        "examples": [{"input": "[0,1,0,3,12]", "output": "[1,3,12,0,0]", "explanation": "non-zero order preserved, zeroes pushed to the end"}],
        "function_name": "move_zeroes",
        "starter_code": "def move_zeroes(nums):\n    pass\n",
        "reference_solution": "def move_zeroes(nums):\n    result = [x for x in nums if x != 0]\n    result += [0] * (len(nums) - len(result))\n    return result\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[0, 1, 0, 3, 12]], "hidden": False, "explanation": "typical case"},
            {"args": [[0, 0, 1]], "hidden": False, "explanation": "zeroes at the start"},
            {"args": [[1, 2, 3]], "hidden": True, "explanation": "no zeroes at all"},
        ],
        "hints": ["Collect the non-zero elements first, in order.", "The number of zeroes needed at the end equals the length difference.", "`[x for x in nums if x != 0]` plus the right number of zeroes solves it in one pass conceptually."],
    },
    {
        "slug": "merge-sorted-array",
        "title": "Merge Two Sorted Arrays",
        "primary_skill": "ARRAYS_TRAVERSAL", "pattern_skills": ["ARRAYS_TRAVERSAL", "TWO_POINTER"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 2, "reasoning_difficulty": 1, "pattern_difficulty": 2,
        "statement": "Given two sorted arrays `nums1` and `nums2`, return a single merged sorted array.",
        "constraints": "0 <= len(nums1), len(nums2) <= 10^4",
        "examples": [{"input": "[1,2,3], [2,5,6]", "output": "[1,2,2,3,5,6]", "explanation": "merged in sorted order"}],
        "function_name": "merge_sorted",
        "starter_code": "def merge_sorted(nums1, nums2):\n    pass\n",
        "reference_solution": (
            "def merge_sorted(nums1, nums2):\n"
            "    result = []\n    i = j = 0\n"
            "    while i < len(nums1) and j < len(nums2):\n"
            "        if nums1[i] <= nums2[j]:\n            result.append(nums1[i]); i += 1\n"
            "        else:\n            result.append(nums2[j]); j += 1\n"
            "    result.extend(nums1[i:])\n    result.extend(nums2[j:])\n    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3], [2, 5, 6]], "hidden": False, "explanation": "typical case"},
            {"args": [[], [1]], "hidden": False, "explanation": "one array empty"},
            {"args": [[4, 5, 6], [1, 2, 3]], "hidden": True, "explanation": "second array entirely smaller"},
        ],
        "hints": ["This is exactly the merge step of merge sort.", "Use two pointers, one per array, always taking the smaller current element.", "Once one array runs out, append the rest of the other -- it's already sorted."],
    },
    {
        "slug": "remove-duplicates-sorted-array",
        "title": "Remove Duplicates from a Sorted Array",
        "primary_skill": "ARRAYS_TRAVERSAL", "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a sorted array `nums`, return a new array containing only the unique elements, preserving order.",
        "constraints": "0 <= len(nums) <= 10^4, nums is sorted ascending",
        "examples": [{"input": "[1,1,2]", "output": "[1,2]", "explanation": "duplicate 1 removed"}],
        "function_name": "remove_duplicates",
        "starter_code": "def remove_duplicates(nums):\n    pass\n",
        "reference_solution": (
            "def remove_duplicates(nums):\n"
            "    if not nums:\n        return []\n"
            "    result = [nums[0]]\n"
            "    for x in nums[1:]:\n        if x != result[-1]:\n            result.append(x)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 1, 2]], "hidden": False, "explanation": "typical case"},
            {"args": [[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]], "hidden": False, "explanation": "many duplicates"},
            {"args": [[1]], "hidden": True, "explanation": "single element"},
        ],
        "hints": ["Because the array is sorted, duplicates are always adjacent.", "Compare each element only to the last one you kept, not the whole result so far.", "One pass, one comparison per element."],
    },
    {
        "slug": "subarray-sum-equals-k",
        "title": "Subarray Sum Equals K",
        "primary_skill": "ARRAYS_PREFIX_SUM", "pattern_skills": ["ARRAYS_PREFIX_SUM", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given an array `nums` and an integer `k`, return the number of contiguous subarrays whose sum equals `k`.",
        "constraints": "1 <= len(nums) <= 2*10^4, values can be negative",
        "examples": [{"input": "nums=[1,1,1], k=2", "output": "2", "explanation": "[1,1] appears at two positions"}],
        "function_name": "subarray_sum_equals_k",
        "starter_code": "def subarray_sum_equals_k(nums, k):\n    pass\n",
        "reference_solution": (
            "from collections import defaultdict\n"
            "def subarray_sum_equals_k(nums, k):\n"
            "    count = defaultdict(int)\n    count[0] = 1\n"
            "    total = 0\n    result = 0\n"
            "    for x in nums:\n"
            "        total += x\n        result += count[total - k]\n        count[total] += 1\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 1, 1], 2], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 2, 3], 3], "hidden": False, "explanation": "two different subarrays sum to 3"},
            {"args": [[1, -1, 0], 0], "hidden": True, "explanation": "negative numbers involved"},
        ],
        "hints": ["A brute-force check of every subarray is O(n^2) -- too slow for the constraints.", "If prefix[j] - prefix[i] = k, the subarray between i and j sums to k. Rearrange: prefix[i] = prefix[j] - k.", "Track how many times each prefix sum has occurred in a hashmap as you go."],
    },
    {
        "slug": "pivot-index",
        "title": "Find the Pivot Index",
        "primary_skill": "ARRAYS_PREFIX_SUM", "pattern_skills": ["ARRAYS_PREFIX_SUM"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given an array `nums`, return the leftmost index where the sum of elements to its left equals the sum of elements to its right (excluding the index itself). Return -1 if none exists.",
        "constraints": "1 <= len(nums) <= 10^4",
        "examples": [{"input": "[1,7,3,6,5,6]", "output": "3", "explanation": "left sum 1+7+3=11 equals right sum 5+6=11"}],
        "function_name": "pivot_index",
        "starter_code": "def pivot_index(nums):\n    pass\n",
        "reference_solution": (
            "def pivot_index(nums):\n"
            "    total = sum(nums)\n    left = 0\n"
            "    for i, x in enumerate(nums):\n"
            "        if left == total - left - x:\n            return i\n"
            "        left += x\n"
            "    return -1\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 7, 3, 6, 5, 6]], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 2, 3]], "hidden": False, "explanation": "no pivot exists"},
            {"args": [[2, 1, -1]], "hidden": True, "explanation": "negative number involved"},
        ],
        "hints": ["Total sum minus left sum minus the current element gives the right sum -- no need to re-sum the right side each time.", "Keep a running left-sum as you scan.", "Compare left-sum to (total - left-sum - current) at each index."],
    },
    {
        "slug": "valid-anagram",
        "title": "Valid Anagram",
        "primary_skill": "HASHING", "pattern_skills": ["HASHING"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given two strings `s` and `t`, return True if `t` is an anagram of `s`.",
        "constraints": "0 <= len(s), len(t) <= 5*10^4",
        "examples": [{"input": 's="anagram", t="nagaram"', "output": "true", "explanation": "same letters, same counts"}],
        "function_name": "is_anagram",
        "starter_code": "def is_anagram(s, t):\n    pass\n",
        "reference_solution": "from collections import Counter\ndef is_anagram(s, t):\n    return len(s) == len(t) and Counter(s) == Counter(t)\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["anagram", "nagaram"], "hidden": False, "explanation": "typical anagram"},
            {"args": ["rat", "car"], "hidden": False, "explanation": "not an anagram"},
            {"args": ["a", "ab"], "hidden": True, "explanation": "different lengths"},
        ],
        "hints": ["Two strings are anagrams exactly when they have identical character frequency counts.", "A quick length check first avoids wasted work.", "A frequency map (or Counter) comparison is O(n), faster than sorting both strings."],
    },
    {
        "slug": "first-unique-character",
        "title": "First Unique Character in a String",
        "primary_skill": "HASHING", "pattern_skills": ["HASHING"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a string `s`, return the index of the first character that appears exactly once. Return -1 if there is none.",
        "constraints": "1 <= len(s) <= 10^5, lowercase English letters",
        "examples": [{"input": '"leetcode"', "output": "0", "explanation": "'l' appears once and is first"}],
        "function_name": "first_unique_char",
        "starter_code": "def first_unique_char(s):\n    pass\n",
        "reference_solution": (
            "from collections import Counter\n"
            "def first_unique_char(s):\n"
            "    counts = Counter(s)\n"
            "    for i, c in enumerate(s):\n"
            "        if counts[c] == 1:\n            return i\n"
            "    return -1\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["leetcode"], "hidden": False, "explanation": "typical case"},
            {"args": ["loveleetcode"], "hidden": False, "explanation": "first unique isn't the first character"},
            {"args": ["aabb"], "hidden": True, "explanation": "no unique character"},
        ],
        "hints": ["Count every character's frequency first, in one pass.", "Then scan left to right and return the first character whose count is exactly 1.", "Two passes, both O(n) -- still linear overall."],
    },
    {
        "slug": "contains-duplicate",
        "title": "Contains Duplicate",
        "primary_skill": "HASHING", "pattern_skills": ["HASHING"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given an array `nums`, return True if any value appears at least twice.",
        "constraints": "0 <= len(nums) <= 10^5",
        "examples": [{"input": "[1,2,3,1]", "output": "true", "explanation": "1 appears twice"}],
        "function_name": "contains_duplicate",
        "starter_code": "def contains_duplicate(nums):\n    pass\n",
        "reference_solution": "def contains_duplicate(nums):\n    return len(set(nums)) != len(nums)\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 1]], "hidden": False, "explanation": "has a duplicate"},
            {"args": [[1, 2, 3, 4]], "hidden": False, "explanation": "no duplicates"},
            {"args": [[]], "hidden": True, "explanation": "empty array"},
        ],
        "hints": ["A set only keeps unique values.", "If the set is smaller than the original list, something repeated.", "This is O(n), versus O(n^2) for checking every pair."],
    },
    {
        "slug": "container-with-most-water",
        "title": "Container With Most Water",
        "primary_skill": "TWO_POINTER", "pattern_skills": ["TWO_POINTER"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": "Given heights of vertical lines at each index, find two lines that, together with the x-axis, form a container holding the most water. Return the maximum area.",
        "constraints": "2 <= len(heights) <= 10^5",
        "examples": [{"input": "[1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "lines at index 1 (height 8) and index 8 (height 7) give area 7*7=49"}],
        "function_name": "max_area",
        "starter_code": "def max_area(heights):\n    pass\n",
        "reference_solution": (
            "def max_area(heights):\n"
            "    l, r = 0, len(heights) - 1\n    best = 0\n"
            "    while l < r:\n"
            "        best = max(best, (r - l) * min(heights[l], heights[r]))\n"
            "        if heights[l] < heights[r]:\n            l += 1\n"
            "        else:\n            r -= 1\n"
            "    return best\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "hidden": False, "explanation": "classic case"},
            {"args": [[1, 1]], "hidden": False, "explanation": "minimal case"},
            {"args": [[4, 3, 2, 1, 4]], "hidden": True, "explanation": "tallest lines at both ends"},
        ],
        "hints": ["Checking every pair of lines is O(n^2).", "Start with the widest possible container (both ends) and narrow in.", "The shorter of the two current lines caps the area -- moving its pointer inward is the only way to possibly find something taller."],
    },
    {
        "slug": "three-sum",
        "title": "Three Sum to Zero",
        "primary_skill": "TWO_POINTER", "pattern_skills": ["TWO_POINTER"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 4, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an array `nums`, return all unique triplets `[a, b, c]` such that `a + b + c == 0`. Each triplet's values should be in ascending order; the list of triplets can be in any order.",
        "constraints": "3 <= len(nums) <= 3000",
        "examples": [{"input": "[-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "the two unique zero-sum triplets"}],
        "function_name": "three_sum",
        "starter_code": "def three_sum(nums):\n    pass\n",
        "reference_solution": (
            "def three_sum(nums):\n"
            "    nums = sorted(nums)\n    n = len(nums)\n    result = []\n"
            "    for i in range(n):\n"
            "        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n"
            "        l, r = i + 1, n - 1\n"
            "        while l < r:\n"
            "            s = nums[i] + nums[l] + nums[r]\n"
            "            if s < 0:\n                l += 1\n"
            "            elif s > 0:\n                r -= 1\n"
            "            else:\n"
            "                result.append([nums[i], nums[l], nums[r]])\n"
            "                l += 1; r -= 1\n"
            "                while l < r and nums[l] == nums[l - 1]:\n                    l += 1\n"
            "                while l < r and nums[r] == nums[r + 1]:\n                    r -= 1\n"
            "    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(n^2)",
        "test_cases": [
            {"args": [[-1, 0, 1, 2, -1, -4]], "hidden": False, "explanation": "classic case"},
            {"args": [[0, 1, 1]], "hidden": False, "explanation": "no valid triplet"},
            {"args": [[0, 0, 0]], "hidden": True, "explanation": "all zeros"},
        ],
        "hints": ["Sort first -- this both enables two pointers and makes skipping duplicates easy.", "Fix one number, then use two pointers on the rest to find pairs summing to its negation.", "After sorting, skip over duplicate values at every level to avoid duplicate triplets."],
    },
    {
        "slug": "longest-substring-without-repeating",
        "title": "Longest Substring Without Repeating Characters",
        "primary_skill": "SLIDING_WINDOW", "pattern_skills": ["SLIDING_WINDOW", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a string `s`, return the length of the longest substring without repeating characters.",
        "constraints": "0 <= len(s) <= 5*10^4",
        "examples": [{"input": '"abcabcbb"', "output": "3", "explanation": '"abc" is the longest without repeats'}],
        "function_name": "longest_substring_no_repeat",
        "starter_code": "def longest_substring_no_repeat(s):\n    pass\n",
        "reference_solution": (
            "def longest_substring_no_repeat(s):\n"
            "    seen = {}\n    left = 0\n    best = 0\n"
            "    for right, c in enumerate(s):\n"
            "        if c in seen and seen[c] >= left:\n            left = seen[c] + 1\n"
            "        seen[c] = right\n        best = max(best, right - left + 1)\n"
            "    return best\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["abcabcbb"], "hidden": False, "explanation": "classic case"},
            {"args": ["bbbbb"], "hidden": False, "explanation": "all same character"},
            {"args": ["pwwkew"], "hidden": True, "explanation": "repeat forces a jump, not a simple shrink"},
        ],
        "hints": ["Track the last seen index of each character in a hashmap.", "When you see a repeat inside the current window, jump `left` to just past its last occurrence -- not necessarily by one.", "The window is always the longest repeat-free substring ending at `right`."],
    },
    {
        "slug": "minimum-size-subarray-sum",
        "title": "Minimum Size Subarray Sum",
        "primary_skill": "SLIDING_WINDOW", "pattern_skills": ["SLIDING_WINDOW"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an array of positive integers `nums` and a target `target`, return the minimal length of a contiguous subarray whose sum is >= target. Return 0 if no such subarray exists.",
        "constraints": "1 <= len(nums) <= 10^5, all values positive",
        "examples": [{"input": "target=7, nums=[2,3,1,2,4,3]", "output": "2", "explanation": "[4,3] sums to 7 with length 2"}],
        "function_name": "min_subarray_len",
        "starter_code": "def min_subarray_len(target, nums):\n    pass\n",
        "reference_solution": (
            "def min_subarray_len(target, nums):\n"
            "    left = 0\n    total = 0\n    best = float('inf')\n"
            "    for right, x in enumerate(nums):\n"
            "        total += x\n"
            "        while total >= target:\n"
            "            best = min(best, right - left + 1)\n            total -= nums[left]\n            left += 1\n"
            "    return best if best != float('inf') else 0\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [7, [2, 3, 1, 2, 4, 3]], "hidden": False, "explanation": "typical case"},
            {"args": [4, [1, 4, 4]], "hidden": False, "explanation": "single element already meets target"},
            {"args": [11, [1, 1, 1, 1, 1, 1, 1, 1]], "hidden": True, "explanation": "no subarray reaches the target"},
        ],
        "hints": ["Since all values are positive, growing the window only ever increases the sum -- shrinking only ever decreases it.", "Expand the window until the sum meets the target, then shrink from the left while it still does, recording the shortest length.", "Because both pointers only move forward, this is O(n) total, not O(n^2)."],
    },
    {
        "slug": "search-insert-position",
        "title": "Search Insert Position",
        "primary_skill": "BINARY_SEARCH", "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a sorted array of distinct integers `nums` and a `target`, return the index where target is found, or where it would be inserted to keep the array sorted.",
        "constraints": "1 <= len(nums) <= 10^4",
        "examples": [{"input": "nums=[1,3,5,6], target=5", "output": "2", "explanation": "5 is at index 2"}],
        "function_name": "search_insert",
        "starter_code": "def search_insert(nums, target):\n    pass\n",
        "reference_solution": (
            "def search_insert(nums, target):\n"
            "    lo, hi = 0, len(nums)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < target:\n            lo = mid + 1\n"
            "        else:\n            hi = mid\n"
            "    return lo\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[1, 3, 5, 6], 5], "hidden": False, "explanation": "target present"},
            {"args": [[1, 3, 5, 6], 2], "hidden": False, "explanation": "target absent, inserts in the middle"},
            {"args": [[1, 3, 5, 6], 7], "hidden": True, "explanation": "target inserts at the end"},
        ],
        "hints": ["This is a small variation on standard binary search -- find the first position where nums[i] >= target.", "That position is correct whether or not the target is actually present.", "Use a half-open [lo, hi) invariant to avoid off-by-one bugs."],
    },
    {
        "slug": "find-peak-element",
        "title": "Find a Peak Element",
        "primary_skill": "BINARY_SEARCH", "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "A peak element is one strictly greater than its neighbors (treat out-of-bounds neighbors as negative infinity). Given an array `nums`, return the index of a peak element.",
        "constraints": "1 <= len(nums) <= 1000",
        "examples": [{"input": "[1,2,4,8,5,3]", "output": "3", "explanation": "8 is greater than both neighbors"}],
        "function_name": "find_peak_element",
        "starter_code": "def find_peak_element(nums):\n    pass\n",
        "reference_solution": (
            "def find_peak_element(nums):\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < nums[mid + 1]:\n            lo = mid + 1\n"
            "        else:\n            hi = mid\n"
            "    return lo\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[1, 2, 3, 1]], "hidden": False, "explanation": "single unambiguous peak"},
            {"args": [[1, 2, 4, 8, 5, 3]], "hidden": False, "explanation": "peak in the middle"},
            {"args": [[5, 4, 3, 2, 1]], "hidden": True, "explanation": "strictly decreasing -- peak is the first element"},
        ],
        "hints": ["If nums[mid] < nums[mid+1], a peak must exist somewhere to the right (the slope is still climbing).", "Otherwise, a peak exists at mid or to its left.", "This halves the search space each time even though the array isn't sorted -- binary search doesn't require sortedness, just a way to eliminate half the candidates."],
    },
    {
        "slug": "evaluate-reverse-polish-notation",
        "title": "Evaluate Reverse Polish Notation",
        "primary_skill": "STACK", "pattern_skills": ["STACK"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Evaluate an arithmetic expression given in Reverse Polish Notation (postfix), as a list of tokens (numbers and `+ - * /`). Division truncates toward zero.",
        "constraints": "1 <= len(tokens) <= 10^4",
        "examples": [{"input": '["2","1","+","3","*"]', "output": "9", "explanation": "(2+1)*3 = 9"}],
        "function_name": "eval_rpn",
        "starter_code": "def eval_rpn(tokens):\n    pass\n",
        "reference_solution": (
            "def eval_rpn(tokens):\n"
            "    stack = []\n"
            "    for tok in tokens:\n"
            "        if tok in ('+', '-', '*', '/'):\n"
            "            b = stack.pop(); a = stack.pop()\n"
            "            if tok == '+':\n                stack.append(a + b)\n"
            "            elif tok == '-':\n                stack.append(a - b)\n"
            "            elif tok == '*':\n                stack.append(a * b)\n"
            "            else:\n                stack.append(int(a / b))\n"
            "        else:\n            stack.append(int(tok))\n"
            "    return stack[0]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [["2", "1", "+", "3", "*"]], "hidden": False, "explanation": "typical case"},
            {"args": [["4", "13", "5", "/", "+"]], "hidden": False, "explanation": "involves integer division"},
            {"args": [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]], "hidden": True, "explanation": "longer expression"},
        ],
        "hints": ["A stack is the natural fit: postfix notation is designed to be evaluated with one.", "Push numbers. On an operator, pop the two most recent operands, apply the operator, push the result back.", "Watch the order: for `a - b`, `a` was pushed before `b`, so pop `b` first, then `a`."],
    },
    {
        "slug": "next-greater-element",
        "title": "Next Greater Element",
        "primary_skill": "STACK", "pattern_skills": ["STACK"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 4,
        "statement": "Given an array `nums`, for each element find the next element to its right that is greater than it. If none exists, use -1.",
        "constraints": "1 <= len(nums) <= 10^4",
        "examples": [{"input": "[2,1,2,4,3]", "output": "[4,2,4,-1,-1]", "explanation": "for each element, the first larger one to its right"}],
        "function_name": "next_greater_elements",
        "starter_code": "def next_greater_elements(nums):\n    pass\n",
        "reference_solution": (
            "def next_greater_elements(nums):\n"
            "    result = [-1] * len(nums)\n    stack = []\n"
            "    for i, x in enumerate(nums):\n"
            "        while stack and nums[stack[-1]] < x:\n            result[stack.pop()] = x\n"
            "        stack.append(i)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 1, 2, 4, 3]], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 2, 3, 4]], "hidden": False, "explanation": "strictly increasing"},
            {"args": [[4, 3, 2, 1]], "hidden": True, "explanation": "strictly decreasing -- nothing has a next greater"},
        ],
        "hints": ["A monotonic stack of indices, kept in decreasing value order, is the standard tool here.", "When the current element beats the stack's top, that top index has just found its answer -- pop and record it.", "Every index is pushed once and popped at most once -- O(n) total, not O(n^2)."],
    },
    {
        "slug": "power-fast-exponentiation",
        "title": "Fast Exponentiation",
        "primary_skill": "RECURSION", "pattern_skills": ["RECURSION"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a `base` and a non-negative integer `exp`, compute `base^exp` using divide-and-conquer recursion (not a simple loop).",
        "constraints": "0 <= exp <= 30",
        "examples": [{"input": "base=2, exp=10", "output": "1024", "explanation": "2^10 = 1024"}],
        "function_name": "fast_power",
        "starter_code": "def fast_power(base, exp):\n    pass\n",
        "reference_solution": (
            "def fast_power(base, exp):\n"
            "    if exp == 0:\n        return 1\n"
            "    half = fast_power(base, exp // 2)\n"
            "    if exp % 2 == 0:\n        return half * half\n"
            "    return half * half * base\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [2, 10], "hidden": False, "explanation": "typical case"},
            {"args": [3, 0], "hidden": False, "explanation": "base case: anything to the 0th power is 1"},
            {"args": [5, 3], "hidden": True, "explanation": "odd exponent"},
        ],
        "hints": ["A naive loop multiplies exp times -- O(exp). Can you halve the exponent each recursive call instead?", "`base^exp = (base^(exp//2))^2`, with one extra factor of base if exp is odd.", "This turns O(n) multiplications into O(log n)."],
    },
    {
        "slug": "sum-of-digits",
        "title": "Sum of Digits (Recursive)",
        "primary_skill": "RECURSION", "pattern_skills": ["RECURSION"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a non-negative integer `n`, return the sum of its digits, computed recursively.",
        "constraints": "0 <= n <= 10^9",
        "examples": [{"input": "1234", "output": "10", "explanation": "1+2+3+4 = 10"}],
        "function_name": "sum_of_digits",
        "starter_code": "def sum_of_digits(n):\n    pass\n",
        "reference_solution": "def sum_of_digits(n):\n    if n < 10:\n        return n\n    return n % 10 + sum_of_digits(n // 10)\n",
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [1234], "hidden": False, "explanation": "typical case"},
            {"args": [0], "hidden": False, "explanation": "base case"},
            {"args": [999], "hidden": True, "explanation": "all same digit"},
        ],
        "hints": ["A number's last digit is `n % 10`; the rest is `n // 10`.", "Base case: a single-digit number is its own digit sum.", "Recursive case: last digit plus the digit sum of everything before it."],
    },
    {
        "slug": "min-cost-climbing-stairs",
        "title": "Minimum Cost Climbing Stairs",
        "primary_skill": "DP_BASICS", "pattern_skills": ["DP_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a `cost` array where cost[i] is the cost of stepping on stair i, find the minimum cost to reach the top (one step past the last stair), starting from step 0 or step 1, moving 1 or 2 steps at a time.",
        "constraints": "2 <= len(cost) <= 1000",
        "examples": [{"input": "[10,15,20]", "output": "15", "explanation": "start at step 1 (cost 15), then step 2 past the top"}],
        "function_name": "min_cost_climbing_stairs",
        "starter_code": "def min_cost_climbing_stairs(cost):\n    pass\n",
        "reference_solution": (
            "def min_cost_climbing_stairs(cost):\n"
            "    n = len(cost)\n    dp = [0] * (n + 1)\n"
            "    for i in range(2, n + 1):\n"
            "        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])\n"
            "    return dp[n]\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[10, 15, 20]], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]], "hidden": False, "explanation": "avoiding the expensive steps matters"},
            {"args": [[0, 0, 0, 1]], "hidden": True, "explanation": "free steps at the start"},
        ],
        "hints": ["State: the minimum cost to reach step i (not stepping *on* it, just reaching it).", "Transition: you arrive at step i from i-1 or i-2, paying whichever of those steps' cost you actually stepped on.", "You can start for free at step 0 or step 1 -- both are valid base cases with cost 0 to *reach*."],
    },
    {
        "slug": "maximum-product-subarray",
        "title": "Maximum Product Subarray",
        "primary_skill": "DP_BASICS", "pattern_skills": ["DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given an array `nums`, find the contiguous subarray with the largest product and return that product.",
        "constraints": "1 <= len(nums) <= 2*10^4, can include negative numbers and zero",
        "examples": [{"input": "[2,3,-2,4]", "output": "6", "explanation": "[2,3] has the largest product, 6"}],
        "function_name": "max_product_subarray",
        "starter_code": "def max_product_subarray(nums):\n    pass\n",
        "reference_solution": (
            "def max_product_subarray(nums):\n"
            "    max_so_far = cur_max = cur_min = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        candidates = (x, cur_max * x, cur_min * x)\n"
            "        cur_max = max(candidates)\n        cur_min = min(candidates)\n"
            "        max_so_far = max(max_so_far, cur_max)\n"
            "    return max_so_far\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 3, -2, 4]], "hidden": False, "explanation": "typical case"},
            {"args": [[-2, 0, -1]], "hidden": False, "explanation": "a zero breaks any subarray crossing it"},
            {"args": [[-2, 3, -4]], "hidden": True, "explanation": "two negatives multiply to a large positive"},
        ],
        "hints": ["Unlike max subarray *sum*, a negative number can turn the smallest product into the largest -- you need to track both a running max AND a running min.", "At each step, the new max is the best of: just this element, max*element, or min*element.", "Track the min alongside the max for exactly the negative-flip case."],
    },
    {
        "slug": "last-stone-weight",
        "title": "Last Stone Weight",
        "primary_skill": "HEAP", "pattern_skills": ["HEAP"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 1, "pattern_difficulty": 2,
        "statement": "Given stone weights, repeatedly smash the two heaviest together: if equal, both are destroyed; otherwise the lighter is destroyed and the heavier becomes their difference. Return the weight of the last stone left, or 0 if none remain.",
        "constraints": "1 <= len(stones) <= 30",
        "examples": [{"input": "[2,7,4,1,8,1]", "output": "1", "explanation": "successive smashes leave a single stone of weight 1"}],
        "function_name": "last_stone_weight",
        "starter_code": "def last_stone_weight(stones):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def last_stone_weight(stones):\n"
            "    heap = [-s for s in stones]\n    heapq.heapify(heap)\n"
            "    while len(heap) > 1:\n"
            "        a = -heapq.heappop(heap)\n        b = -heapq.heappop(heap)\n"
            "        if a != b:\n            heapq.heappush(heap, -(a - b))\n"
            "    return -heap[0] if heap else 0\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[2, 7, 4, 1, 8, 1]], "hidden": False, "explanation": "typical case"},
            {"args": [[1]], "hidden": False, "explanation": "single stone, nothing to smash"},
            {"args": [[2, 2]], "hidden": True, "explanation": "equal stones fully destroy each other"},
        ],
        "hints": ["You always need the two *heaviest* stones repeatedly -- a max-heap is built for exactly this.", "Python's heapq is a min-heap, so negate values to simulate a max-heap.", "Push the difference back in (if any) and repeat until at most one stone remains."],
    },
    {
        "slug": "merge-k-sorted-arrays",
        "title": "Merge K Sorted Arrays",
        "primary_skill": "HEAP", "pattern_skills": ["HEAP"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a list of `k` sorted arrays, merge them into one sorted array.",
        "constraints": "1 <= k <= 100, total elements <= 10^4",
        "examples": [{"input": "[[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "all elements merged in sorted order"}],
        "function_name": "merge_k_sorted",
        "starter_code": "def merge_k_sorted(arrays):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def merge_k_sorted(arrays):\n"
            "    heap = []\n"
            "    for i, arr in enumerate(arrays):\n"
            "        if arr:\n            heapq.heappush(heap, (arr[0], i, 0))\n"
            "    result = []\n"
            "    while heap:\n"
            "        val, i, idx = heapq.heappop(heap)\n        result.append(val)\n"
            "        if idx + 1 < len(arrays[i]):\n            heapq.heappush(heap, (arrays[i][idx + 1], i, idx + 1))\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n log k)",
        "test_cases": [
            {"args": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "hidden": False, "explanation": "typical case"},
            {"args": [[[]]], "hidden": False, "explanation": "a single empty array"},
            {"args": [[[1], [0]]], "hidden": True, "explanation": "two single-element arrays"},
        ],
        "hints": ["Merging two sorted lists at a time, k-1 times, works but is not the most efficient approach.", "A min-heap holding 'the current smallest unmerged element from each array' lets you always pull the global minimum next in O(log k).", "Track which array and index each heap entry came from, so you know what to push next after popping it."],
    },
    {
        "slug": "reverse-words-in-string",
        "title": "Reverse Words in a String",
        "primary_skill": "STRINGS", "pattern_skills": ["STRINGS"],
        "difficulty": "medium",
        "concept_difficulty": 1, "implementation_difficulty": 2, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a string `s`, reverse the order of the words. Words are separated by whitespace; collapse multiple spaces and trim leading/trailing spaces in the result.",
        "constraints": "1 <= len(s) <= 10^4",
        "examples": [{"input": '"the sky is blue"', "output": '"blue is sky the"', "explanation": "words reversed, single-spaced"}],
        "function_name": "reverse_words",
        "starter_code": "def reverse_words(s):\n    pass\n",
        "reference_solution": "def reverse_words(s):\n    return ' '.join(reversed(s.split()))\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["the sky is blue"], "hidden": False, "explanation": "typical case"},
            {"args": ["  hello world  "], "hidden": False, "explanation": "leading/trailing spaces"},
            {"args": ["a good   example"], "hidden": True, "explanation": "multiple spaces between words"},
        ],
        "hints": ["`str.split()` with no arguments already collapses whitespace and drops empty tokens.", "Reverse the resulting list of words.", "Join with a single space."],
    },
    {
        "slug": "string-compression",
        "title": "String Compression (Run-Length Encoding)",
        "primary_skill": "STRINGS", "pattern_skills": ["STRINGS"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a string `chars`, compress consecutive runs of the same character into `char` + `count` (omit the count when it's 1). Return the compressed string.",
        "constraints": "1 <= len(chars) <= 2000",
        "examples": [{"input": '"aabcccccaaa"', "output": '"a2bc5a3"', "explanation": "each run encoded as char+count (count omitted when 1)"}],
        "function_name": "compress_string",
        "starter_code": "def compress_string(chars):\n    pass\n",
        "reference_solution": (
            "def compress_string(chars):\n"
            "    result = []\n    i = 0\n    n = len(chars)\n"
            "    while i < n:\n"
            "        j = i\n"
            "        while j < n and chars[j] == chars[i]:\n            j += 1\n"
            "        result.append(chars[i])\n"
            "        if j - i > 1:\n            result.append(str(j - i))\n"
            "        i = j\n"
            "    return ''.join(result)\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["aabcccccaaa"], "hidden": False, "explanation": "typical case"},
            {"args": ["abbbbbbbbbbbb"], "hidden": False, "explanation": "a run longer than 9"},
            {"args": ["abc"], "hidden": True, "explanation": "no repeated characters at all"},
        ],
        "hints": ["Scan for runs of consecutive identical characters using a second pointer.", "A run of length 1 is written as just the character -- no count.", "This is a single left-to-right pass, O(n)."],
    },
    {
        "slug": "middle-of-linked-list",
        "title": "Middle of a Linked List",
        "primary_skill": "LINKED_LIST", "pattern_skills": ["LINKED_LIST"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given the head of a linked list, return the middle node (as a value list from the middle to the end). If there are two middle nodes, return the second one.",
        "constraints": "1 <= number of nodes <= 100",
        "examples": [{"input": "[1,2,3,4,5]", "output": "[3,4,5]", "explanation": "3 is the middle of 5 nodes"}],
        "function_name": "middle_node",
        "starter_code": "# A ListNode class is provided: ListNode(val, next=None)\ndef middle_node(head):\n    pass\n",
        "reference_solution": (
            "def middle_node(head):\n"
            "    slow = head\n    fast = head\n"
            "    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n"
            "    return slow\n"
        ),
        "io_transform": {"args": {"0": "linked_list"}, "result": "linked_list"},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5]], "hidden": False, "explanation": "odd length"},
            {"args": [[1, 2, 3, 4, 5, 6]], "hidden": False, "explanation": "even length -- second middle returned"},
            {"args": [[1]], "hidden": True, "explanation": "single node"},
        ],
        "hints": ["A slow pointer moving 1 step and a fast pointer moving 2 steps will have the fast one finish exactly when the slow one is at the middle.", "This finds the middle in one pass, without first counting the length.", "When fast reaches the end (or one before it), slow is at the answer."],
    },
    {
        "slug": "remove-nth-node-from-end",
        "title": "Remove the Nth Node From the End",
        "primary_skill": "LINKED_LIST", "pattern_skills": ["LINKED_LIST"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given the head of a linked list and an integer `n`, remove the nth node from the end and return the resulting list.",
        "constraints": "1 <= number of nodes <= 30",
        "examples": [{"input": "head=[1,2,3,4,5], n=2", "output": "[1,2,3,5]", "explanation": "the 2nd-from-last node (4) is removed"}],
        "function_name": "remove_nth_from_end",
        "starter_code": "# A ListNode class is provided: ListNode(val, next=None)\ndef remove_nth_from_end(head, n):\n    pass\n",
        "reference_solution": (
            "def remove_nth_from_end(head, n):\n"
            "    dummy = ListNode(0, head)\n    fast = dummy\n    slow = dummy\n"
            "    for _ in range(n):\n        fast = fast.next\n"
            "    while fast.next:\n        fast = fast.next\n        slow = slow.next\n"
            "    slow.next = slow.next.next\n"
            "    return dummy.next\n"
        ),
        "io_transform": {"args": {"0": "linked_list"}, "result": "linked_list"},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5], 2], "hidden": False, "explanation": "typical case"},
            {"args": [[1], 1], "hidden": False, "explanation": "removing the only node"},
            {"args": [[1, 2], 1], "hidden": True, "explanation": "removing the last of two nodes"},
        ],
        "hints": ["A dummy node before the head avoids special-casing 'remove the head itself'.", "Advance a fast pointer n steps first, then move both fast and slow together -- when fast reaches the end, slow is right before the node to remove.", "This finds the target in one pass, without first counting the list's length."],
    },
    {
        "slug": "first-negative-in-every-window",
        "title": "First Negative Number in Every Window",
        "primary_skill": "QUEUE_DEQUE", "pattern_skills": ["QUEUE_DEQUE", "SLIDING_WINDOW"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an array `nums` and window size `k`, return the first negative number in each window of size k (0 if a window has none).",
        "constraints": "1 <= k <= len(nums) <= 10^5",
        "examples": [{"input": "nums=[-8,2,3,-6,10], k=2", "output": "[-8,0,-6,-6]", "explanation": "first negative in each window of size 2"}],
        "function_name": "first_negative_in_window",
        "starter_code": "def first_negative_in_window(nums, k):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def first_negative_in_window(nums, k):\n"
            "    dq = deque()\n    result = []\n"
            "    for i, x in enumerate(nums):\n"
            "        if dq and dq[0] <= i - k:\n            dq.popleft()\n"
            "        if x < 0:\n            dq.append(i)\n"
            "        if i >= k - 1:\n            result.append(nums[dq[0]] if dq else 0)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[-8, 2, 3, -6, 10], 2], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 2, 3], 1], "hidden": False, "explanation": "no negatives at all"},
            {"args": [[12, -1, -7, 8, -15, 30, 16, 28], 3], "hidden": True, "explanation": "longer window with several negatives"},
        ],
        "hints": ["Keep a deque of *indices* of negative numbers currently inside the window, in order.", "Before recording an answer, evict any index from the front that's fallen outside the window.", "The front of the deque, if any, is the first negative in the current window."],
    },
    {
        "slug": "same-tree",
        "title": "Same Tree",
        "primary_skill": "TREES", "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given the roots of two binary trees (level-order form), return True if they are structurally identical with the same node values.",
        "constraints": "0 <= number of nodes <= 100 in each tree",
        "examples": [{"input": "[1,2,3], [1,2,3]", "output": "true", "explanation": "identical structure and values"}],
        "function_name": "is_same_tree",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef is_same_tree(p, q):\n    pass\n",
        "reference_solution": (
            "def is_same_tree(p, q):\n"
            "    if p is None and q is None:\n        return True\n"
            "    if p is None or q is None:\n        return False\n"
            "    if p.val != q.val:\n        return False\n"
            "    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)\n"
        ),
        "io_transform": {"args": {"0": "binary_tree", "1": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3], [1, 2, 3]], "hidden": False, "explanation": "identical trees"},
            {"args": [[1, 2], [1, None, 2]], "hidden": False, "explanation": "same values, different structure"},
            {"args": [[], []], "hidden": True, "explanation": "both empty"},
        ],
        "hints": ["Two empty trees are trivially the same.", "If exactly one is empty, they can't match.", "Otherwise, compare the current values and recurse into both left and right subtrees."],
    },
    {
        "slug": "symmetric-tree",
        "title": "Symmetric Tree",
        "primary_skill": "TREES", "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given the root of a binary tree (level-order form), return True if it is a mirror of itself around its center.",
        "constraints": "0 <= number of nodes <= 1000",
        "examples": [{"input": "[1,2,2,3,4,4,3]", "output": "true", "explanation": "left and right subtrees mirror each other"}],
        "function_name": "is_symmetric",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef is_symmetric(root):\n    pass\n",
        "reference_solution": (
            "def is_symmetric(root):\n"
            "    def mirror(a, b):\n"
            "        if a is None and b is None:\n            return True\n"
            "        if a is None or b is None:\n            return False\n"
            "        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)\n"
            "    return root is None or mirror(root.left, root.right)\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 2, 3, 4, 4, 3]], "hidden": False, "explanation": "symmetric tree"},
            {"args": [[1, 2, 2, None, 3, None, 3]], "hidden": False, "explanation": "not symmetric"},
            {"args": [[]], "hidden": True, "explanation": "empty tree -- trivially symmetric"},
        ],
        "hints": ["This is same-tree's cousin: instead of comparing two separate trees, compare a tree's left subtree against its right subtree, mirrored.", "'Mirrored' means: compare a's left to b's right, and a's right to b's left.", "An empty tree, or one with only a root, is trivially symmetric."],
    },
    {
        "slug": "path-sum",
        "title": "Path Sum",
        "primary_skill": "TREES", "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a binary tree (level-order form) and a target sum, return True if there is a root-to-leaf path whose values sum to the target.",
        "constraints": "0 <= number of nodes <= 5000",
        "examples": [{"input": "[1,2,3], target=5", "output": "false", "explanation": "no root-to-leaf path sums to 5 (paths are 1+2=3 and 1+3=4)"}],
        "function_name": "has_path_sum",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef has_path_sum(root, target_sum):\n    pass\n",
        "reference_solution": (
            "def has_path_sum(root, target_sum):\n"
            "    if root is None:\n        return False\n"
            "    if root.left is None and root.right is None:\n        return root.val == target_sum\n"
            "    remaining = target_sum - root.val\n"
            "    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3], 5], "hidden": False, "explanation": "no path matches"},
            {"args": [[1, 2, 3], 4], "hidden": False, "explanation": "1+3 = 4 matches"},
            {"args": [[], 0], "hidden": True, "explanation": "empty tree -- no path exists"},
        ],
        "hints": ["A leaf is a node with no children -- that's your base case for 'does a path end here successfully?'", "At each node, subtract its value from the target and recurse into the children with the reduced target.", "Only leaf nodes can satisfy the sum -- an internal node matching the target isn't enough."],
    },
    {
        "slug": "validate-bst",
        "title": "Validate a Binary Search Tree",
        "primary_skill": "BST", "pattern_skills": ["BST", "RECURSION"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given a binary tree (level-order form), return True if it satisfies the binary search tree property at every node.",
        "constraints": "1 <= number of nodes <= 10^4",
        "examples": [{"input": "[5,1,4,None,None,3,6]", "output": "false", "explanation": "3 is in 5's right subtree but is less than 5"}],
        "function_name": "is_valid_bst",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef is_valid_bst(root):\n    pass\n",
        "reference_solution": (
            "def is_valid_bst(root):\n"
            "    def helper(node, low, high):\n"
            "        if node is None:\n            return True\n"
            "        if not (low < node.val < high):\n            return False\n"
            "        return helper(node.left, low, node.val) and helper(node.right, node.val, high)\n"
            "    return helper(root, float('-inf'), float('inf'))\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 1, 3]], "hidden": False, "explanation": "valid BST"},
            {"args": [[5, 1, 4, None, None, 3, 6]], "hidden": False, "explanation": "invalid -- 3 violates the ancestor 5"},
            {"args": [[]], "hidden": True, "explanation": "empty tree is trivially valid"},
        ],
        "hints": ["Checking only `left.val < node.val < right.val` locally is not enough -- a node must respect *every* ancestor's bound, not just its parent.", "Pass down a valid (low, high) range that narrows as you descend left or right.", "A node's value must strictly fall within the range inherited from all its ancestors."],
    },
    {
        "slug": "kth-smallest-in-bst",
        "title": "Kth Smallest Element in a BST",
        "primary_skill": "BST", "pattern_skills": ["BST"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given the root of a binary search tree (level-order form) and an integer `k`, return the kth smallest value in the tree.",
        "constraints": "1 <= k <= number of nodes <= 10^4",
        "examples": [{"input": "[3,1,4,None,2], k=1", "output": "1", "explanation": "1 is the smallest value in the tree"}],
        "function_name": "kth_smallest",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef kth_smallest(root, k):\n    pass\n",
        "reference_solution": (
            "def kth_smallest(root, k):\n"
            "    result = []\n"
            "    def inorder(node):\n"
            "        if node is None or len(result) >= k:\n            return\n"
            "        inorder(node.left)\n"
            "        if len(result) < k:\n            result.append(node.val)\n"
            "        inorder(node.right)\n"
            "    inorder(root)\n    return result[-1]\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(k)",
        "test_cases": [
            {"args": [[3, 1, 4, None, 2], 1], "hidden": False, "explanation": "typical case"},
            {"args": [[5, 3, 6, 2, 4, None, None, 1], 3], "hidden": False, "explanation": "larger tree"},
            {"args": [[1], 1], "hidden": True, "explanation": "single-node tree"},
        ],
        "hints": ["Inorder traversal (left, root, right) visits a BST's values in sorted order -- for free.", "You don't need to visit the whole tree -- stop as soon as you've collected k values.", "The kth value collected during an inorder traversal is the answer."],
    },
    {
        "slug": "number-of-islands",
        "title": "Number of Islands",
        "primary_skill": "GRAPHS", "pattern_skills": ["GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a 2D grid of 1s (land) and 0s (water), return the number of islands (groups of land connected 4-directionally).",
        "constraints": "1 <= rows, cols <= 300",
        "examples": [{"input": "[[1,1,0],[0,1,0],[1,0,1]]", "output": "3", "explanation": "one 3-cell island, one isolated 1"}],
        "function_name": "num_islands",
        "starter_code": "def num_islands(grid):\n    pass\n",
        "reference_solution": (
            "def num_islands(grid):\n"
            "    if not grid:\n        return 0\n"
            "    grid = [row[:] for row in grid]\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    def dfs(r, c):\n"
            "        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:\n            return\n"
            "        grid[r][c] = 0\n"
            "        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)\n"
            "    count = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 1:\n                count += 1\n                dfs(r, c)\n"
            "    return count\n"
        ),
        "expected_complexity": "O(rows * cols)",
        "test_cases": [
            {"args": [[[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]]], "hidden": False, "explanation": "three separate islands"},
            {"args": [[[1, 1, 1], [0, 1, 0], [1, 1, 1]]], "hidden": False, "explanation": "one connected island"},
            {"args": [[[0, 0], [0, 0]]], "hidden": True, "explanation": "no land at all"},
        ],
        "hints": ["Think of the grid as an implicit graph: each land cell is a node, connected to its 4-directional land neighbors.", "Whenever you find an unvisited land cell, that's a brand new island -- flood-fill (DFS/BFS) it to mark the whole island visited, then count it once.", "Sinking visited land to 0 as you go is a simple way to avoid a separate visited set."],
    },
    {
        "slug": "flood-fill",
        "title": "Flood Fill",
        "primary_skill": "GRAPHS", "pattern_skills": ["GRAPHS"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 1, "pattern_difficulty": 2,
        "statement": "Given an image (2D grid of colors), a starting pixel `(sr, sc)`, and a `new_color`, flood-fill all 4-directionally connected pixels of the same original color as the start, and return the modified image.",
        "constraints": "1 <= rows, cols <= 50",
        "examples": [{"input": "image=[[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, new_color=2", "output": "[[2,2,2],[2,2,0],[2,0,1]]", "explanation": "all connected 1s from (1,1) become 2"}],
        "function_name": "flood_fill",
        "starter_code": "def flood_fill(image, sr, sc, new_color):\n    pass\n",
        "reference_solution": (
            "def flood_fill(image, sr, sc, new_color):\n"
            "    image = [row[:] for row in image]\n"
            "    rows, cols = len(image), len(image[0])\n"
            "    old_color = image[sr][sc]\n"
            "    if old_color == new_color:\n        return image\n"
            "    def dfs(r, c):\n"
            "        if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != old_color:\n            return\n"
            "        image[r][c] = new_color\n"
            "        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)\n"
            "    dfs(sr, sc)\n    return image\n"
        ),
        "expected_complexity": "O(rows * cols)",
        "test_cases": [
            {"args": [[[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2], "hidden": False, "explanation": "typical case"},
            {"args": [[[0, 0, 0], [0, 0, 0]], 0, 0, 0], "hidden": False, "explanation": "new color equals old color -- no change"},
            {"args": [[[1]], 0, 0, 5], "hidden": True, "explanation": "single-pixel image"},
        ],
        "hints": ["This is the same DFS-flood-fill idea as counting islands, but starting from one given cell instead of scanning the whole grid.", "Guard against the no-op case where new_color already equals the starting color -- otherwise you could recurse forever.", "Recolor as you visit, and recurse into the 4-directional neighbors that still match the original color."],
    },
    {
        "slug": "jump-game",
        "title": "Jump Game",
        "primary_skill": "GREEDY", "pattern_skills": ["GREEDY"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an array `nums` where nums[i] is the maximum jump length from index i, return True if you can reach the last index starting from index 0.",
        "constraints": "1 <= len(nums) <= 10^4",
        "examples": [{"input": "[2,3,1,1,4]", "output": "true", "explanation": "jump 1 step then 3 steps to the last index"}],
        "function_name": "can_jump",
        "starter_code": "def can_jump(nums):\n    pass\n",
        "reference_solution": (
            "def can_jump(nums):\n"
            "    max_reach = 0\n"
            "    for i, x in enumerate(nums):\n"
            "        if i > max_reach:\n            return False\n"
            "        max_reach = max(max_reach, i + x)\n"
            "    return True\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 3, 1, 1, 4]], "hidden": False, "explanation": "reachable"},
            {"args": [[3, 2, 1, 0, 4]], "hidden": False, "explanation": "gets stuck at the 0"},
            {"args": [[0]], "hidden": True, "explanation": "already at the last index"},
        ],
        "hints": ["You don't need to try every combination of jumps -- just track the farthest index reachable so far.", "If you ever reach an index beyond the farthest-reachable point, you're stuck.", "Greedy works here because 'farthest reachable so far' only ever needs to grow, never needs reconsidering."],
    },
    {
        "slug": "assign-cookies",
        "title": "Assign Cookies",
        "primary_skill": "GREEDY", "pattern_skills": ["GREEDY"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given children's greed factors `g` and cookie sizes `s`, assign at most one cookie per child (a cookie satisfies a child if its size >= their greed factor). Return the maximum number of content children.",
        "constraints": "1 <= len(g), len(s) <= 3*10^4",
        "examples": [{"input": "g=[1,2,3], s=[1,1]", "output": "1", "explanation": "only one cookie is big enough for any child"}],
        "function_name": "find_content_children",
        "starter_code": "def find_content_children(g, s):\n    pass\n",
        "reference_solution": (
            "def find_content_children(g, s):\n"
            "    g = sorted(g); s = sorted(s)\n"
            "    i = j = 0; count = 0\n"
            "    while i < len(g) and j < len(s):\n"
            "        if s[j] >= g[i]:\n            count += 1; i += 1; j += 1\n"
            "        else:\n            j += 1\n"
            "    return count\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[1, 2, 3], [1, 1]], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 2], [1, 2, 3]], "hidden": False, "explanation": "more cookies than children"},
            {"args": [[10, 9, 8, 7], [5, 6, 7, 8]], "hidden": True, "explanation": "greedy children, small cookies"},
        ],
        "hints": ["Sort both the greed factors and the cookie sizes.", "Greedily try to satisfy the least-greedy child with the smallest cookie that's big enough for them.", "If a cookie isn't big enough for the least-greedy remaining child, it isn't big enough for anyone left -- discard it."],
    },
    {
        "slug": "combination-sum",
        "title": "Combination Sum",
        "primary_skill": "BACKTRACKING", "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given distinct positive integers `candidates` and a `target`, return all unique combinations where the chosen numbers (each usable unlimited times) sum to target.",
        "constraints": "1 <= len(candidates) <= 30, 1 <= target <= 40",
        "examples": [{"input": "candidates=[2,3,6,7], target=7", "output": "[[2,2,3],[7]]", "explanation": "two ways to reach 7"}],
        "function_name": "combination_sum",
        "starter_code": "def combination_sum(candidates, target):\n    pass\n",
        "reference_solution": (
            "def combination_sum(candidates, target):\n"
            "    candidates = sorted(candidates)\n    result = []\n"
            "    def backtrack(start, remaining, path):\n"
            "        if remaining == 0:\n            result.append(path[:])\n            return\n"
            "        for i in range(start, len(candidates)):\n"
            "            if candidates[i] > remaining:\n                break\n"
            "            path.append(candidates[i])\n            backtrack(i, remaining - candidates[i], path)\n            path.pop()\n"
            "    backtrack(0, target, [])\n    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(2^target) worst case",
        "test_cases": [
            {"args": [[2, 3, 6, 7], 7], "hidden": False, "explanation": "typical case"},
            {"args": [[2, 3, 5], 8], "hidden": False, "explanation": "several valid combinations"},
            {"args": [[2], 1], "hidden": True, "explanation": "no combination possible"},
        ],
        "hints": ["Since each number can be reused, the recursive call for 'include this number' doesn't advance past it -- only 'move to the next candidate' does.", "Sorting first lets you stop early once a candidate exceeds the remaining target.", "Remember to undo (`path.pop()`) after each recursive call, and copy the path when recording a complete combination."],
    },
    {
        "slug": "letter-combinations-phone-number",
        "title": "Letter Combinations of a Phone Number",
        "primary_skill": "BACKTRACKING", "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a string of digits 2-9, return all possible letter combinations the digits could represent on a phone keypad, in any order.",
        "constraints": "0 <= len(digits) <= 4",
        "examples": [{"input": '"23"', "output": '["ad","ae","af","bd","be","bf","cd","ce","cf"]', "explanation": "2->abc, 3->def, all combinations"}],
        "function_name": "letter_combinations",
        "starter_code": "def letter_combinations(digits):\n    pass\n",
        "reference_solution": (
            "def letter_combinations(digits):\n"
            "    if not digits:\n        return []\n"
            "    mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}\n"
            "    result = ['']\n"
            "    for d in digits:\n"
            "        letters = mapping[d]\n"
            "        result = [prefix + letter for prefix in result for letter in letters]\n"
            "    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(4^n)",
        "test_cases": [
            {"args": ["23"], "hidden": False, "explanation": "typical case"},
            {"args": [""], "hidden": False, "explanation": "empty input -- no combinations"},
            {"args": ["2"], "hidden": True, "explanation": "single digit"},
        ],
        "hints": ["This is a backtracking/combinatorial expansion problem even without an explicit recursive function -- building up combinations digit by digit works too.", "For each new digit, every existing partial combination branches into one new combination per letter on that digit's key.", "An empty input has no digits to map, so the answer is an empty list, not a list containing an empty string."],
    },
    {
        "slug": "power-of-two",
        "title": "Power of Two",
        "primary_skill": "BIT_MANIPULATION", "pattern_skills": ["BIT_MANIPULATION"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 1, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given an integer `n`, return True if it is a power of two.",
        "constraints": "-2^31 <= n <= 2^31 - 1",
        "examples": [{"input": "16", "output": "true", "explanation": "16 = 2^4"}],
        "function_name": "is_power_of_two",
        "starter_code": "def is_power_of_two(n):\n    pass\n",
        "reference_solution": "def is_power_of_two(n):\n    return n > 0 and (n & (n - 1)) == 0\n",
        "expected_complexity": "O(1)",
        "test_cases": [
            {"args": [1], "hidden": False, "explanation": "2^0 = 1"},
            {"args": [16], "hidden": False, "explanation": "typical case"},
            {"args": [0], "hidden": True, "explanation": "zero is not a power of two"},
        ],
        "hints": ["A power of two in binary is a single 1-bit followed by zeroes (e.g. 8 = 1000).", "`n & (n-1)` clears the lowest set bit -- for a power of two, that leaves 0.", "Don't forget to exclude non-positive numbers first."],
    },
    {
        "slug": "reverse-bits",
        "title": "Reverse Bits",
        "primary_skill": "BIT_MANIPULATION", "pattern_skills": ["BIT_MANIPULATION"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a 32-bit unsigned integer `n`, return the integer obtained by reversing the order of its bits.",
        "constraints": "0 <= n <= 2^32 - 1",
        "examples": [{"input": "1", "output": "2147483648", "explanation": "bit 0 set becomes bit 31 set"}],
        "function_name": "reverse_bits_32",
        "starter_code": "def reverse_bits_32(n):\n    pass\n",
        "reference_solution": (
            "def reverse_bits_32(n):\n"
            "    result = 0\n"
            "    for i in range(32):\n"
            "        bit = (n >> i) & 1\n        result |= bit << (31 - i)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(1)",
        "test_cases": [
            {"args": [43261596], "hidden": False, "explanation": "classic example"},
            {"args": [4294967293], "hidden": False, "explanation": "a number near the 32-bit max"},
            {"args": [1], "hidden": True, "explanation": "smallest possible set bit"},
        ],
        "hints": ["Consider each of the 32 bit positions independently.", "Bit i of the input becomes bit (31-i) of the output.", "Extract each bit with `(n >> i) & 1`, then place it with `bit << (31 - i)`, OR-ing all 32 placements together."],
    },
    {
        "slug": "partition-equal-subset-sum",
        "title": "Partition Equal Subset Sum",
        "primary_skill": "DP_KNAPSACK", "pattern_skills": ["DP_KNAPSACK"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given an array `nums`, return True if it can be split into two subsets with equal sum.",
        "constraints": "1 <= len(nums) <= 200",
        "examples": [{"input": "[1,5,11,5]", "output": "true", "explanation": "[1,5,5] and [11] both sum to 11"}],
        "function_name": "can_partition",
        "starter_code": "def can_partition(nums):\n    pass\n",
        "reference_solution": (
            "def can_partition(nums):\n"
            "    total = sum(nums)\n"
            "    if total % 2 != 0:\n        return False\n"
            "    target = total // 2\n"
            "    dp = [False] * (target + 1)\n    dp[0] = True\n"
            "    for x in nums:\n"
            "        for c in range(target, x - 1, -1):\n"
            "            if dp[c - x]:\n                dp[c] = True\n"
            "    return dp[target]\n"
        ),
        "expected_complexity": "O(n * sum)",
        "test_cases": [
            {"args": [[1, 5, 11, 5]], "hidden": False, "explanation": "typical case"},
            {"args": [[1, 2, 3, 5]], "hidden": False, "explanation": "impossible to split evenly"},
            {"args": [[1, 1]], "hidden": True, "explanation": "smallest possible even split"},
        ],
        "hints": ["An odd total sum can never be split into two equal halves -- check that first.", "This reduces to: can some subset sum to exactly half the total? That's the 0/1 knapsack subset-sum shape.", "dp[c] tracks whether some subset of the numbers seen so far sums to exactly c."],
    },
    {
        "slug": "is-subsequence",
        "title": "Is Subsequence",
        "primary_skill": "DP_STRING", "pattern_skills": ["DP_STRING", "TWO_POINTER"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 2,
        "statement": "Given strings `s` and `t`, return True if `s` is a subsequence of `t` (characters of s appear in t in the same order, not necessarily contiguous).",
        "constraints": "0 <= len(s) <= 100, 0 <= len(t) <= 10^4",
        "examples": [{"input": 's="abc", t="ahbgdc"', "output": "true", "explanation": "a, b, c appear in order in t"}],
        "function_name": "is_subsequence",
        "starter_code": "def is_subsequence(s, t):\n    pass\n",
        "reference_solution": "def is_subsequence(s, t):\n    it = iter(t)\n    return all(c in it for c in s)\n",
        "expected_complexity": "O(len(t))",
        "test_cases": [
            {"args": ["abc", "ahbgdc"], "hidden": False, "explanation": "typical case"},
            {"args": ["axc", "ahbgdc"], "hidden": False, "explanation": "not a subsequence"},
            {"args": ["", "abc"], "hidden": True, "explanation": "an empty string is a subsequence of anything"},
        ],
        "hints": ["This is a simpler cousin of full LCS -- you only need to confirm s can be found in order, not compute a general alignment.", "Two pointers, one per string, work: advance the t-pointer always, advance the s-pointer only on a match.", "If the s-pointer reaches the end, every character was found in order."],
    },
    {
        "slug": "sum-of-array",
        "title": "Sum of an Array",
        "primary_skill": "PROGRAMMING_BASICS", "pattern_skills": ["PROGRAMMING_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given an array of integers `nums`, return the sum of all its elements.",
        "constraints": "0 <= len(nums) <= 1000",
        "examples": [{"input": "[1,2,3]", "output": "6", "explanation": "1+2+3 = 6"}],
        "function_name": "sum_array",
        "starter_code": "def sum_array(nums):\n    pass\n",
        "reference_solution": "def sum_array(nums):\n    total = 0\n    for x in nums:\n        total += x\n    return total\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3]], "hidden": False, "explanation": "typical case"},
            {"args": [[]], "hidden": False, "explanation": "empty array"},
            {"args": [[-1, 1]], "hidden": True, "explanation": "values that cancel out"},
        ],
        "hints": ["This is exactly the trace-table exercise from the Programming Foundations lesson.", "Start a running total at 0, then add each element as you go.", "This is your first real loop-with-an-accumulator pattern -- it appears everywhere in DSA."],
    },
    {
        "slug": "count-vowels",
        "title": "Count Vowels in a String",
        "primary_skill": "PROGRAMMING_BASICS", "pattern_skills": ["PROGRAMMING_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given a string `s`, return the number of vowels (a, e, i, o, u, case-insensitive) it contains.",
        "constraints": "0 <= len(s) <= 1000",
        "examples": [{"input": '"hello world"', "output": "3", "explanation": "e, o, o are vowels"}],
        "function_name": "count_vowels",
        "starter_code": "def count_vowels(s):\n    pass\n",
        "reference_solution": "def count_vowels(s):\n    count = 0\n    for c in s:\n        if c.lower() in 'aeiou':\n            count += 1\n    return count\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["hello world"], "hidden": False, "explanation": "typical case"},
            {"args": ["xyz"], "hidden": False, "explanation": "no vowels"},
            {"args": ["AEIOU"], "hidden": True, "explanation": "uppercase vowels"},
        ],
        "hints": ["Loop through each character once.", "Normalize case before checking -- 'A' and 'a' should both count.", "Check membership in the string 'aeiou' rather than five separate comparisons."],
    },
]
