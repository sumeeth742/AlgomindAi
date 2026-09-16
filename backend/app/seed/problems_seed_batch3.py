"""
Third batch of seeded problems -- see problems_seed.py for the honesty note on
how expected outputs are generated (reference solution executed, never
hand-typed). This batch targets the skills that were thinnest after batches 1
and 2 (Queue/Deque, Union-Find, Topological Sort, Dijkstra, Advanced Patterns,
BST, Programming Basics all had only 2-3 problems) and adds hard-tier depth
(median of two sorted arrays, N-Queens, minimum window substring) that was
almost entirely missing before this batch.

A few classic problems have more than one textbook-correct answer (e.g. more
than one valid topological order, or more than one height-balanced BST for an
array). Where that's the case, the statement pins down a specific,
unambiguous convention (matching this reference solution) so grading isn't
accidentally rejecting a differently-valid-but-differently-shaped answer.
"""

PROBLEMS_BATCH3 = [
    {
        "slug": "rotting-oranges",
        "title": "Rotting Oranges",
        "primary_skill": "QUEUE_DEQUE", "pattern_skills": ["QUEUE_DEQUE", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a grid of 0 (empty), 1 (fresh orange), 2 (rotten orange), every minute a rotten orange rots its 4-directional fresh neighbors. Return the minimum minutes until no fresh orange remains, or -1 if impossible.",
        "constraints": "1 <= rows, cols <= 10",
        "examples": [{"input": "[[2,1,1],[1,1,0],[0,1,1]]", "output": "4", "explanation": "rot spreads outward minute by minute"}],
        "function_name": "oranges_rotting",
        "starter_code": "def oranges_rotting(grid):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def oranges_rotting(grid):\n"
            "    grid = [row[:] for row in grid]\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    q = deque()\n    fresh = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 2:\n                q.append((r, c, 0))\n"
            "            elif grid[r][c] == 1:\n                fresh += 1\n"
            "    if fresh == 0:\n        return 0\n"
            "    minutes = 0\n"
            "    while q:\n"
            "        r, c, t = q.popleft()\n        minutes = max(minutes, t)\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n"
            "                grid[nr][nc] = 2\n                fresh -= 1\n                q.append((nr, nc, t + 1))\n"
            "    return minutes if fresh == 0 else -1\n"
        ),
        "expected_complexity": "O(rows * cols)",
        "test_cases": [
            {"args": [[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], "hidden": False, "explanation": "typical case, 4 minutes"},
            {"args": [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], "hidden": False, "explanation": "an isolated fresh orange -- impossible"},
            {"args": [[[0, 2]]], "hidden": True, "explanation": "no fresh oranges to begin with"},
        ],
        "hints": ["This is multi-source BFS -- start the BFS from every rotten orange at once, not just one.", "Track elapsed time per queue entry, or process the queue in whole 'layers' (one layer per minute).", "If any fresh orange is still unreached once the queue empties, it's unreachable -- return -1."],
    },
    {
        "slug": "walls-and-gates",
        "title": "Walls and Gates",
        "primary_skill": "QUEUE_DEQUE", "pattern_skills": ["QUEUE_DEQUE", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a grid where -1 is a wall, 0 is a gate, and 2147483647 represents an empty room, fill each empty room with the distance to its nearest gate. Return the filled grid.",
        "constraints": "1 <= rows, cols <= 10",
        "examples": [{"input": "[[INF,-1,0,INF],[INF,INF,INF,-1],[INF,-1,INF,-1],[0,-1,INF,INF]]", "output": "distances filled in", "explanation": "BFS outward from every gate at once"}],
        "function_name": "walls_and_gates",
        "starter_code": "def walls_and_gates(rooms):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def walls_and_gates(rooms):\n"
            "    rooms = [row[:] for row in rooms]\n"
            "    if not rooms or not rooms[0]:\n        return rooms\n"
            "    rows, cols = len(rooms), len(rooms[0])\n"
            "    INF = 2147483647\n"
            "    q = deque()\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if rooms[r][c] == 0:\n                q.append((r, c))\n"
            "    while q:\n"
            "        r, c = q.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:\n"
            "                rooms[nr][nc] = rooms[r][c] + 1\n                q.append((nr, nc))\n"
            "    return rooms\n"
        ),
        "expected_complexity": "O(rows * cols)",
        "test_cases": [
            {"args": [[[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]]], "hidden": False, "explanation": "classic layout with two gates"},
            {"args": [[[-1]]], "hidden": False, "explanation": "a single wall -- nothing to fill"},
            {"args": [[[0]]], "hidden": True, "explanation": "a single gate"},
        ],
        "hints": ["Start BFS from every gate simultaneously, not one at a time -- that's what makes distances come out correctly and efficiently.", "Only expand into cells that are still the INF sentinel -- walls and already-filled rooms should be skipped.", "Each cell's distance is exactly one more than the cell that first reached it."],
    },
    {
        "slug": "perfect-squares-bfs",
        "title": "Fewest Perfect Squares Summing to N",
        "primary_skill": "QUEUE_DEQUE", "pattern_skills": ["QUEUE_DEQUE"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an integer `n`, return the least number of perfect square numbers (1, 4, 9, 16, ...) that sum to `n`.",
        "constraints": "1 <= n <= 10^4",
        "examples": [{"input": "12", "output": "3", "explanation": "4+4+4 = 12"}],
        "function_name": "num_squares",
        "starter_code": "def num_squares(n):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def num_squares(n):\n"
            "    if n <= 0:\n        return 0\n"
            "    squares = []\n    i = 1\n"
            "    while i * i <= n:\n        squares.append(i * i)\n        i += 1\n"
            "    visited = {n}\n    q = deque([(n, 0)])\n"
            "    while q:\n"
            "        cur, steps = q.popleft()\n"
            "        for s in squares:\n"
            "            nxt = cur - s\n"
            "            if nxt < 0:\n                break\n"
            "            if nxt == 0:\n                return steps + 1\n"
            "            if nxt not in visited:\n                visited.add(nxt)\n                q.append((nxt, steps + 1))\n"
            "    return -1\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [12], "hidden": False, "explanation": "4+4+4"},
            {"args": [13], "hidden": False, "explanation": "4+9"},
            {"args": [1], "hidden": True, "explanation": "already a perfect square"},
        ],
        "hints": ["Think of this as a shortest-path problem: each state is a remaining amount, and each move subtracts one perfect square.", "BFS from n toward 0 finds the fewest 'moves' (perfect squares used) since BFS explores in order of steps taken.", "Track visited remainders so you don't re-expand the same state repeatedly."],
    },
    {
        "slug": "first-non-repeating-in-stream",
        "title": "First Non-Repeating Character in a Stream",
        "primary_skill": "QUEUE_DEQUE", "pattern_skills": ["QUEUE_DEQUE", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a stream of characters `s`, after each character return the first character seen so far that has not repeated yet, or '#' if none. Return the list of these answers, one per character processed.",
        "constraints": "1 <= len(s) <= 10^4",
        "examples": [{"input": '"aabc"', "output": '["a","#","b","b"]', "explanation": "after each character, the first not-yet-repeated one so far"}],
        "function_name": "first_non_repeating_in_stream",
        "starter_code": "def first_non_repeating_in_stream(s):\n    pass\n",
        "reference_solution": (
            "from collections import deque, Counter\n"
            "def first_non_repeating_in_stream(s):\n"
            "    q = deque()\n    freq = Counter()\n    result = []\n"
            "    for c in s:\n"
            "        freq[c] += 1\n        q.append(c)\n"
            "        while q and freq[q[0]] > 1:\n            q.popleft()\n"
            "        result.append(q[0] if q else '#')\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["aabc"], "hidden": False, "explanation": "typical case"},
            {"args": ["zz"], "hidden": False, "explanation": "immediately repeats"},
            {"args": ["x"], "hidden": True, "explanation": "single character, never repeats"},
        ],
        "hints": ["A queue of 'candidates still not known to repeat' works well here, paired with a frequency count.", "Whenever the front of the queue turns out to have repeated, pop it -- it's disqualified for good.", "The front of the queue, if any survives, is the answer at that point in the stream."],
    },
    {
        "slug": "graph-valid-tree",
        "title": "Graph Valid Tree",
        "primary_skill": "UNION_FIND", "pattern_skills": ["UNION_FIND"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given `n` nodes labeled 0 to n-1 and a list of undirected `edges`, return True if these edges form a valid tree (connected, no cycles).",
        "constraints": "1 <= n <= 2000",
        "examples": [{"input": "n=5, edges=[[0,1],[0,2],[0,3],[1,4]]", "output": "true", "explanation": "connected with exactly n-1 edges and no cycle"}],
        "function_name": "valid_tree",
        "starter_code": "def valid_tree(n, edges):\n    pass\n",
        "reference_solution": (
            "def valid_tree(n, edges):\n"
            "    if len(edges) != n - 1:\n        return False\n"
            "    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n"
            "    for a, b in edges:\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra == rb:\n            return False\n"
            "        parent[ra] = rb\n"
            "    return True\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [5, [[0, 1], [0, 2], [0, 3], [1, 4]]], "hidden": False, "explanation": "a valid tree"},
            {"args": [5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]], "hidden": False, "explanation": "contains a cycle -- not a tree"},
            {"args": [1, []], "hidden": True, "explanation": "single node, trivially a tree"},
        ],
        "hints": ["A tree on n nodes has exactly n-1 edges -- check that first, it's a free disqualifier.", "Union-Find naturally detects a cycle: if two endpoints of an edge are already in the same component, adding that edge creates a cycle.", "If no edge ever connects two already-joined components, and the edge count is exactly n-1, it must be a tree."],
    },
    {
        "slug": "smallest-string-with-swaps",
        "title": "Smallest String With Swaps",
        "primary_skill": "UNION_FIND", "pattern_skills": ["UNION_FIND"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a string `s` and pairs of indices `pairs` that can be swapped any number of times, return the lexicographically smallest string achievable.",
        "constraints": "1 <= len(s) <= 100",
        "examples": [{"input": 's="dcab", pairs=[[0,3],[1,2]]', "output": '"bacd"', "explanation": "indices 0,3 can freely swap, and so can 1,2"}],
        "function_name": "smallest_string_with_swaps",
        "starter_code": "def smallest_string_with_swaps(s, pairs):\n    pass\n",
        "reference_solution": (
            "def smallest_string_with_swaps(s, pairs):\n"
            "    n = len(s)\n    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n            parent[ra] = rb\n"
            "    for a, b in pairs:\n        union(a, b)\n"
            "    from collections import defaultdict\n"
            "    groups = defaultdict(list)\n"
            "    for i in range(n):\n        groups[find(i)].append(i)\n"
            "    result = list(s)\n"
            "    for idxs in groups.values():\n"
            "        idxs_sorted = sorted(idxs)\n        chars = sorted(result[i] for i in idxs)\n"
            "        for i, ch in zip(idxs_sorted, chars):\n            result[i] = ch\n"
            "    return ''.join(result)\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": ["dcab", [[0, 3], [1, 2]]], "hidden": False, "explanation": "two independent swap groups"},
            {"args": ["dcab", [[0, 3], [1, 2], [0, 2]]], "hidden": False, "explanation": "all four indices end up connected"},
            {"args": ["cba", [[0, 1], [1, 2]]], "hidden": True, "explanation": "chained pairs connect everything"},
        ],
        "hints": ["Any two indices connected (directly or transitively) through the given pairs can end up holding any permutation of each other's characters.", "Union-Find groups indices into these connected components.", "Within each component, sort the characters and place them back into the sorted index positions -- that yields the lexicographically smallest arrangement for that group."],
    },
    {
        "slug": "most-stones-removed",
        "title": "Most Stones Removed With Same Row or Column",
        "primary_skill": "UNION_FIND", "pattern_skills": ["UNION_FIND"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given stone positions `[row, col]`, a stone can be removed if it shares a row or column with another remaining stone. Return the maximum number of stones removable.",
        "constraints": "1 <= len(stones) <= 1000",
        "examples": [{"input": "[[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]", "output": "5", "explanation": "all but one stone per connected group can be removed"}],
        "function_name": "remove_stones",
        "starter_code": "def remove_stones(stones):\n    pass\n",
        "reference_solution": (
            "def remove_stones(stones):\n"
            "    parent = {}\n"
            "    def find(x):\n"
            "        if x not in parent:\n            parent[x] = x\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n            parent[ra] = rb\n"
            "    for r, c in stones:\n        union(('r', r), ('c', c))\n"
            "    roots = {find(('r', r)) for r, c in stones}\n"
            "    return len(stones) - len(roots)\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]], "hidden": False, "explanation": "typical case"},
            {"args": [[[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]], "hidden": False, "explanation": "three separate groups"},
            {"args": [[[0, 0]]], "hidden": True, "explanation": "a single stone can't be removed"},
        ],
        "hints": ["The maximum removable count from any connected group of stones is (group size - 1) -- you can always chain-remove down to one survivor.", "Treat each stone as connecting its row-node and column-node in a union-find structure, rather than connecting stones to each other directly.", "The answer is total stones minus the number of connected components."],
    },
    {
        "slug": "accounts-merge",
        "title": "Accounts Merge",
        "primary_skill": "UNION_FIND", "pattern_skills": ["UNION_FIND", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 3, "pattern_difficulty": 4,
        "statement": "Given accounts `[name, email1, email2, ...]`, merge accounts that share at least one email (same name is not required to merge, but merged accounts do share the same name). Return the merged accounts, each as `[name, sorted emails...]`.",
        "constraints": "1 <= len(accounts) <= 100",
        "examples": [{"input": '[["John","j1@mail.com","j2@mail.com"],["John","j1@mail.com","j3@mail.com"],["Mary","m@mail.com"]]', "output": "John's two accounts merge via the shared email", "explanation": "shared email j1@mail.com links the two John accounts"}],
        "function_name": "accounts_merge",
        "starter_code": "def accounts_merge(accounts):\n    pass\n",
        "reference_solution": (
            "def accounts_merge(accounts):\n"
            "    parent = list(range(len(accounts)))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n            parent[ra] = rb\n"
            "    email_to_acct = {}\n"
            "    for i, acct in enumerate(accounts):\n"
            "        for email in acct[1:]:\n"
            "            if email in email_to_acct:\n                union(i, email_to_acct[email])\n"
            "            else:\n                email_to_acct[email] = i\n"
            "    groups = {}\n"
            "    for email, i in email_to_acct.items():\n"
            "        groups.setdefault(find(i), set()).add(email)\n"
            "    result = []\n"
            "    for root, emails in groups.items():\n        result.append([accounts[root][0]] + sorted(emails))\n"
            "    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]], "hidden": False, "explanation": "two John accounts merge via a shared email"},
            {"args": [[["Alice", "alice@mail.com"], ["Bob", "bob@mail.com"]]], "hidden": False, "explanation": "no shared emails -- stay separate"},
            {"args": [[["A", "a@mail.com", "b@mail.com"], ["A", "b@mail.com", "c@mail.com"], ["A", "c@mail.com", "d@mail.com"]]], "hidden": True, "explanation": "chained shared emails merge all three"},
        ],
        "hints": ["Treat each account index as a union-find node, and union two accounts whenever they share an email.", "A hashmap from email to 'the first account index that owned it' lets you detect shared emails and trigger the union.", "After unioning, group all emails by their component's root, then attach the (any representative's) name."],
    },
    {
        "slug": "course-schedule-ii",
        "title": "Course Schedule II",
        "primary_skill": "TOPOLOGICAL_SORT", "pattern_skills": ["TOPOLOGICAL_SORT", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given `num_courses` and prerequisite pairs `[a, b]` meaning b must be taken before a, return a valid course order. If impossible (a cycle exists), return an empty list. When multiple valid orders exist, return the one produced by Kahn's BFS algorithm processing available (zero-prerequisite) courses in increasing course-number order.",
        "constraints": "1 <= num_courses <= 2000",
        "examples": [{"input": "num_courses=2, prerequisites=[[1,0]]", "output": "[0,1]", "explanation": "0 must come before 1"}],
        "function_name": "find_order",
        "starter_code": "def find_order(num_courses, prerequisites):\n    pass\n",
        "reference_solution": (
            "from collections import defaultdict, deque\n"
            "def find_order(num_courses, prerequisites):\n"
            "    graph = defaultdict(list)\n    indegree = [0] * num_courses\n"
            "    for a, b in prerequisites:\n        graph[b].append(a)\n        indegree[a] += 1\n"
            "    q = deque(i for i in range(num_courses) if indegree[i] == 0)\n"
            "    order = []\n"
            "    while q:\n"
            "        node = q.popleft()\n        order.append(node)\n"
            "        for nxt in graph[node]:\n"
            "            indegree[nxt] -= 1\n"
            "            if indegree[nxt] == 0:\n                q.append(nxt)\n"
            "    return order if len(order) == num_courses else []\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [2, [[1, 0]]], "hidden": False, "explanation": "simple chain"},
            {"args": [4, [[1, 0], [2, 0], [3, 1], [3, 2]]], "hidden": False, "explanation": "diamond dependency"},
            {"args": [2, [[1, 0], [0, 1]]], "hidden": True, "explanation": "a cycle -- impossible"},
        ],
        "hints": ["This is Kahn's algorithm: repeatedly take a course with no remaining prerequisites, then 'remove' it and see what becomes available.", "A course whose prerequisite count (indegree) never reaches zero is stuck in a cycle.", "If the final order doesn't include every course, a cycle exists -- return an empty list."],
    },
    {
        "slug": "minimum-height-trees",
        "title": "Minimum Height Trees",
        "primary_skill": "TOPOLOGICAL_SORT", "pattern_skills": ["TOPOLOGICAL_SORT", "GRAPHS"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 5, "pattern_difficulty": 4,
        "statement": "Given a tree with `n` nodes and its `edges`, return the label(s) of the root(s) that would produce a minimum-height tree (there are at most 2 such roots -- the tree's centroid(s)).",
        "constraints": "1 <= n <= 2*10^4",
        "examples": [{"input": "n=4, edges=[[1,0],[1,2],[1,3]]", "output": "[1]", "explanation": "node 1 is the center"}],
        "function_name": "find_min_height_trees",
        "starter_code": "def find_min_height_trees(n, edges):\n    pass\n",
        "reference_solution": (
            "from collections import defaultdict, deque\n"
            "def find_min_height_trees(n, edges):\n"
            "    if n == 1:\n        return [0]\n"
            "    graph = defaultdict(set)\n"
            "    for a, b in edges:\n        graph[a].add(b)\n        graph[b].add(a)\n"
            "    leaves = deque(i for i in range(n) if len(graph[i]) == 1)\n"
            "    remaining = n\n"
            "    while remaining > 2:\n"
            "        num_leaves = len(leaves)\n        remaining -= num_leaves\n"
            "        for _ in range(num_leaves):\n"
            "            leaf = leaves.popleft()\n"
            "            for neighbor in graph[leaf]:\n"
            "                graph[neighbor].discard(leaf)\n"
            "                if len(graph[neighbor]) == 1:\n                    leaves.append(neighbor)\n"
            "    return list(leaves)\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [4, [[1, 0], [1, 2], [1, 3]]], "hidden": False, "explanation": "star graph, single center"},
            {"args": [6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]], "hidden": False, "explanation": "two centroids"},
            {"args": [1, []], "hidden": True, "explanation": "single node -- it is its own center"},
        ],
        "hints": ["The center(s) of a tree are found by repeatedly peeling off all current leaves, layer by layer -- like trimming a tree from the outside in.", "This is the same 'onion peeling' idea as topological sort's layer-by-layer processing, just on an undirected tree.", "At most 2 nodes remain when the peeling can't continue -- those are the answer."],
    },
    {
        "slug": "parallel-courses",
        "title": "Parallel Courses",
        "primary_skill": "TOPOLOGICAL_SORT", "pattern_skills": ["TOPOLOGICAL_SORT"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given `n` courses (1-indexed) and prerequisite pairs `[a,b]` meaning a must be taken before b, and you can take any number of courses in one semester as long as prerequisites are satisfied, return the minimum number of semesters to finish all courses, or -1 if impossible.",
        "constraints": "1 <= n <= 5000",
        "examples": [{"input": "n=3, relations=[[1,3],[2,3]]", "output": "2", "explanation": "take 1 and 2 in semester one, 3 in semester two"}],
        "function_name": "minimum_semesters",
        "starter_code": "def minimum_semesters(n, relations):\n    pass\n",
        "reference_solution": (
            "from collections import defaultdict, deque\n"
            "def minimum_semesters(n, relations):\n"
            "    graph = defaultdict(list)\n    indegree = [0] * (n + 1)\n"
            "    for a, b in relations:\n        graph[a].append(b)\n        indegree[b] += 1\n"
            "    q = deque(i for i in range(1, n + 1) if indegree[i] == 0)\n"
            "    studied = 0\n    semesters = 0\n"
            "    while q:\n"
            "        semesters += 1\n"
            "        for _ in range(len(q)):\n"
            "            node = q.popleft()\n            studied += 1\n"
            "            for nxt in graph[node]:\n"
            "                indegree[nxt] -= 1\n"
            "                if indegree[nxt] == 0:\n                    q.append(nxt)\n"
            "    return semesters if studied == n else -1\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [3, [[1, 3], [2, 3]]], "hidden": False, "explanation": "typical case"},
            {"args": [3, [[1, 2], [2, 3], [3, 1]]], "hidden": False, "explanation": "a cycle -- impossible"},
            {"args": [1, []], "hidden": True, "explanation": "single course, no prerequisites"},
        ],
        "hints": ["Process courses in 'layers' (BFS/Kahn's algorithm) -- every course in the current layer can be taken in the same semester.", "The number of layers processed is the number of semesters needed.", "If some courses never reach indegree zero, they're stuck in a cycle -- return -1."],
    },
    {
        "slug": "cheapest-flights-k-stops",
        "title": "Cheapest Flights Within K Stops",
        "primary_skill": "DIJKSTRA", "pattern_skills": ["DIJKSTRA", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given `n` cities, flights `[from, to, price]`, a source `src`, destination `dst`, and at most `k` stops allowed, return the cheapest price, or -1 if unreachable within k stops.",
        "constraints": "1 <= n <= 100, 0 <= k <= n-1",
        "examples": [{"input": "n=4, flights=[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src=0, dst=3, k=1", "output": "700", "explanation": "0->1->3 costs 700 within 1 stop"}],
        "function_name": "find_cheapest_price",
        "starter_code": "def find_cheapest_price(n, flights, src, dst, k):\n    pass\n",
        "reference_solution": (
            "def find_cheapest_price(n, flights, src, dst, k):\n"
            "    INF = float('inf')\n    dist = [INF] * n\n    dist[src] = 0\n"
            "    for _ in range(k + 1):\n"
            "        new_dist = dist[:]\n"
            "        for u, v, w in flights:\n"
            "            if dist[u] != INF and dist[u] + w < new_dist[v]:\n                new_dist[v] = dist[u] + w\n"
            "        dist = new_dist\n"
            "    return dist[dst] if dist[dst] != INF else -1\n"
        ),
        "expected_complexity": "O(k * edges)",
        "test_cases": [
            {"args": [4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], "hidden": False, "explanation": "typical case"},
            {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1], "hidden": False, "explanation": "one stop allows the cheaper path"},
            {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], "hidden": True, "explanation": "zero stops forces the direct (expensive) flight"},
        ],
        "hints": ["Plain Dijkstra doesn't track 'number of stops used', so it can lock in a cheap-but-too-long path too early -- this needs a stop-limited relaxation instead.", "Bellman-Ford-style: relax all edges once per allowed stop, using a snapshot of the previous round's distances (not updating in place) so each round represents exactly one more flight.", "After k+1 rounds of relaxation (k stops means k+1 flights), the destination's distance is the answer."],
    },
    {
        "slug": "path-with-max-probability",
        "title": "Path With Maximum Probability",
        "primary_skill": "DIJKSTRA", "pattern_skills": ["DIJKSTRA", "GRAPHS"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given `n` nodes, undirected edges with success probabilities, a `start` and `end`, return the maximum probability of reaching end from start (0.0 if unreachable).",
        "constraints": "1 <= n <= 10^4, 0 <= probability <= 1",
        "examples": [{"input": "n=3, edges=[[0,1],[1,2],[0,2]], succ_prob=[0.5,0.5,0.125], start=0, end=2", "output": "0.25", "explanation": "0->1->2 beats the direct edge"}],
        "function_name": "max_probability",
        "starter_code": "def max_probability(n, edges, succ_prob, start, end):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "from collections import defaultdict\n"
            "def max_probability(n, edges, succ_prob, start, end):\n"
            "    graph = defaultdict(list)\n"
            "    for (a, b), p in zip(edges, succ_prob):\n"
            "        graph[a].append((b, p))\n        graph[b].append((a, p))\n"
            "    prob = [0.0] * n\n    prob[start] = 1.0\n"
            "    heap = [(-1.0, start)]\n"
            "    while heap:\n"
            "        neg_p, node = heapq.heappop(heap)\n        p = -neg_p\n"
            "        if node == end:\n            return p\n"
            "        if p < prob[node]:\n            continue\n"
            "        for nxt, edge_p in graph[node]:\n"
            "            new_p = p * edge_p\n"
            "            if new_p > prob[nxt]:\n                prob[nxt] = new_p\n                heapq.heappush(heap, (-new_p, nxt))\n"
            "    return 0.0\n"
        ),
        "expected_complexity": "O((n + edges) log n)",
        "test_cases": [
            {"args": [3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.125], 0, 2], "hidden": False, "explanation": "indirect path wins"},
            {"args": [3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.5], 0, 2], "hidden": False, "explanation": "direct edge wins"},
            {"args": [3, [[0, 1]], [0.5], 0, 2], "hidden": True, "explanation": "unreachable"},
        ],
        "hints": ["This is Dijkstra with the comparison flipped: instead of minimizing summed weight, maximize multiplied probability.", "A max-heap (simulate with negated values in Python's min-heap) always expands the currently-most-probable node next.", "Probabilities only shrink as you traverse more edges, so once you pop the destination, that's provably its best probability."],
    },
    {
        "slug": "minimum-effort-path",
        "title": "Path With Minimum Effort",
        "primary_skill": "DIJKSTRA", "pattern_skills": ["DIJKSTRA"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given a grid of heights, find a path from the top-left to bottom-right (4-directional moves) that minimizes the *maximum* absolute height difference between two consecutive cells along the path. Return that minimized maximum difference.",
        "constraints": "1 <= rows, cols <= 100",
        "examples": [{"input": "[[1,2,2],[3,8,2],[5,3,5]]", "output": "2", "explanation": "the best route never needs a step bigger than 2"}],
        "function_name": "minimum_effort_path",
        "starter_code": "def minimum_effort_path(heights):\n    pass\n",
        "reference_solution": (
            "import heapq\n"
            "def minimum_effort_path(heights):\n"
            "    rows, cols = len(heights), len(heights[0])\n"
            "    effort = [[float('inf')] * cols for _ in range(rows)]\n    effort[0][0] = 0\n"
            "    heap = [(0, 0, 0)]\n"
            "    while heap:\n"
            "        e, r, c = heapq.heappop(heap)\n"
            "        if (r, c) == (rows - 1, cols - 1):\n            return e\n"
            "        if e > effort[r][c]:\n            continue\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols:\n"
            "                diff = abs(heights[nr][nc] - heights[r][c])\n"
            "                new_effort = max(e, diff)\n"
            "                if new_effort < effort[nr][nc]:\n"
            "                    effort[nr][nc] = new_effort\n                    heapq.heappush(heap, (new_effort, nr, nc))\n"
            "    return 0\n"
        ),
        "expected_complexity": "O(rows * cols * log(rows * cols))",
        "test_cases": [
            {"args": [[[1, 2, 2], [3, 8, 2], [5, 3, 5]]], "hidden": False, "explanation": "classic example"},
            {"args": [[[1, 2, 3], [3, 8, 4], [5, 3, 5]]], "hidden": False, "explanation": "a different grid"},
            {"args": [[[1, 10, 6, 7, 9, 10, 4, 9]]], "hidden": True, "explanation": "single row -- path is forced"},
        ],
        "hints": ["This is a 'minimax path' problem -- Dijkstra still applies, just with 'cost so far' redefined as the largest single step taken, not a sum.", "When relaxing a neighbor, the new cost is max(current path's worst step, this new step) -- not current + new.", "Once you pop the bottom-right cell off the priority queue, its recorded effort is optimal."],
    },
    {
        "slug": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "primary_skill": "ADVANCED_PATTERNS", "pattern_skills": ["ADVANCED_PATTERNS", "TWO_POINTER"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 5, "pattern_difficulty": 4,
        "statement": "Given an elevation map `height`, compute how much rainwater it can trap after raining.",
        "constraints": "1 <= len(height) <= 2*10^4",
        "examples": [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "water pools between the taller bars"}],
        "function_name": "trap",
        "starter_code": "def trap(height):\n    pass\n",
        "reference_solution": (
            "def trap(height):\n"
            "    if not height:\n        return 0\n"
            "    l, r = 0, len(height) - 1\n    left_max, right_max = height[l], height[r]\n    water = 0\n"
            "    while l < r:\n"
            "        if left_max <= right_max:\n"
            "            l += 1\n            left_max = max(left_max, height[l])\n            water += left_max - height[l]\n"
            "        else:\n"
            "            r -= 1\n            right_max = max(right_max, height[r])\n            water += right_max - height[r]\n"
            "    return water\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], "hidden": False, "explanation": "classic example"},
            {"args": [[4, 2, 0, 3, 2, 5]], "hidden": False, "explanation": "another classic example"},
            {"args": [[]], "hidden": True, "explanation": "empty terrain -- no water"},
        ],
        "hints": ["The water trapped above any bar is limited by the shorter of the tallest bar to its left and the tallest bar to its right.", "A brute-force approach recomputes left-max/right-max for every position -- O(n^2). Two pointers moving inward can track both running maxes in one pass.", "Whichever side currently has the smaller running max is safe to resolve next -- its water level is already determined."],
    },
    {
        "slug": "product-except-self",
        "title": "Product of Array Except Self",
        "primary_skill": "ADVANCED_PATTERNS", "pattern_skills": ["ADVANCED_PATTERNS", "ARRAYS_PREFIX_SUM"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an array `nums`, return an array `answer` where `answer[i]` is the product of all elements except `nums[i]`, without using division.",
        "constraints": "2 <= len(nums) <= 10^5",
        "examples": [{"input": "[1,2,3,4]", "output": "[24,12,8,6]", "explanation": "product of all others at each index"}],
        "function_name": "product_except_self",
        "starter_code": "def product_except_self(nums):\n    pass\n",
        "reference_solution": (
            "def product_except_self(nums):\n"
            "    n = len(nums)\n    result = [1] * n\n"
            "    prefix = 1\n"
            "    for i in range(n):\n        result[i] = prefix\n        prefix *= nums[i]\n"
            "    suffix = 1\n"
            "    for i in range(n - 1, -1, -1):\n        result[i] *= suffix\n        suffix *= nums[i]\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4]], "hidden": False, "explanation": "typical case"},
            {"args": [[-1, 1, 0, -3, 3]], "hidden": False, "explanation": "a zero forces most positions to 0"},
            {"args": [[2, 3]], "hidden": True, "explanation": "minimal case"},
        ],
        "hints": ["Without division, build the answer from two passes: prefix products from the left, suffix products from the right.", "After the left pass, result[i] holds the product of everything before i.", "Multiply in the product of everything after i during a second, right-to-left pass."],
    },
    {
        "slug": "gas-station",
        "title": "Gas Station Circuit",
        "primary_skill": "ADVANCED_PATTERNS", "pattern_skills": ["ADVANCED_PATTERNS", "GREEDY"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 2, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "There are `gas[i]` fuel and `cost[i]` fuel needed to travel from station i to i+1 around a circular route. Return the starting station index from which you can complete the full circuit, or -1 if impossible (there is at most one valid answer).",
        "constraints": "1 <= len(gas) == len(cost) <= 10^5",
        "examples": [{"input": "gas=[1,2,3,4,5], cost=[3,4,5,1,2]", "output": "3", "explanation": "starting at station 3 you can always keep enough fuel"}],
        "function_name": "can_complete_circuit",
        "starter_code": "def can_complete_circuit(gas, cost):\n    pass\n",
        "reference_solution": (
            "def can_complete_circuit(gas, cost):\n"
            "    total = 0\n    tank = 0\n    start = 0\n"
            "    for i in range(len(gas)):\n"
            "        diff = gas[i] - cost[i]\n        total += diff\n        tank += diff\n"
            "        if tank < 0:\n            start = i + 1\n            tank = 0\n"
            "    return start if total >= 0 else -1\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "hidden": False, "explanation": "typical case"},
            {"args": [[2, 3, 4], [3, 4, 3]], "hidden": False, "explanation": "impossible -- not enough total fuel"},
            {"args": [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], "hidden": True, "explanation": "another valid circuit"},
        ],
        "hints": ["If the total gas is less than the total cost, no starting point works -- check that first.", "Track a running tank balance as you go; whenever it goes negative, no station before this point could have been a valid start either.", "The station right after the last point the tank went negative is the only remaining candidate."],
    },
    {
        "slug": "longest-increasing-subsequence",
        "title": "Longest Increasing Subsequence",
        "primary_skill": "ADVANCED_PATTERNS", "pattern_skills": ["ADVANCED_PATTERNS", "BINARY_SEARCH", "DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 5, "pattern_difficulty": 4,
        "statement": "Given an array `nums`, return the length of the longest strictly increasing subsequence.",
        "constraints": "1 <= len(nums) <= 2500",
        "examples": [{"input": "[10,9,2,5,3,7,101,18]", "output": "4", "explanation": "[2,3,7,101] or [2,3,7,18]"}],
        "function_name": "length_of_lis",
        "starter_code": "def length_of_lis(nums):\n    pass\n",
        "reference_solution": (
            "import bisect\n"
            "def length_of_lis(nums):\n"
            "    tails = []\n"
            "    for x in nums:\n"
            "        i = bisect.bisect_left(tails, x)\n"
            "        if i == len(tails):\n            tails.append(x)\n"
            "        else:\n            tails[i] = x\n"
            "    return len(tails)\n"
        ),
        "expected_complexity": "O(n log n)",
        "test_cases": [
            {"args": [[10, 9, 2, 5, 3, 7, 101, 18]], "hidden": False, "explanation": "classic example"},
            {"args": [[0, 1, 0, 3, 2, 3]], "hidden": False, "explanation": "another classic example"},
            {"args": [[7, 7, 7, 7]], "hidden": True, "explanation": "no strictly increasing pair exists"},
        ],
        "hints": ["A plain O(n^2) DP (best-ending-here for every index) works but is too slow for the largest inputs -- there's an O(n log n) approach.", "Maintain an array of 'the smallest possible tail value for an increasing subsequence of each length seen so far'.", "Binary search for where the current number fits into that tails array -- the final length of the tails array is the answer, even though the tails array itself isn't a real subsequence."],
    },
    {
        "slug": "lowest-common-ancestor-bst",
        "title": "Lowest Common Ancestor of a BST",
        "primary_skill": "BST", "pattern_skills": ["BST"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a binary search tree (level-order form) and two values `p` and `q` known to exist in it, return the value of their lowest common ancestor.",
        "constraints": "2 <= number of nodes <= 10^5",
        "examples": [{"input": "root=[6,2,8,0,4,7,9,None,None,3,5], p=2, q=8", "output": "6", "explanation": "6 is where the search paths to 2 and 8 diverge"}],
        "function_name": "lowest_common_ancestor",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef lowest_common_ancestor(root, p, q):\n    pass\n",
        "reference_solution": (
            "def lowest_common_ancestor(root, p, q):\n"
            "    node = root\n"
            "    while node:\n"
            "        if p < node.val and q < node.val:\n            node = node.left\n"
            "        elif p > node.val and q > node.val:\n            node = node.right\n"
            "        else:\n            return node.val\n"
            "    return -1\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], "hidden": False, "explanation": "ancestor is the root"},
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4], "hidden": False, "explanation": "one is an ancestor of the other"},
            {"args": [[2, 1], 2, 1], "hidden": True, "explanation": "the root itself is the answer"},
        ],
        "hints": ["The BST property tells you which direction to go without searching both subtrees: if both values are smaller than the current node, the answer is in the left subtree; if both are bigger, the right.", "The moment the values split (one smaller, one bigger, or one equals the current node), you've found the ancestor.", "No need for a general tree LCA algorithm here -- the BST ordering makes this a single O(log n) walk down."],
    },
    {
        "slug": "insert-into-bst",
        "title": "Insert into a Binary Search Tree",
        "primary_skill": "BST", "pattern_skills": ["BST"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a BST (level-order form) and a `val`, insert val into the tree so it remains a valid BST, and return the resulting tree.",
        "constraints": "0 <= number of nodes <= 10^4",
        "examples": [{"input": "root=[4,2,7,1,3], val=5", "output": "5 becomes the left child of 7", "explanation": "5 is greater than 4, less than 7"}],
        "function_name": "insert_into_bst",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef insert_into_bst(root, val):\n    pass\n",
        "reference_solution": (
            "def insert_into_bst(root, val):\n"
            "    if root is None:\n        return TreeNode(val)\n"
            "    if val < root.val:\n        root.left = insert_into_bst(root.left, val)\n"
            "    else:\n        root.right = insert_into_bst(root.right, val)\n"
            "    return root\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}, "result": "binary_tree"},
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[4, 2, 7, 1, 3], 5], "hidden": False, "explanation": "inserts as a new leaf"},
            {"args": [[], 5], "hidden": False, "explanation": "empty tree -- new node becomes the root"},
            {"args": [[40, 20, 60, 10, 30, 50, 70], 25], "hidden": True, "explanation": "inserts deeper into an existing subtree"},
        ],
        "hints": ["A BST insert always creates exactly one new leaf -- it never needs to rebalance or restructure existing nodes.", "Compare val against the current node to decide whether to recurse left or right.", "The base case is an empty spot (None) -- that's exactly where the new node belongs."],
    },
    {
        "slug": "convert-sorted-array-to-bst",
        "title": "Convert Sorted Array to Binary Search Tree",
        "primary_skill": "BST", "pattern_skills": ["BST", "RECURSION"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a sorted array `nums`, build a height-balanced BST from it and return it. Many height-balanced BSTs can be valid for a given array; to make grading well-defined, use this convention: at every recursive step, the root of the current subarray range is its left-middle element (using integer floor division for the midpoint).",
        "constraints": "1 <= len(nums) <= 10^4",
        "examples": [{"input": "[-10,-3,0,5,9]", "output": "a balanced BST rooted at 0", "explanation": "middle element becomes the root at each level"}],
        "function_name": "sorted_array_to_bst",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef sorted_array_to_bst(nums):\n    pass\n",
        "reference_solution": (
            "def sorted_array_to_bst(nums):\n"
            "    def build(lo, hi):\n"
            "        if lo > hi:\n            return None\n"
            "        mid = (lo + hi) // 2\n"
            "        node = TreeNode(nums[mid])\n"
            "        node.left = build(lo, mid - 1)\n        node.right = build(mid + 1, hi)\n"
            "        return node\n"
            "    return build(0, len(nums) - 1)\n"
        ),
        "io_transform": {"result": "binary_tree"},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[-10, -3, 0, 5, 9]], "hidden": False, "explanation": "odd-length array"},
            {"args": [[1, 3]], "hidden": False, "explanation": "even-length array -- left-middle convention picks index 0"},
            {"args": [[1]], "hidden": True, "explanation": "single element"},
        ],
        "hints": ["Recursively pick the middle of the current range as the root, then recurse on the left and right halves for the subtrees.", "For an even-length range, this problem's convention is to use the left-middle element (floor division) -- match that exactly to pass grading.", "This naturally produces a height-balanced tree since each recursive call roughly halves the range."],
    },
    {
        "slug": "range-sum-bst",
        "title": "Range Sum of BST",
        "primary_skill": "BST", "pattern_skills": ["BST"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a BST (level-order form) and a range `[low, high]`, return the sum of values of all nodes with a value in that range (inclusive).",
        "constraints": "1 <= number of nodes <= 2*10^4",
        "examples": [{"input": "root=[10,5,15,3,7,None,18], low=7, high=15", "output": "32", "explanation": "7+10+15 = 32"}],
        "function_name": "range_sum_bst",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef range_sum_bst(root, low, high):\n    pass\n",
        "reference_solution": (
            "def range_sum_bst(root, low, high):\n"
            "    if root is None:\n        return 0\n"
            "    total = 0\n"
            "    if low <= root.val <= high:\n        total += root.val\n"
            "    if root.val > low:\n        total += range_sum_bst(root.left, low, high)\n"
            "    if root.val < high:\n        total += range_sum_bst(root.right, low, high)\n"
            "    return total\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[10, 5, 15, 3, 7, None, 18], 7, 15], "hidden": False, "explanation": "typical case"},
            {"args": [[10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10], "hidden": False, "explanation": "a deeper tree"},
            {"args": [[10], 5, 15], "hidden": True, "explanation": "single node inside the range"},
        ],
        "hints": ["Use the BST property to skip entire subtrees that can't possibly be in range -- don't just do a plain full-tree traversal.", "If the current node's value is below `low`, its entire left subtree is also below `low` and can be skipped.", "Symmetrically, skip the right subtree if the current node's value is already above `high`."],
    },
    {
        "slug": "fizzbuzz-sum",
        "title": "FizzBuzz",
        "primary_skill": "PROGRAMMING_BASICS", "pattern_skills": ["PROGRAMMING_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given an integer `n`, return a list of strings for 1 to n where multiples of 3 are 'Fizz', multiples of 5 are 'Buzz', multiples of both are 'FizzBuzz', and otherwise the number itself as a string.",
        "constraints": "1 <= n <= 10^4",
        "examples": [{"input": "5", "output": '["1","2","Fizz","4","Buzz"]', "explanation": "standard FizzBuzz rules"}],
        "function_name": "fizz_buzz",
        "starter_code": "def fizz_buzz(n):\n    pass\n",
        "reference_solution": (
            "def fizz_buzz(n):\n"
            "    result = []\n"
            "    for i in range(1, n + 1):\n"
            "        if i % 15 == 0:\n            result.append('FizzBuzz')\n"
            "        elif i % 3 == 0:\n            result.append('Fizz')\n"
            "        elif i % 5 == 0:\n            result.append('Buzz')\n"
            "        else:\n            result.append(str(i))\n"
            "    return result\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [15], "hidden": False, "explanation": "covers all four cases"},
            {"args": [5], "hidden": False, "explanation": "typical small case"},
            {"args": [1], "hidden": True, "explanation": "minimal case"},
        ],
        "hints": ["Check the 'FizzBuzz' case (divisible by both 3 and 5, i.e. by 15) before checking either individually -- otherwise you'd only ever hit the Fizz or Buzz branch.", "Use the modulo operator to test divisibility.", "This is a foundational loop-with-conditionals exercise -- get comfortable with it before moving to pattern-based problems."],
    },
    {
        "slug": "reverse-integer",
        "title": "Reverse an Integer",
        "primary_skill": "PROGRAMMING_BASICS", "pattern_skills": ["PROGRAMMING_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing causes the value to go outside the signed 32-bit range [-2^31, 2^31-1], return 0.",
        "constraints": "-2^31 <= x <= 2^31 - 1",
        "examples": [{"input": "123", "output": "321", "explanation": "digits reversed"}],
        "function_name": "reverse_integer",
        "starter_code": "def reverse_integer(x):\n    pass\n",
        "reference_solution": (
            "def reverse_integer(x):\n"
            "    sign = -1 if x < 0 else 1\n    x = abs(x)\n    result = 0\n"
            "    while x:\n        result = result * 10 + x % 10\n        x //= 10\n"
            "    result *= sign\n"
            "    if result < -2**31 or result > 2**31 - 1:\n        return 0\n"
            "    return result\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [123], "hidden": False, "explanation": "typical case"},
            {"args": [-123], "hidden": False, "explanation": "negative number keeps its sign"},
            {"args": [120], "hidden": True, "explanation": "trailing zero disappears when reversed"},
        ],
        "hints": ["Peel off digits one at a time from the end using `% 10` and `// 10`, building the reversed number as you go.", "Handle the sign separately -- work with the absolute value, then reapply the sign at the end.", "Check the 32-bit signed range only at the very end, once you have the full reversed value."],
    },
    {
        "slug": "palindrome-number",
        "title": "Palindrome Number",
        "primary_skill": "PROGRAMMING_BASICS", "pattern_skills": ["PROGRAMMING_BASICS"],
        "difficulty": "easy",
        "concept_difficulty": 1, "implementation_difficulty": 1, "reasoning_difficulty": 1, "pattern_difficulty": 1,
        "statement": "Given an integer `x`, return True if it reads the same forwards and backwards. Negative numbers are never palindromes.",
        "constraints": "-2^31 <= x <= 2^31 - 1",
        "examples": [{"input": "121", "output": "true", "explanation": "reads the same both ways"}],
        "function_name": "is_palindrome_number",
        "starter_code": "def is_palindrome_number(x):\n    pass\n",
        "reference_solution": "def is_palindrome_number(x):\n    if x < 0:\n        return False\n    s = str(x)\n    return s == s[::-1]\n",
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [121], "hidden": False, "explanation": "a palindrome"},
            {"args": [-121], "hidden": False, "explanation": "negative -- never a palindrome"},
            {"args": [10], "hidden": True, "explanation": "reversed is 01, not equal to 10"},
        ],
        "hints": ["Negative numbers can be rejected immediately -- the minus sign breaks any chance of symmetry.", "Comparing the number's string form to its reverse is a simple, correct approach.", "This is a good first exercise in string slicing (`s[::-1]`)."],
    },
    {
        "slug": "count-primes-sieve",
        "title": "Count Primes Below N",
        "primary_skill": "PROGRAMMING_BASICS", "pattern_skills": ["PROGRAMMING_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given an integer `n`, return the number of prime numbers strictly less than `n`.",
        "constraints": "0 <= n <= 5*10^6",
        "examples": [{"input": "10", "output": "4", "explanation": "2, 3, 5, 7 are prime and less than 10"}],
        "function_name": "count_primes",
        "starter_code": "def count_primes(n):\n    pass\n",
        "reference_solution": (
            "def count_primes(n):\n"
            "    if n < 3:\n        return 0\n"
            "    is_prime = [True] * n\n    is_prime[0] = is_prime[1] = False\n"
            "    for i in range(2, int(n ** 0.5) + 1):\n"
            "        if is_prime[i]:\n"
            "            for j in range(i * i, n, i):\n                is_prime[j] = False\n"
            "    return sum(is_prime)\n"
        ),
        "expected_complexity": "O(n log log n)",
        "test_cases": [
            {"args": [10], "hidden": False, "explanation": "typical case"},
            {"args": [0], "hidden": False, "explanation": "no numbers to check"},
            {"args": [1], "hidden": True, "explanation": "no primes below 1"},
        ],
        "hints": ["Checking each number for primality individually (trial division) is far slower than needed for large n -- a Sieve of Eratosthenes computes all of them at once.", "Start by assuming every number is prime, then cross off multiples of each prime you find, starting from that prime's square.", "You only need to sieve up to sqrt(n) -- any composite number below n has a factor at most sqrt(n)."],
    },
    {
        "slug": "search-in-rotated-sorted-array",
        "title": "Search in Rotated Sorted Array",
        "primary_skill": "BINARY_SEARCH", "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given a sorted array that has been rotated at an unknown pivot, and a `target`, return its index, or -1 if not present. All values are distinct.",
        "constraints": "1 <= len(nums) <= 5000",
        "examples": [{"input": "nums=[4,5,6,7,0,1,2], target=0", "output": "4", "explanation": "0 is found despite the rotation"}],
        "function_name": "search_rotated",
        "starter_code": "def search_rotated(nums, target):\n    pass\n",
        "reference_solution": (
            "def search_rotated(nums, target):\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] == target:\n            return mid\n"
            "        if nums[lo] <= nums[mid]:\n"
            "            if nums[lo] <= target < nums[mid]:\n                hi = mid - 1\n"
            "            else:\n                lo = mid + 1\n"
            "        else:\n"
            "            if nums[mid] < target <= nums[hi]:\n                lo = mid + 1\n"
            "            else:\n                hi = mid - 1\n"
            "    return -1\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[4, 5, 6, 7, 0, 1, 2], 0], "hidden": False, "explanation": "typical case"},
            {"args": [[4, 5, 6, 7, 0, 1, 2], 3], "hidden": False, "explanation": "target absent"},
            {"args": [[1], 0], "hidden": True, "explanation": "single element, absent"},
        ],
        "hints": ["At every midpoint, at least one half of the array (left-of-mid or mid-to-right) is guaranteed to still be normally sorted -- identify which half that is first.", "Once you know which half is sorted, you can check in O(1) whether the target could be in that half's range.", "This turns an unfamiliar 'rotated' search into a slightly modified ordinary binary search, still O(log n)."],
    },
    {
        "slug": "find-min-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "primary_skill": "BINARY_SEARCH", "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": "Given a sorted array rotated at an unknown pivot (all values distinct), return the minimum element.",
        "constraints": "1 <= len(nums) <= 5000",
        "examples": [{"input": "[3,4,5,1,2]", "output": "1", "explanation": "the rotation point holds the minimum"}],
        "function_name": "find_min_rotated",
        "starter_code": "def find_min_rotated(nums):\n    pass\n",
        "reference_solution": (
            "def find_min_rotated(nums):\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] > nums[hi]:\n            lo = mid + 1\n"
            "        else:\n            hi = mid\n"
            "    return nums[lo]\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[3, 4, 5, 1, 2]], "hidden": False, "explanation": "typical case"},
            {"args": [[4, 5, 6, 7, 0, 1, 2]], "hidden": False, "explanation": "rotation point later in the array"},
            {"args": [[11, 13, 15, 17]], "hidden": True, "explanation": "no rotation at all"},
        ],
        "hints": ["Comparing the middle element to the rightmost element tells you which side the rotation point (and hence the minimum) is on.", "If nums[mid] > nums[hi], the minimum must be to the right of mid.", "Otherwise, the minimum is at mid or to its left -- narrow the search accordingly."],
    },
    {
        "slug": "median-of-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "primary_skill": "BINARY_SEARCH", "pattern_skills": ["BINARY_SEARCH"],
        "difficulty": "hard",
        "concept_difficulty": 5, "implementation_difficulty": 5, "reasoning_difficulty": 5, "pattern_difficulty": 5,
        "statement": "Given two sorted arrays `nums1` and `nums2`, return the median of the combined sorted array, in O(log(min(m,n))) time.",
        "constraints": "0 <= len(nums1), len(nums2) <= 1000, at least one array is non-empty",
        "examples": [{"input": "nums1=[1,3], nums2=[2]", "output": "2.0", "explanation": "merged: [1,2,3], median 2"}],
        "function_name": "find_median_sorted_arrays",
        "starter_code": "def find_median_sorted_arrays(nums1, nums2):\n    pass\n",
        "reference_solution": (
            "def find_median_sorted_arrays(nums1, nums2):\n"
            "    if len(nums1) > len(nums2):\n        nums1, nums2 = nums2, nums1\n"
            "    m, n = len(nums1), len(nums2)\n"
            "    lo, hi = 0, m\n    half = (m + n + 1) // 2\n"
            "    while lo <= hi:\n"
            "        i = (lo + hi) // 2\n        j = half - i\n"
            "        left1 = nums1[i - 1] if i > 0 else float('-inf')\n        right1 = nums1[i] if i < m else float('inf')\n"
            "        left2 = nums2[j - 1] if j > 0 else float('-inf')\n        right2 = nums2[j] if j < n else float('inf')\n"
            "        if left1 <= right2 and left2 <= right1:\n"
            "            if (m + n) % 2 == 1:\n                return float(max(left1, left2))\n"
            "            return (max(left1, left2) + min(right1, right2)) / 2.0\n"
            "        elif left1 > right2:\n            hi = i - 1\n"
            "        else:\n            lo = i + 1\n"
            "    return 0.0\n"
        ),
        "expected_complexity": "O(log n)",
        "test_cases": [
            {"args": [[1, 3], [2]], "hidden": False, "explanation": "odd total length"},
            {"args": [[1, 2], [3, 4]], "hidden": False, "explanation": "even total length"},
            {"args": [[], [1]], "hidden": True, "explanation": "one array is empty"},
        ],
        "hints": ["Merging both arrays and taking the middle is O(m+n) -- correct, but not the O(log(min(m,n))) this problem asks for.", "Binary search on how many elements to take from the smaller array; the number taken from the other array is then determined (so both sides of the 'partition' have equal-ish size).", "A valid partition is one where every element on the left side is <= every element on the right side, across both arrays combined."],
    },
    {
        "slug": "n-queens",
        "title": "N-Queens Count",
        "primary_skill": "BACKTRACKING", "pattern_skills": ["BACKTRACKING"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given an integer `n`, return the number of distinct ways to place n queens on an n x n chessboard so that no two queens attack each other.",
        "constraints": "1 <= n <= 9",
        "examples": [{"input": "4", "output": "2", "explanation": "there are exactly 2 solutions for a 4x4 board"}],
        "function_name": "total_n_queens",
        "starter_code": "def total_n_queens(n):\n    pass\n",
        "reference_solution": (
            "def total_n_queens(n):\n"
            "    cols, diag1, diag2 = set(), set(), set()\n    count = 0\n"
            "    def backtrack(row):\n"
            "        nonlocal count\n"
            "        if row == n:\n            count += 1\n            return\n"
            "        for col in range(n):\n"
            "            if col in cols or (row - col) in diag1 or (row + col) in diag2:\n                continue\n"
            "            cols.add(col); diag1.add(row - col); diag2.add(row + col)\n"
            "            backtrack(row + 1)\n"
            "            cols.discard(col); diag1.discard(row - col); diag2.discard(row + col)\n"
            "    backtrack(0)\n    return count\n"
        ),
        "expected_complexity": "O(n!)",
        "test_cases": [
            {"args": [4], "hidden": False, "explanation": "classic small case"},
            {"args": [1], "hidden": False, "explanation": "trivial single-queen board"},
            {"args": [2], "hidden": True, "explanation": "impossible to place 2 non-attacking queens on a 2x2 board"},
        ],
        "hints": ["Place one queen per row, and backtrack across columns within each row -- this automatically avoids two queens sharing a row.", "Track occupied columns and both diagonals (row-col and row+col are constant along each diagonal direction) to check attacks in O(1).", "Undo (backtrack) the column/diagonal markers after exploring each placement so sibling branches aren't polluted."],
    },
    {
        "slug": "word-search",
        "title": "Word Search",
        "primary_skill": "BACKTRACKING", "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 4, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a 2D grid of letters and a `word`, return True if the word can be formed by a path of adjacent (4-directional) cells, using each cell at most once.",
        "constraints": "1 <= rows, cols <= 6, 1 <= len(word) <= 15",
        "examples": [{"input": '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCCED"', "output": "true", "explanation": "a valid connected path spells the word"}],
        "function_name": "word_search_exists",
        "starter_code": "def word_search_exists(board, word):\n    pass\n",
        "reference_solution": (
            "def word_search_exists(board, word):\n"
            "    board = [row[:] for row in board]\n"
            "    rows, cols = len(board), len(board[0])\n"
            "    def backtrack(r, c, i):\n"
            "        if i == len(word):\n            return True\n"
            "        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]:\n            return False\n"
            "        temp = board[r][c]\n        board[r][c] = '#'\n"
            "        found = (backtrack(r + 1, c, i + 1) or backtrack(r - 1, c, i + 1) or\n"
            "                 backtrack(r, c + 1, i + 1) or backtrack(r, c - 1, i + 1))\n"
            "        board[r][c] = temp\n        return found\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if backtrack(r, c, 0):\n                return True\n"
            "    return False\n"
        ),
        "expected_complexity": "O(rows * cols * 4^len(word))",
        "test_cases": [
            {"args": [[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"], "hidden": False, "explanation": "a valid path exists"},
            {"args": [[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"], "hidden": False, "explanation": "another valid path"},
            {"args": [[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"], "hidden": True, "explanation": "would require reusing a cell -- not allowed"},
        ],
        "hints": ["Try starting the search from every cell that matches the word's first letter.", "Temporarily mark a visited cell (e.g. with a placeholder character) so the search can't reuse it, then restore it when backtracking out.", "Stop exploring a branch as soon as a mismatch is found -- that's the 'pruning' that makes backtracking practical here."],
    },
    {
        "slug": "permutations-ii",
        "title": "Permutations II (With Duplicates)",
        "primary_skill": "BACKTRACKING", "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 4, "reasoning_difficulty": 3, "pattern_difficulty": 4,
        "statement": "Given an array `nums` that may contain duplicates, return all distinct permutations.",
        "constraints": "1 <= len(nums) <= 8",
        "examples": [{"input": "[1,1,2]", "output": "[[1,1,2],[1,2,1],[2,1,1]]", "explanation": "duplicate permutations are not repeated"}],
        "function_name": "permute_unique",
        "starter_code": "def permute_unique(nums):\n    pass\n",
        "reference_solution": (
            "def permute_unique(nums):\n"
            "    nums = sorted(nums)\n    result = []\n    used = [False] * len(nums)\n    path = []\n"
            "    def backtrack():\n"
            "        if len(path) == len(nums):\n            result.append(path[:])\n            return\n"
            "        for i in range(len(nums)):\n"
            "            if used[i]:\n                continue\n"
            "            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:\n                continue\n"
            "            used[i] = True\n            path.append(nums[i])\n            backtrack()\n            path.pop()\n            used[i] = False\n"
            "    backtrack()\n    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(n!)",
        "test_cases": [
            {"args": [[1, 1, 2]], "hidden": False, "explanation": "one duplicate value"},
            {"args": [[2, 2]], "hidden": False, "explanation": "all identical -- only one distinct permutation"},
            {"args": [[1, 2, 3]], "hidden": True, "explanation": "no duplicates -- all 6 permutations distinct"},
        ],
        "hints": ["Sort the array first -- this puts equal values adjacent, which is what lets you detect and skip duplicate branches.", "At each position, skip a value equal to the previous one if the previous one hasn't been used yet in the current path -- that specific condition is what prevents duplicate permutations without missing valid ones.", "This is standard permutation backtracking with one extra duplicate-skipping rule layered on top."],
    },
    {
        "slug": "combination-sum-ii",
        "title": "Combination Sum II (No Reuse)",
        "primary_skill": "BACKTRACKING", "pattern_skills": ["BACKTRACKING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 4, "reasoning_difficulty": 3, "pattern_difficulty": 4,
        "statement": "Given `candidates` (each usable at most once, may contain duplicates) and a `target`, return all unique combinations that sum to target.",
        "constraints": "1 <= len(candidates) <= 100",
        "examples": [{"input": "candidates=[10,1,2,7,6,1,5], target=8", "output": "[[1,1,6],[1,2,5],[1,7],[2,6]]", "explanation": "each candidate used at most once per combination"}],
        "function_name": "combination_sum2",
        "starter_code": "def combination_sum2(candidates, target):\n    pass\n",
        "reference_solution": (
            "def combination_sum2(candidates, target):\n"
            "    candidates = sorted(candidates)\n    result = []\n"
            "    def backtrack(start, remaining, path):\n"
            "        if remaining == 0:\n            result.append(path[:])\n            return\n"
            "        for i in range(start, len(candidates)):\n"
            "            if i > start and candidates[i] == candidates[i - 1]:\n                continue\n"
            "            if candidates[i] > remaining:\n                break\n"
            "            path.append(candidates[i])\n            backtrack(i + 1, remaining - candidates[i], path)\n            path.pop()\n"
            "    backtrack(0, target, [])\n    return result\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(2^n)",
        "test_cases": [
            {"args": [[10, 1, 2, 7, 6, 1, 5], 8], "hidden": False, "explanation": "classic example"},
            {"args": [[2, 5, 2, 1, 2], 5], "hidden": False, "explanation": "multiple duplicate 2s"},
            {"args": [[1], 2], "hidden": True, "explanation": "no valid combination"},
        ],
        "hints": ["Sort first so duplicate values sit next to each other, making them easy to skip.", "Unlike unlimited-reuse combination sum, the recursive call must advance past the current index (i+1), not stay at i.", "At the same recursion depth (same `start`), skip over a candidate equal to the previous one you already tried -- that's what avoids duplicate combinations."],
    },
    {
        "slug": "diameter-of-binary-tree",
        "title": "Diameter of a Binary Tree",
        "primary_skill": "TREES", "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "easy",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a binary tree (level-order form), return the length (in edges) of the longest path between any two nodes -- this path may or may not pass through the root.",
        "constraints": "1 <= number of nodes <= 10^4",
        "examples": [{"input": "[1,2,3,4,5]", "output": "3", "explanation": "the longest path goes through nodes 4-2-1-3 or 5-2-1-3"}],
        "function_name": "diameter_of_binary_tree",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef diameter_of_binary_tree(root):\n    pass\n",
        "reference_solution": (
            "def diameter_of_binary_tree(root):\n"
            "    diameter = 0\n"
            "    def depth(node):\n"
            "        nonlocal diameter\n"
            "        if node is None:\n            return 0\n"
            "        l = depth(node.left)\n        r = depth(node.right)\n"
            "        diameter = max(diameter, l + r)\n"
            "        return 1 + max(l, r)\n"
            "    depth(root)\n    return diameter\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5]], "hidden": False, "explanation": "diameter passes through the root"},
            {"args": [[1, 2]], "hidden": False, "explanation": "a single edge"},
            {"args": [[1]], "hidden": True, "explanation": "single node -- no path exists"},
        ],
        "hints": ["The diameter at any node is the sum of its left and right subtree depths -- track the best such sum seen anywhere in the tree, not just at the root.", "A single depth-first traversal can compute both each subtree's depth AND update the running best diameter at the same time.", "The path doesn't have to pass through the root -- it could be entirely within one subtree, which is why you must check every node, not just the top one."],
    },
    {
        "slug": "binary-tree-level-order-traversal",
        "title": "Binary Tree Level Order Traversal",
        "primary_skill": "TREES", "pattern_skills": ["TREES", "QUEUE_DEQUE"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a binary tree (level-order form), return its node values grouped level by level, top to bottom.",
        "constraints": "0 <= number of nodes <= 2000",
        "examples": [{"input": "[3,9,20,None,None,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": "one list per depth level"}],
        "function_name": "level_order",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef level_order(root):\n    pass\n",
        "reference_solution": (
            "def level_order(root):\n"
            "    if root is None:\n        return []\n"
            "    result = []\n    queue = [root]\n"
            "    while queue:\n"
            "        level = []\n        next_queue = []\n"
            "        for node in queue:\n"
            "            level.append(node.val)\n"
            "            if node.left:\n                next_queue.append(node.left)\n"
            "            if node.right:\n                next_queue.append(node.right)\n"
            "        result.append(level)\n        queue = next_queue\n"
            "    return result\n"
        ),
        "io_transform": {"args": {"0": "binary_tree"}},
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "hidden": False, "explanation": "typical case"},
            {"args": [[1]], "hidden": False, "explanation": "single node"},
            {"args": [[]], "hidden": True, "explanation": "empty tree"},
        ],
        "hints": ["A queue is exactly the right structure for level-by-level (breadth-first) processing.", "Process one whole level's worth of nodes at a time, collecting their children into a separate list for the next level.", "The number of nodes in the queue at the start of each loop iteration is exactly the current level's size."],
    },
    {
        "slug": "construct-binary-tree-preorder-inorder",
        "title": "Construct Binary Tree from Preorder and Inorder",
        "primary_skill": "TREES", "pattern_skills": ["TREES", "RECURSION"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given `preorder` and `inorder` traversals of a binary tree with unique values, reconstruct and return the tree.",
        "constraints": "1 <= len(preorder) <= 3000, all values unique",
        "examples": [{"input": "preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]", "output": "the original tree", "explanation": "preorder gives the root first, inorder splits left/right subtrees"}],
        "function_name": "build_tree",
        "starter_code": "# A TreeNode class is provided: TreeNode(val, left=None, right=None)\ndef build_tree(preorder, inorder):\n    pass\n",
        "reference_solution": (
            "def build_tree(preorder, inorder):\n"
            "    if not preorder:\n        return None\n"
            "    root_val = preorder[0]\n    root = TreeNode(root_val)\n"
            "    mid = inorder.index(root_val)\n"
            "    root.left = build_tree(preorder[1:mid + 1], inorder[:mid])\n"
            "    root.right = build_tree(preorder[mid + 1:], inorder[mid + 1:])\n"
            "    return root\n"
        ),
        "io_transform": {"result": "binary_tree"},
        "expected_complexity": "O(n^2)",
        "test_cases": [
            {"args": [[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]], "hidden": False, "explanation": "classic example"},
            {"args": [[-1], [-1]], "hidden": False, "explanation": "single node"},
            {"args": [[1, 2], [2, 1]], "hidden": True, "explanation": "a left-only chain"},
        ],
        "hints": ["Preorder always lists the root first -- that immediately tells you the current subtree's root value.", "Find that root value's position in the inorder slice -- everything to its left in inorder is the left subtree, everything to its right is the right subtree.", "Recurse on the matching preorder/inorder slices for each side; the sizes must match up since both slices describe the same subtree."],
    },
    {
        "slug": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "primary_skill": "STRINGS", "pattern_skills": ["STRINGS", "TWO_POINTER"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a string `s`, return its longest palindromic substring. Test cases are chosen so the longest palindrome is unique, so there is exactly one correct answer.",
        "constraints": "1 <= len(s) <= 1000",
        "examples": [{"input": '"racecar"', "output": '"racecar"', "explanation": "the whole string is a palindrome"}],
        "function_name": "longest_palindrome",
        "starter_code": "def longest_palindrome(s):\n    pass\n",
        "reference_solution": (
            "def longest_palindrome(s):\n"
            "    if not s:\n        return ''\n"
            "    start, end = 0, 0\n"
            "    def expand(l, r):\n"
            "        while l >= 0 and r < len(s) and s[l] == s[r]:\n            l -= 1; r += 1\n"
            "        return l + 1, r - 1\n"
            "    for i in range(len(s)):\n"
            "        l1, r1 = expand(i, i)\n"
            "        if r1 - l1 > end - start:\n            start, end = l1, r1\n"
            "        l2, r2 = expand(i, i + 1)\n"
            "        if r2 - l2 > end - start:\n            start, end = l2, r2\n"
            "    return s[start:end + 1]\n"
        ),
        "expected_complexity": "O(n^2)",
        "test_cases": [
            {"args": ["racecar"], "hidden": False, "explanation": "the whole string is the palindrome"},
            {"args": ["noon"], "hidden": False, "explanation": "an even-length palindrome"},
            {"args": ["a"], "hidden": True, "explanation": "single character"},
        ],
        "hints": ["A palindrome can be found by expanding outward from a center -- but the center could be a single character (odd length) or between two characters (even length).", "Try both kinds of centers at every position and keep the longest palindrome found.", "This is O(n^2) but far simpler to get right than the linear-time Manacher's algorithm, and fast enough for this problem's constraints."],
    },
    {
        "slug": "group-anagrams",
        "title": "Group Anagrams",
        "primary_skill": "STRINGS", "pattern_skills": ["STRINGS", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given an array of strings `strs`, group the anagrams together. Return the groups in any order.",
        "constraints": "1 <= len(strs) <= 10^4",
        "examples": [{"input": '["eat","tea","tan","ate","nat","bat"]', "output": '[["eat","tea","ate"],["tan","nat"],["bat"]]', "explanation": "grouped by shared sorted-letter signature"}],
        "function_name": "group_anagrams",
        "starter_code": "def group_anagrams(strs):\n    pass\n",
        "reference_solution": (
            "def group_anagrams(strs):\n"
            "    groups = {}\n"
            "    for s in strs:\n"
            "        key = ''.join(sorted(s))\n        groups.setdefault(key, []).append(s)\n"
            "    return list(groups.values())\n"
        ),
        "output_comparison": "unordered_nested",
        "expected_complexity": "O(n * k log k)",
        "test_cases": [
            {"args": [["eat", "tea", "tan", "ate", "nat", "bat"]], "hidden": False, "explanation": "typical case"},
            {"args": [[""]], "hidden": False, "explanation": "a single empty string"},
            {"args": [["a"]], "hidden": True, "explanation": "a single character"},
        ],
        "hints": ["Two strings are anagrams exactly when their sorted characters match -- that sorted form makes a natural grouping key.", "A hashmap from sorted-signature to the list of original strings sharing it groups everything in one pass.", "The order of groups, and the order within a group, doesn't need to match any particular convention -- any valid grouping is accepted."],
    },
    {
        "slug": "minimum-window-substring",
        "title": "Minimum Window Substring",
        "primary_skill": "SLIDING_WINDOW", "pattern_skills": ["SLIDING_WINDOW", "HASHING"],
        "difficulty": "hard",
        "concept_difficulty": 4, "implementation_difficulty": 4, "reasoning_difficulty": 5, "pattern_difficulty": 4,
        "statement": "Given strings `s` and `t`, return the smallest substring of s that contains every character of t (including duplicates). Return an empty string if no such substring exists.",
        "constraints": "1 <= len(s), len(t) <= 10^5",
        "examples": [{"input": 's="ADOBECODEBANC", t="ABC"', "output": '"BANC"', "explanation": "the smallest window containing A, B, and C"}],
        "function_name": "min_window",
        "starter_code": "def min_window(s, t):\n    pass\n",
        "reference_solution": (
            "from collections import Counter\n"
            "def min_window(s, t):\n"
            "    if not t or not s:\n        return ''\n"
            "    need = Counter(t)\n    missing = len(t)\n    left = 0\n"
            "    best_left, best_right = 0, float('inf')\n"
            "    for right, c in enumerate(s, 1):\n"
            "        if need[c] > 0:\n            missing -= 1\n"
            "        need[c] -= 1\n"
            "        if missing == 0:\n"
            "            while left < right and need[s[left]] < 0:\n                need[s[left]] += 1\n                left += 1\n"
            "            if right - left < best_right - best_left:\n                best_left, best_right = left, right\n"
            "    return s[best_left:best_right] if best_right <= len(s) else ''\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["ADOBECODEBANC", "ABC"], "hidden": False, "explanation": "classic example"},
            {"args": ["a", "a"], "hidden": False, "explanation": "the whole string is the answer"},
            {"args": ["a", "aa"], "hidden": True, "explanation": "impossible -- not enough 'a's"},
        ],
        "hints": ["Expand the window until it contains every needed character (including duplicate counts), then shrink from the left as much as possible while it still does.", "A running 'missing count' (how many more characters are needed) avoids re-checking the entire need-map on every step.", "Every time the window becomes valid, check if it's the smallest valid window seen so far before continuing to shrink it."],
    },
    {
        "slug": "permutation-in-string",
        "title": "Permutation in String",
        "primary_skill": "SLIDING_WINDOW", "pattern_skills": ["SLIDING_WINDOW", "HASHING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given strings `s1` and `s2`, return True if `s2` contains a permutation of `s1` as a contiguous substring.",
        "constraints": "1 <= len(s1) <= len(s2) <= 10^4",
        "examples": [{"input": 's1="ab", s2="eidbaooo"', "output": "true", "explanation": "\"ba\" (a permutation of ab) appears in s2"}],
        "function_name": "check_inclusion",
        "starter_code": "def check_inclusion(s1, s2):\n    pass\n",
        "reference_solution": (
            "from collections import Counter\n"
            "def check_inclusion(s1, s2):\n"
            "    need = Counter(s1)\n    window = Counter()\n    n = len(s1)\n"
            "    for i, c in enumerate(s2):\n"
            "        window[c] += 1\n"
            "        if i >= n:\n"
            "            left_char = s2[i - n]\n            window[left_char] -= 1\n"
            "            if window[left_char] == 0:\n                del window[left_char]\n"
            "        if window == need:\n            return True\n"
            "    return False\n"
        ),
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": ["ab", "eidbaooo"], "hidden": False, "explanation": "a permutation is present"},
            {"args": ["ab", "eidboaoo"], "hidden": False, "explanation": "no permutation present"},
            {"args": ["adc", "dcda"], "hidden": True, "explanation": "a permutation present later in the string"},
        ],
        "hints": ["A permutation of s1 is just any window of s2 (the same length as s1) with the exact same character frequency counts as s1.", "Maintain a fixed-size sliding window of length len(s1) over s2, updating a running frequency count as it slides.", "Comparing the window's frequency count to s1's frequency count directly tells you whether the current window is a permutation."],
    },
    {
        "slug": "rotate-array",
        "title": "Rotate Array",
        "primary_skill": "ARRAYS_TRAVERSAL", "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 2, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given an array `nums` and an integer `k`, return the array rotated to the right by k steps.",
        "constraints": "1 <= len(nums) <= 10^5, 0 <= k <= 10^5",
        "examples": [{"input": "nums=[1,2,3,4,5,6,7], k=3", "output": "[5,6,7,1,2,3,4]", "explanation": "the last 3 elements move to the front"}],
        "function_name": "rotate_array",
        "starter_code": "def rotate_array(nums, k):\n    pass\n",
        "reference_solution": "def rotate_array(nums, k):\n    n = len(nums)\n    k %= n\n    return nums[-k:] + nums[:-k] if k else nums[:]\n",
        "expected_complexity": "O(n)",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5, 6, 7], 3], "hidden": False, "explanation": "typical case"},
            {"args": [[-1, -100, 3, 99], 2], "hidden": False, "explanation": "another typical case"},
            {"args": [[1, 2], 0], "hidden": True, "explanation": "no rotation needed"},
        ],
        "hints": ["k can be larger than the array's length -- taking k modulo the length first avoids unnecessary full rotations.", "The last k elements end up at the front, and everything else shifts right -- that's just a slice-and-concatenate.", "Watch the k=0 edge case: slicing with `[-0:]` behaves like `[0:]`, which is NOT the same as 'no rotation' -- handle it explicitly."],
    },
    {
        "slug": "spiral-matrix",
        "title": "Spiral Matrix Traversal",
        "primary_skill": "ARRAYS_TRAVERSAL", "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 4, "reasoning_difficulty": 2, "pattern_difficulty": 3,
        "statement": "Given a 2D `matrix`, return all its elements in spiral order (clockwise, starting from the top-left).",
        "constraints": "1 <= rows, cols <= 10",
        "examples": [{"input": "[[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]", "explanation": "spiraling clockwise inward"}],
        "function_name": "spiral_order",
        "starter_code": "def spiral_order(matrix):\n    pass\n",
        "reference_solution": (
            "def spiral_order(matrix):\n"
            "    result = []\n"
            "    if not matrix:\n        return result\n"
            "    top, bottom = 0, len(matrix) - 1\n    left, right = 0, len(matrix[0]) - 1\n"
            "    while top <= bottom and left <= right:\n"
            "        for c in range(left, right + 1):\n            result.append(matrix[top][c])\n        top += 1\n"
            "        for r in range(top, bottom + 1):\n            result.append(matrix[r][right])\n        right -= 1\n"
            "        if top <= bottom:\n"
            "            for c in range(right, left - 1, -1):\n                result.append(matrix[bottom][c])\n            bottom -= 1\n"
            "        if left <= right:\n"
            "            for r in range(bottom, top - 1, -1):\n                result.append(matrix[r][left])\n            left += 1\n"
            "    return result\n"
        ),
        "expected_complexity": "O(rows * cols)",
        "test_cases": [
            {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "hidden": False, "explanation": "square matrix"},
            {"args": [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], "hidden": False, "explanation": "non-square matrix"},
            {"args": [[[1]]], "hidden": True, "explanation": "single element"},
        ],
        "hints": ["Track four shrinking boundaries (top, bottom, left, right) and walk each edge in turn: right along the top, down the right side, left along the bottom, up the left side.", "After completing a side, move that boundary inward -- that's what keeps the spiral from retracing itself.", "Check the boundaries are still valid (top <= bottom, left <= right) before each of the bottom and left edges specifically -- a single row or column can otherwise get traversed twice."],
    },
    {
        "slug": "set-matrix-zeroes",
        "title": "Set Matrix Zeroes",
        "primary_skill": "ARRAYS_TRAVERSAL", "pattern_skills": ["ARRAYS_TRAVERSAL"],
        "difficulty": "medium",
        "concept_difficulty": 2, "implementation_difficulty": 3, "reasoning_difficulty": 2, "pattern_difficulty": 2,
        "statement": "Given a matrix, if an element is 0, set its entire row and column to 0. Return the resulting matrix.",
        "constraints": "1 <= rows, cols <= 200",
        "examples": [{"input": "[[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]", "explanation": "the row and column of the 0 both get zeroed"}],
        "function_name": "set_zeroes",
        "starter_code": "def set_zeroes(matrix):\n    pass\n",
        "reference_solution": (
            "def set_zeroes(matrix):\n"
            "    rows, cols = len(matrix), len(matrix[0])\n"
            "    zero_rows, zero_cols = set(), set()\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if matrix[r][c] == 0:\n                zero_rows.add(r); zero_cols.add(c)\n"
            "    result = [row[:] for row in matrix]\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if r in zero_rows or c in zero_cols:\n                result[r][c] = 0\n"
            "    return result\n"
        ),
        "expected_complexity": "O(rows * cols)",
        "test_cases": [
            {"args": [[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], "hidden": False, "explanation": "single zero"},
            {"args": [[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]], "hidden": False, "explanation": "two zeroes affecting overlapping rows/columns"},
            {"args": [[[1]]], "hidden": True, "explanation": "single element, no zero"},
        ],
        "hints": ["First scan the whole matrix just to record which rows and columns contain a zero -- don't zero anything out yet, or you'll create new zeroes that cascade incorrectly.", "Once you know every 'to be zeroed' row and column, do a second pass to actually apply the zeroes.", "Build the result on a fresh copy rather than mutating cells you might still need to read."],
    },
    {
        "slug": "unique-paths",
        "title": "Unique Paths in a Grid",
        "primary_skill": "DP_BASICS", "pattern_skills": ["DP_BASICS"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 2, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "A robot starts at the top-left of an `m x n` grid and can only move right or down. Return the number of distinct paths to the bottom-right corner.",
        "constraints": "1 <= m, n <= 100",
        "examples": [{"input": "m=3, n=7", "output": "28", "explanation": "28 distinct right/down paths"}],
        "function_name": "unique_paths",
        "starter_code": "def unique_paths(m, n):\n    pass\n",
        "reference_solution": (
            "def unique_paths(m, n):\n"
            "    dp = [[1] * n for _ in range(m)]\n"
            "    for i in range(1, m):\n"
            "        for j in range(1, n):\n            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]\n"
            "    return dp[m - 1][n - 1]\n"
        ),
        "expected_complexity": "O(m * n)",
        "test_cases": [
            {"args": [3, 7], "hidden": False, "explanation": "classic example"},
            {"args": [3, 2], "hidden": False, "explanation": "smaller grid"},
            {"args": [1, 1], "hidden": True, "explanation": "already at the destination"},
        ],
        "hints": ["Every cell in the top row or left column can only be reached one way -- straight across or straight down.", "Every other cell's path count is the sum of the cell above it and the cell to its left, since those are the only two ways to arrive.", "This is a classic 2D DP table fill, very similar in shape to a grid-based edit-distance or knapsack table."],
    },
    {
        "slug": "word-break",
        "title": "Word Break",
        "primary_skill": "DP_BASICS", "pattern_skills": ["DP_BASICS", "DP_STRING"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 3, "pattern_difficulty": 3,
        "statement": "Given a string `s` and a dictionary `word_dict`, return True if s can be segmented into a space-separated sequence of one or more dictionary words.",
        "constraints": "1 <= len(s) <= 300",
        "examples": [{"input": 's="leetcode", word_dict=["leet","code"]', "output": "true", "explanation": "\"leet\" + \"code\""}],
        "function_name": "word_break",
        "starter_code": "def word_break(s, word_dict):\n    pass\n",
        "reference_solution": (
            "def word_break(s, word_dict):\n"
            "    word_set = set(word_dict)\n    n = len(s)\n"
            "    dp = [False] * (n + 1)\n    dp[0] = True\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(i):\n"
            "            if dp[j] and s[j:i] in word_set:\n                dp[i] = True\n                break\n"
            "    return dp[n]\n"
        ),
        "expected_complexity": "O(n^2)",
        "test_cases": [
            {"args": ["leetcode", ["leet", "code"]], "hidden": False, "explanation": "classic example"},
            {"args": ["applepenapple", ["apple", "pen"]], "hidden": False, "explanation": "words reused"},
            {"args": ["catsandog", ["cats", "dog", "sand", "and", "cat"]], "hidden": True, "explanation": "no valid segmentation exists"},
        ],
        "hints": ["dp[i] means: can the first i characters of s be fully segmented into dictionary words?", "dp[i] is true if there's some earlier split point j where dp[j] is true AND s[j:i] is itself a dictionary word.", "Words can be reused any number of times -- this isn't like combination-sum-ii's 'use once' restriction."],
    },
    {
        "slug": "is-graph-bipartite",
        "title": "Is Graph Bipartite?",
        "primary_skill": "GRAPHS", "pattern_skills": ["GRAPHS", "QUEUE_DEQUE"],
        "difficulty": "medium",
        "concept_difficulty": 3, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 3,
        "statement": "Given an undirected graph as an adjacency list `graph` (graph[i] lists i's neighbors), return True if the graph's nodes can be split into two groups such that every edge connects nodes from different groups.",
        "constraints": "1 <= len(graph) <= 100",
        "examples": [{"input": "[[1,3],[0,2],[1,3],[0,2]]", "output": "true", "explanation": "alternating 2-coloring works: {0,2} and {1,3}"}],
        "function_name": "is_bipartite",
        "starter_code": "def is_bipartite(graph):\n    pass\n",
        "reference_solution": (
            "from collections import deque\n"
            "def is_bipartite(graph):\n"
            "    n = len(graph)\n    color = [0] * n\n"
            "    for start in range(n):\n"
            "        if color[start] != 0:\n            continue\n"
            "        color[start] = 1\n        q = deque([start])\n"
            "        while q:\n"
            "            node = q.popleft()\n"
            "            for nxt in graph[node]:\n"
            "                if color[nxt] == 0:\n                    color[nxt] = -color[node]\n                    q.append(nxt)\n"
            "                elif color[nxt] == color[node]:\n                    return False\n"
            "    return True\n"
        ),
        "expected_complexity": "O(nodes + edges)",
        "test_cases": [
            {"args": [[[1, 3], [0, 2], [1, 3], [0, 2]]], "hidden": False, "explanation": "a valid 2-coloring exists"},
            {"args": [[[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]], "hidden": False, "explanation": "an odd cycle blocks bipartiteness"},
            {"args": [[[], []]], "hidden": True, "explanation": "no edges at all -- trivially bipartite"},
        ],
        "hints": ["Try to 2-color the graph via BFS: color a node, then force every neighbor to the opposite color.", "If a neighbor already has a color and it matches the current node's color, that's a contradiction -- the graph isn't bipartite.", "The graph might not be fully connected -- restart the coloring process from any uncolored node until all nodes are covered."],
    },
    {
        "slug": "kruskal-mst",
        "title": "Minimum Spanning Tree Weight (Kruskal's)",
        "primary_skill": "GRAPHS", "pattern_skills": ["GRAPHS", "UNION_FIND"],
        "difficulty": "medium",
        "concept_difficulty": 4, "implementation_difficulty": 3, "reasoning_difficulty": 4, "pattern_difficulty": 4,
        "statement": "Given `n` nodes and weighted undirected `edges` as `[u, v, weight]`, return the total weight of a minimum spanning tree, or -1 if the graph isn't connected.",
        "constraints": "1 <= n <= 1000",
        "examples": [{"input": "n=4, edges=[[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]]", "output": "19", "explanation": "Kruskal's picks the cheapest edges that don't form a cycle"}],
        "function_name": "minimum_spanning_tree_weight",
        "starter_code": "def minimum_spanning_tree_weight(n, edges):\n    pass\n",
        "reference_solution": (
            "def minimum_spanning_tree_weight(n, edges):\n"
            "    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n"
            "    edges = sorted(edges, key=lambda e: e[2])\n"
            "    total = 0\n    count = 0\n"
            "    for u, v, w in edges:\n"
            "        ru, rv = find(u), find(v)\n"
            "        if ru != rv:\n"
            "            parent[ru] = rv\n            total += w\n            count += 1\n"
            "            if count == n - 1:\n                break\n"
            "    return total if count == n - 1 else -1\n"
        ),
        "expected_complexity": "O(edges log edges)",
        "test_cases": [
            {"args": [4, [[0, 1, 10], [0, 2, 6], [0, 3, 5], [1, 3, 15], [2, 3, 4]]], "hidden": False, "explanation": "classic example"},
            {"args": [3, [[0, 1, 1], [1, 2, 2], [0, 2, 3]]], "hidden": False, "explanation": "smaller graph"},
            {"args": [3, [[0, 1, 1]]], "hidden": True, "explanation": "not enough edges to connect all 3 nodes"},
        ],
        "hints": ["Kruskal's algorithm greedily takes the cheapest remaining edge, as long as it doesn't create a cycle.", "Union-Find is exactly the tool for 'would this edge create a cycle?' -- if both endpoints are already in the same component, skip it.", "If you can't connect all n nodes with n-1 edges by the time you run out of edges, the graph was never fully connected -- return -1."],
    },
]
