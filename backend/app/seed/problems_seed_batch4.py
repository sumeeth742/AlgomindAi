"""
Batch 4: fills real gaps in per-skill problem counts (Trie had zero problems;
Prefix Sum, Knapsack, String DP, Greedy, and Two Pointer each had only 3) --
picked from the skill's own weakest-covered techniques, not arbitrarily.
Every reference solution here is executed for real against its own test
cases by seed_all.py's `_run_reference` before being stored, same as every
other problem in this repo -- no expected output below is hand-typed.
"""

PROBLEMS_BATCH4 = [
    {
        "slug": "trie-insert-search",
        "title": "Trie: Insert and Search Words",
        "primary_skill": "TRIE", "pattern_skills": ["TRIE"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": (
            "Insert every word in `words` into a trie, then answer each query in `queries`: does the query "
            "exactly match one of the inserted words? Return a list of booleans, one per query."
        ),
        "constraints": "0 <= len(words), len(queries) <= 10^4, lowercase letters only",
        "examples": [{"input": "words=['cat','car','dog'], queries=['cat','ca','dog','do']", "output": "[true,false,true,false]", "explanation": "'ca' and 'do' are prefixes but not inserted whole words"}],
        "function_name": "trie_search",
        "starter_code": "def trie_search(words, queries):\n    pass\n",
        "reference_solution": (
            "def trie_search(words, queries):\n"
            "    root = {}\n"
            "    END = \"$\"\n"
            "    for w in words:\n"
            "        node = root\n"
            "        for ch in w:\n"
            "            node = node.setdefault(ch, {})\n"
            "        node[END] = True\n"
            "    result = []\n"
            "    for q in queries:\n"
            "        node = root\n"
            "        ok = True\n"
            "        for ch in q:\n"
            "            if ch not in node:\n"
            "                ok = False\n"
            "                break\n"
            "            node = node[ch]\n"
            "        result.append(ok and END in node)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [["cat", "car", "dog"], ["cat", "ca", "dog", "do"]], "hidden": False, "explanation": "exact words pass, prefixes fail"},
            {"args": [[], ["a"]], "hidden": False, "explanation": "empty trie"},
            {"args": [["a"], ["a", "aa", ""]], "hidden": True, "explanation": "single-char word, empty query"},
            {"args": [["apple", "app"], ["app", "apple", "appl"]], "hidden": True, "explanation": "one word is a prefix of another"},
        ],
        "hints": [
            "Checking every word against every query with string comparisons is wasteful once there are many words -- a trie lets every query walk down in time proportional to its own length.",
            "Build a nested dict of dicts: each character advances one level deeper. Mark the end of a real word with a special sentinel key that can't collide with a letter.",
            "A query is a real match only if you can walk every one of its characters down the trie AND the node you land on carries the end-of-word marker -- reaching a valid prefix isn't enough.",
        ],
    },
    {
        "slug": "trie-count-words-with-prefix",
        "title": "Trie: Count Words With a Given Prefix",
        "primary_skill": "TRIE", "pattern_skills": ["TRIE"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given `words` and a list of `prefixes`, return, for each prefix, how many words in `words` start "
            "with that prefix."
        ),
        "constraints": "1 <= len(words), len(prefixes) <= 10^4",
        "examples": [{"input": "words=['apple','app','apricot','banana'], prefixes=['app','apr','ban','xyz']", "output": "[2,1,1,0]", "explanation": "'apple' and 'app' both start with 'app'"}],
        "function_name": "count_words_with_prefix",
        "starter_code": "def count_words_with_prefix(words, prefixes):\n    pass\n",
        "reference_solution": (
            "def count_words_with_prefix(words, prefixes):\n"
            "    root = {}\n"
            "    COUNT = \"#\"\n"
            "    for w in words:\n"
            "        node = root\n"
            "        node[COUNT] = node.get(COUNT, 0) + 1\n"
            "        for ch in w:\n"
            "            node = node.setdefault(ch, {})\n"
            "            node[COUNT] = node.get(COUNT, 0) + 1\n"
            "    result = []\n"
            "    for p in prefixes:\n"
            "        node = root\n"
            "        ok = True\n"
            "        for ch in p:\n"
            "            if ch not in node:\n"
            "                ok = False\n"
            "                break\n"
            "            node = node[ch]\n"
            "        result.append(node.get(COUNT, 0) if ok else 0)\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [["apple", "app", "apricot", "banana"], ["app", "apr", "ban", "xyz"]], "hidden": False, "explanation": "typical mixed prefixes"},
            {"args": [["a", "a", "a"], ["a"]], "hidden": False, "explanation": "duplicate words all counted"},
            {"args": [["cat"], ["c", "ca", "cat", "cats"]], "hidden": True, "explanation": "prefix longer than the only word"},
        ],
        "hints": [
            "Re-scanning the whole word list for every prefix is O(words * prefixes * length) -- too slow if either list is large.",
            "Instead, count once while building the trie: increment a counter at every node you pass through while inserting each word, since every node on that path is a prefix of the word.",
            "Answering a prefix query is then just walking down that many characters and reading off the counter you already stored -- no per-query rescanning of `words` needed.",
        ],
    },
    {
        "slug": "replace-words-trie",
        "title": "Replace Words With Their Shortest Root",
        "primary_skill": "TRIE", "pattern_skills": ["TRIE"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given a list of root words `roots` and a space-separated `sentence`, replace every word in the "
            "sentence with the shortest root in `roots` that is a prefix of it. A word with no matching root "
            "stays unchanged. Return the resulting sentence."
        ),
        "constraints": "1 <= len(roots) <= 1000, sentence has at most 1000 words, lowercase letters only",
        "examples": [{"input": "roots=['cat','bat','rat'], sentence='the cattle was rattled by the battery'", "output": "'the cat was rat by the bat'", "explanation": "each long word is replaced by its shortest matching root"}],
        "function_name": "replace_words",
        "starter_code": "def replace_words(roots, sentence):\n    pass\n",
        "reference_solution": (
            "def replace_words(roots, sentence):\n"
            "    trie = {}\n"
            "    END = \"$\"\n"
            "    for r in roots:\n"
            "        node = trie\n"
            "        for ch in r:\n"
            "            node = node.setdefault(ch, {})\n"
            "        node[END] = True\n"
            "\n"
            "    def shortest_root(word):\n"
            "        node = trie\n"
            "        prefix = \"\"\n"
            "        for ch in word:\n"
            "            if ch not in node:\n"
            "                return word\n"
            "            prefix += ch\n"
            "            node = node[ch]\n"
            "            if END in node:\n"
            "                return prefix\n"
            "        return word\n"
            "\n"
            "    return \" \".join(shortest_root(w) for w in sentence.split())\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [["cat", "bat", "rat"], "the cattle was rattled by the battery"], "hidden": False, "explanation": "classic replace-words example"},
            {"args": [["a", "b", "c"], "aadsfasf absfasf acbfnsd acbfnsd"], "hidden": False, "explanation": "single-letter roots match everything"},
            {"args": [["ab"], "abc ab a"], "hidden": True, "explanation": "'a' has no matching root and stays unchanged"},
        ],
        "hints": [
            "Trying every root against every word with string.startswith is O(words * roots * length) -- a trie of the roots avoids re-scanning the whole root list per word.",
            "Insert all the roots into a trie. For each sentence word, walk down the trie one character at a time.",
            "The moment you reach a node marked as the end of a root, stop and use that prefix -- it's guaranteed to be the *shortest* matching root since you stopped at the first one found.",
        ],
    },
    {
        "slug": "subarray-sums-divisible-by-k",
        "title": "Subarray Sums Divisible by K",
        "primary_skill": "ARRAYS_PREFIX_SUM", "pattern_skills": ["ARRAYS_PREFIX_SUM"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": "Given an integer array `nums` and an integer `k`, return the number of (contiguous) subarrays whose sum is divisible by `k`.",
        "constraints": "1 <= len(nums) <= 3*10^4, 2 <= k <= 10^4",
        "examples": [{"input": "nums=[4,5,0,-2,-3,1], k=5", "output": "7", "explanation": "7 subarrays have a sum that's a multiple of 5"}],
        "function_name": "subarrays_div_by_k",
        "starter_code": "def subarrays_div_by_k(nums, k):\n    pass\n",
        "reference_solution": (
            "def subarrays_div_by_k(nums, k):\n"
            "    count = {0: 1}\n"
            "    running = 0\n"
            "    total = 0\n"
            "    for x in nums:\n"
            "        running = (running + x) % k\n"
            "        total += count.get(running, 0)\n"
            "        count[running] = count.get(running, 0) + 1\n"
            "    return total\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[4, 5, 0, -2, -3, 1], 5], "hidden": False, "explanation": "classic example with negative numbers"},
            {"args": [[5], 9], "hidden": False, "explanation": "no subarray divisible"},
            {"args": [[0, 0, 0], 5], "hidden": True, "explanation": "every subarray of zeroes is divisible by anything"},
        ],
        "hints": [
            "Checking every subarray's sum directly is O(n^2) -- there's a way to answer this in one pass.",
            "Two prefix sums with the *same remainder mod k* mean the subarray between them sums to a multiple of k.",
            "Keep a running remainder and a hashmap counting how many times each remainder has been seen so far (start the count at {0: 1} for the empty prefix); add that count every step.",
        ],
    },
    {
        "slug": "product-of-array-except-self",
        "title": "Product of Array Except Self",
        "primary_skill": "ARRAYS_PREFIX_SUM", "pattern_skills": ["ARRAYS_PREFIX_SUM"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given an array `nums`, return an array `answer` where `answer[i]` is the product of every element "
            "except `nums[i]`, without using division."
        ),
        "constraints": "2 <= len(nums) <= 10^5",
        "examples": [{"input": "[1,2,3,4]", "output": "[24,12,8,6]", "explanation": "e.g. answer[0] = 2*3*4 = 24"}],
        "function_name": "product_except_self",
        "starter_code": "def product_except_self(nums):\n    pass\n",
        "reference_solution": (
            "def product_except_self(nums):\n"
            "    n = len(nums)\n"
            "    result = [1] * n\n"
            "    left = 1\n"
            "    for i in range(n):\n"
            "        result[i] = left\n"
            "        left *= nums[i]\n"
            "    right = 1\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        result[i] *= right\n"
            "        right *= nums[i]\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4]], "hidden": False, "explanation": "typical case, no zeroes"},
            {"args": [[-1, 1, 0, -3, 3]], "hidden": False, "explanation": "contains a zero"},
            {"args": [[0, 0]], "hidden": True, "explanation": "two zeroes -- every product is 0"},
        ],
        "hints": [
            "Dividing the total product by nums[i] breaks the moment any element is 0, and the problem forbids division anyway.",
            "answer[i] is exactly (product of everything to i's left) times (product of everything to i's right).",
            "Build the left-products in one left-to-right pass, then multiply in the right-products during a second right-to-left pass over the same output array.",
        ],
    },
    {
        "slug": "coin-change-combinations",
        "title": "Coin Change II (Count Combinations)",
        "primary_skill": "DP_KNAPSACK", "pattern_skills": ["DP_KNAPSACK"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": (
            "Given a target `amount` and an unlimited supply of each denomination in `coins`, return the number "
            "of distinct combinations of coins that add up to `amount`. Order doesn't matter -- {1,2} and {2,1} "
            "count as the same combination."
        ),
        "constraints": "0 <= amount <= 5000, 1 <= len(coins) <= 300",
        "examples": [{"input": "amount=5, coins=[1,2,5]", "output": "4", "explanation": "{5}, {1,1,1,1,1}, {1,1,1,2}, {1,2,2}"}],
        "function_name": "coin_change_combinations",
        "starter_code": "def coin_change_combinations(amount, coins):\n    pass\n",
        "reference_solution": (
            "def coin_change_combinations(amount, coins):\n"
            "    dp = [0] * (amount + 1)\n"
            "    dp[0] = 1\n"
            "    for c in coins:\n"
            "        for a in range(c, amount + 1):\n"
            "            dp[a] += dp[a - c]\n"
            "    return dp[amount]\n"
        ),
        "expected_complexity": "O(amount * len(coins))",
        "test_cases": [
            {"args": [5, [1, 2, 5]], "hidden": False, "explanation": "classic example"},
            {"args": [3, [2]], "hidden": False, "explanation": "impossible -- no way to make 3 from only 2s"},
            {"args": [0, [1, 2, 3]], "hidden": True, "explanation": "amount 0 has exactly one combination: use nothing"},
        ],
        "hints": [
            "This is different from 'minimum coins' -- you're counting combinations, and order must not matter (don't double-count {1,2} and {2,1}).",
            "Iterate coins in the OUTER loop and amounts in the inner loop -- that ordering guarantees each combination is only ever built in one relative coin order.",
            "dp[a] += dp[a - c] for each coin c, processed one coin at a time across the whole amount range before moving to the next coin.",
        ],
    },
    {
        "slug": "target-sum",
        "title": "Target Sum (Assign +/- Signs)",
        "primary_skill": "DP_KNAPSACK", "pattern_skills": ["DP_KNAPSACK"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": (
            "Given an array `nums` and an integer `target`, you may place a '+' or '-' sign in front of each "
            "number. Return the number of ways to assign signs so the resulting expression evaluates to `target`."
        ),
        "constraints": "1 <= len(nums) <= 20, 0 <= nums[i] <= 1000",
        "examples": [{"input": "nums=[1,1,1,1,1], target=3", "output": "5", "explanation": "5 different sign assignments sum to 3"}],
        "function_name": "find_target_sum_ways",
        "starter_code": "def find_target_sum_ways(nums, target):\n    pass\n",
        "reference_solution": (
            "def find_target_sum_ways(nums, target):\n"
            "    dp = {0: 1}\n"
            "    for x in nums:\n"
            "        ndp = {}\n"
            "        for s, c in dp.items():\n"
            "            ndp[s + x] = ndp.get(s + x, 0) + c\n"
            "            ndp[s - x] = ndp.get(s - x, 0) + c\n"
            "        dp = ndp\n"
            "    return dp.get(target, 0)\n"
        ),
        "expected_complexity": "O(n * sum(nums))",
        "test_cases": [
            {"args": [[1, 1, 1, 1, 1], 3], "hidden": False, "explanation": "classic example"},
            {"args": [[1], 1], "hidden": False, "explanation": "single element, only + works"},
            {"args": [[1], 2], "hidden": True, "explanation": "unreachable target -- zero ways"},
        ],
        "hints": [
            "Trying every one of the 2^n sign combinations directly works but blows up fast -- this is really a knapsack in disguise.",
            "Track a running distribution of 'every achievable sum so far and how many ways reach it', updating it one number at a time.",
            "For each number, every existing achievable sum branches into two new sums: one with +x, one with -x. A hashmap from sum -> count of ways handles negative sums cleanly.",
        ],
    },
    {
        "slug": "longest-palindromic-subsequence",
        "title": "Longest Palindromic Subsequence",
        "primary_skill": "DP_STRING", "pattern_skills": ["DP_STRING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": "Given a string `s`, return the length of the longest subsequence of `s` that is also a palindrome (characters don't need to be contiguous).",
        "constraints": "1 <= len(s) <= 1000",
        "examples": [{"input": "'bbbab'", "output": "4", "explanation": "'bbbb' is a palindromic subsequence of length 4"}],
        "function_name": "longest_palindromic_subsequence",
        "starter_code": "def longest_palindromic_subsequence(s):\n    pass\n",
        "reference_solution": (
            "def longest_palindromic_subsequence(s):\n"
            "    n = len(s)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    dp = [[0] * n for _ in range(n)]\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        dp[i][i] = 1\n"
            "        for j in range(i + 1, n):\n"
            "            if s[i] == s[j]:\n"
            "                dp[i][j] = dp[i + 1][j - 1] + 2\n"
            "            else:\n"
            "                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])\n"
            "    return dp[0][n - 1]\n"
        ),
        "expected_complexity": "O(n^2)",
        "test_cases": [
            {"args": ["bbbab"], "hidden": False, "explanation": "classic example"},
            {"args": ["cbbd"], "hidden": False, "explanation": "answer is 'bb', length 2"},
            {"args": ["a"], "hidden": True, "explanation": "single character is its own palindrome"},
        ],
        "hints": [
            "This is exactly the Longest Common Subsequence of the string with its own reverse -- but you can also solve it directly with an interval DP.",
            "Define dp[i][j] as the longest palindromic subsequence within s[i..j]. If s[i] == s[j], they can both be included around whatever's palindromic inside.",
            "dp[i][j] = dp[i+1][j-1] + 2 when s[i]==s[j], else max(dp[i+1][j], dp[i][j-1]) -- fill the table by increasing substring length (or i decreasing, j increasing).",
        ],
    },
    {
        "slug": "delete-operation-two-strings",
        "title": "Delete Operation for Two Strings",
        "primary_skill": "DP_STRING", "pattern_skills": ["DP_STRING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given two strings `word1` and `word2`, return the minimum number of characters you need to delete "
            "(from either string) to make them equal. Unlike full edit distance, only deletion is allowed."
        ),
        "constraints": "0 <= len(word1), len(word2) <= 500",
        "examples": [{"input": "word1='sea', word2='eat'", "output": "2", "explanation": "delete 's' from 'sea' and 't' from 'eat' to get 'ea' from both"}],
        "function_name": "min_delete_distance",
        "starter_code": "def min_delete_distance(word1, word2):\n    pass\n",
        "reference_solution": (
            "def min_delete_distance(word1, word2):\n"
            "    m, n = len(word1), len(word2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if word1[i - 1] == word2[j - 1]:\n"
            "                dp[i][j] = dp[i - 1][j - 1] + 1\n"
            "            else:\n"
            "                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n"
            "    lcs = dp[m][n]\n"
            "    return (m - lcs) + (n - lcs)\n"
        ),
        "expected_complexity": "O(m * n)",
        "test_cases": [
            {"args": ["sea", "eat"], "hidden": False, "explanation": "classic example"},
            {"args": ["leetcode", "etco"], "hidden": False, "explanation": "one string is much shorter"},
            {"args": ["", "abc"], "hidden": True, "explanation": "empty string needs the other fully deleted"},
        ],
        "hints": [
            "The characters that should survive in both strings are exactly their Longest Common Subsequence -- everything else must be deleted.",
            "Compute the LCS length the same way you would for the standalone LCS problem.",
            "The answer is (len(word1) - lcs) + (len(word2) - lcs): whatever isn't part of the shared subsequence gets deleted from each string.",
        ],
    },
    {
        "slug": "minimum-arrows-burst-balloons",
        "title": "Minimum Arrows to Burst Balloons",
        "primary_skill": "GREEDY", "pattern_skills": ["GREEDY"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Balloons are represented as `points`, where `points[i] = [x_start, x_end]` is the horizontal span "
            "a balloon occupies. An arrow shot at position x bursts every balloon whose span includes x. Return "
            "the minimum number of arrows needed to burst every balloon."
        ),
        "constraints": "1 <= len(points) <= 10^5",
        "examples": [{"input": "[[10,16],[2,8],[1,6],[7,12]]", "output": "2", "explanation": "one arrow at x=6 bursts [1,6] and [2,8]; another at x=11 or 12 bursts [10,16] and [7,12]"}],
        "function_name": "find_min_arrow_shots",
        "starter_code": "def find_min_arrow_shots(points):\n    pass\n",
        "reference_solution": (
            "def find_min_arrow_shots(points):\n"
            "    if not points:\n"
            "        return 0\n"
            "    pts = sorted(points, key=lambda p: p[1])\n"
            "    arrows = 1\n"
            "    end = pts[0][1]\n"
            "    for s, e in pts[1:]:\n"
            "        if s > end:\n"
            "            arrows += 1\n"
            "            end = e\n"
            "    return arrows\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[[10, 16], [2, 8], [1, 6], [7, 12]]], "hidden": False, "explanation": "classic example"},
            {"args": [[[1, 2], [3, 4], [5, 6], [7, 8]]], "hidden": False, "explanation": "no overlaps -- one arrow per balloon"},
            {"args": [[[1, 2], [2, 3], [3, 4]]], "hidden": True, "explanation": "touching endpoints still overlap"},
        ],
        "hints": [
            "This looks similar to 'maximum non-overlapping intervals', but the goal here is the minimum number of points that hit every interval, not the count of intervals kept.",
            "Sort balloons by their END coordinate. Always let one arrow cover as many balloons as possible by shooting at the earliest-ending balloon's end.",
            "Track the current arrow's position (an interval's end). Any later balloon whose start is beyond that position needs a brand new arrow -- update the position to that balloon's end.",
        ],
    },
    {
        "slug": "candy-distribution",
        "title": "Candy Distribution",
        "primary_skill": "GREEDY", "pattern_skills": ["GREEDY"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": (
            "There are children standing in a line, each with a rating in `ratings`. Every child must get at "
            "least one candy, and any child with a higher rating than an immediate neighbor must get more "
            "candy than that neighbor. Return the minimum total candies needed."
        ),
        "constraints": "1 <= len(ratings) <= 2*10^4",
        "examples": [{"input": "[1,0,2]", "output": "5", "explanation": "candies [2,1,2] satisfy both neighbor constraints"}],
        "function_name": "candy",
        "starter_code": "def candy(ratings):\n    pass\n",
        "reference_solution": (
            "def candy(ratings):\n"
            "    n = len(ratings)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    candies = [1] * n\n"
            "    for i in range(1, n):\n"
            "        if ratings[i] > ratings[i - 1]:\n"
            "            candies[i] = candies[i - 1] + 1\n"
            "    for i in range(n - 2, -1, -1):\n"
            "        if ratings[i] > ratings[i + 1]:\n"
            "            candies[i] = max(candies[i], candies[i + 1] + 1)\n"
            "    return sum(candies)\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 0, 2]], "hidden": False, "explanation": "classic example"},
            {"args": [[1, 2, 2]], "hidden": False, "explanation": "a plateau needs no extra candy across the tie"},
            {"args": [[1, 3, 2, 1]], "hidden": True, "explanation": "a peak in the middle needs care from both sides"},
        ],
        "hints": [
            "A single greedy left-to-right pass isn't enough -- a child can need more candy than their left neighbor AND more than their right neighbor at the same time.",
            "Do it in two passes: left-to-right, give a child one more candy than their left neighbor if their rating is higher. Then right-to-left, do the same check against the right neighbor.",
            "On the second pass, don't just overwrite -- take the MAX of what the child already has and (right neighbor's candies + 1), since both constraints must hold simultaneously.",
        ],
    },
    {
        "slug": "sort-colors",
        "title": "Sort Colors (Dutch National Flag)",
        "primary_skill": "TWO_POINTER", "pattern_skills": ["TWO_POINTER"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": (
            "Given an array `nums` with only the values 0, 1, and 2, return it sorted in a single pass using "
            "constant extra space (don't just call a library sort)."
        ),
        "constraints": "1 <= len(nums) <= 300, nums[i] is 0, 1, or 2",
        "examples": [{"input": "[2,0,2,1,1,0]", "output": "[0,0,1,1,2,2]", "explanation": "sorted with only 0s, 1s, 2s"}],
        "function_name": "sort_colors",
        "starter_code": "def sort_colors(nums):\n    pass\n",
        "reference_solution": (
            "def sort_colors(nums):\n"
            "    nums = list(nums)\n"
            "    low, mid, high = 0, 0, len(nums) - 1\n"
            "    while mid <= high:\n"
            "        if nums[mid] == 0:\n"
            "            nums[low], nums[mid] = nums[mid], nums[low]\n"
            "            low += 1\n"
            "            mid += 1\n"
            "        elif nums[mid] == 1:\n"
            "            mid += 1\n"
            "        else:\n"
            "            nums[mid], nums[high] = nums[high], nums[mid]\n"
            "            high -= 1\n"
            "    return nums\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[2, 0, 2, 1, 1, 0]], "hidden": False, "explanation": "classic example"},
            {"args": [[2, 0, 1]], "hidden": False, "explanation": "one of each"},
            {"args": [[0, 0, 0]], "hidden": True, "explanation": "already sorted, all same value"},
        ],
        "hints": [
            "Sorting with a library call works but doesn't demonstrate the technique -- and a counting pass plus overwrite is O(n) but uses two passes over the data.",
            "Three pointers do it in one pass: `low` is the next spot for a 0, `high` is the next spot for a 2, and `mid` scans forward.",
            "If nums[mid] is 0, swap it to `low` and advance both low and mid. If it's 2, swap it to `high` and shrink high, but DON'T advance mid yet -- the swapped-in value still needs to be examined.",
        ],
    },
    {
        "slug": "valid-palindrome-ii",
        "title": "Valid Palindrome II (One Deletion Allowed)",
        "primary_skill": "TWO_POINTER", "pattern_skills": ["TWO_POINTER"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a string `s`, return True if it can become a palindrome after deleting at most one character.",
        "constraints": "1 <= len(s) <= 10^5, lowercase letters only",
        "examples": [{"input": "'abca'", "output": "true", "explanation": "deleting 'b' or 'c' leaves a palindrome"}],
        "function_name": "valid_palindrome_ii",
        "starter_code": "def valid_palindrome_ii(s):\n    pass\n",
        "reference_solution": (
            "def valid_palindrome_ii(s):\n"
            "    def is_pal(i, j):\n"
            "        while i < j:\n"
            "            if s[i] != s[j]:\n"
            "                return False\n"
            "            i += 1\n"
            "            j -= 1\n"
            "        return True\n"
            "\n"
            "    i, j = 0, len(s) - 1\n"
            "    while i < j:\n"
            "        if s[i] != s[j]:\n"
            "            return is_pal(i + 1, j) or is_pal(i, j - 1)\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return True\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["aba"], "hidden": False, "explanation": "already a palindrome, no deletion needed"},
            {"args": ["abca"], "hidden": False, "explanation": "one deletion fixes it"},
            {"args": ["abc"], "hidden": True, "explanation": "no single deletion can fix this"},
        ],
        "hints": [
            "Checking every possible single-character deletion and re-testing the whole string each time is O(n^2) -- there's a one-pass way to narrow it down.",
            "Walk inward from both ends with two pointers as if checking a normal palindrome. The first time the characters at the two pointers disagree, you have your one chance to delete.",
            "At that mismatch, try skipping the left character OR skipping the right character, and check if either resulting substring is a palindrome on its own.",
        ],
    },
]
