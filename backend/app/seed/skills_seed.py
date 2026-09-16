"""Seed skill graph nodes + prerequisite edges (spec section 60).

Each skill carries a `mnemonic` -- a short, concrete memory hook shown before the
full lesson so a learner gets a fast, sticky anchor for the concept before the
detailed explanation. Mnemonics aid recall of *what a concept is and when to use
it* -- they are not a substitute for understanding, and are shown alongside full
lessons and real practice problems, not instead of them.

Every lesson follows one consistent template so it genuinely spans beginner to
advanced within a single page, rather than assuming prior knowledge: What is it?
-> How it works -> Real-world analogy -> Worked example (a hand-traceable dry
run) -> Common mistakes -> When to use it / when not to -> An interview-style
question -> Key takeaway.
"""

SKILLS = [
    {"key": "PROGRAMMING_BASICS", "name": "Programming Foundations", "chapter": "Programming Foundations",
     "level": 0, "description": "variables, loops, functions, basic recursion",
     "mnemonic": "A recipe: ingredients (variables) + steps (statements) + repeat instructions (loops).",
     "comic_script": [
         {"speaker": "mira", "text": "I keep hearing 'variables,' 'loops,' 'functions' -- what do those actually mean, in plain words?"},
         {"speaker": "dev", "text": "Think of a recipe card. Ingredients are your variables -- named boxes holding a value. The numbered steps are your statements."},
         {"speaker": "mira", "text": "And 'repeat until golden brown'?"},
         {"speaker": "dev", "text": "That's a loop! And 'see Step 4, make the sauce' pointing to a separate card -- that's a function call."},
         {"speaker": "mira", "text": "Why do people keep saying 'trace through the code by hand'?"},
         {"speaker": "dev", "text": "Because it's the single most useful beginner skill -- literally writing down what each variable equals after every step, like following the recipe ingredient by ingredient instead of just reading it."},
         {"speaker": "mira", "text": "So programming is really just... those four ingredients, combined in different orders?"},
         {"speaker": "dev", "text": "Pretty much everything you'll learn builds on exactly those four things."},
     ],
     "concept_markdown": """# Programming Foundations

## What is it?
A program is a sequence of instructions a computer executes exactly as written, one after another, top to bottom -- unless you tell it to branch or repeat. Four ingredients cover almost everything you'll write for a long time: **variables** (named boxes that hold a value), **conditions** (`if`/`else` branches based on a true/false check), **loops** (repeat a block of instructions), and **functions** (a named, reusable block of instructions you can call by name).

## How it works
When you write `x = 5`, the computer reserves a box named `x` and puts the value 5 inside. `x = x + 1` reads the current value out of the box, computes 6, and puts 6 back in the *same* box -- the box's name never changes, only its contents. A loop like `for i in range(3):` runs its body three times, with `i` taking the values 0, 1, 2 in turn. A function like `def add(a, b): return a + b` packages logic so you don't retype it -- calling `add(2, 3)` substitutes 2 for `a` and 3 for `b`, runs the body, and gives back 5.

## Real-world analogy
A recipe card: ingredients are your variables, the numbered steps are your statements, "repeat until golden brown" is a loop, and "see Step 4 (make the sauce)" pointing to a separate card is a function call.

## Worked example (dry run)
```
total = 0
for x in [10, 20, 30]:
    total = total + x
```
| step | x | total |
|---|---|---|
| start | - | 0 |
| iteration 1 | 10 | 10 |
| iteration 2 | 20 | 30 |
| iteration 3 | 30 | 60 |

The loop ends with `total = 60`. Being able to produce this table by hand for any snippet -- called a *trace table* or *dry run* -- is the single most useful beginner skill in programming.

## Common mistakes
- Off-by-one errors: `range(n)` gives `0..n-1`, not `0..n` -- a frequent source of "why is my last element missing?" bugs.
- Confusing `=` (assignment: "make it equal") with `==` (comparison: "is it equal?").
- Forgetting that a loop variable keeps its *last* value after the loop ends, then accidentally reusing it.

## When to use what
Use a variable whenever you need to remember something between steps. Use a loop whenever you're repeating a similar action a known (or bounded) number of times. Use a function the moment you find yourself about to copy-paste the same block of code twice.

## Interview-style question
"Trace through this loop by hand and tell me what `total` equals at the end" -- interviewers ask this specifically to check you can mentally execute code, not just recognize patterns.

## Key takeaway
Every algorithm you'll ever learn is built from these four ingredients -- mastering dry-running code by hand (not just reading it) is the foundation everything else stands on."""},

    {"key": "ALGORITHMIC_THINKING", "name": "Algorithmic Thinking & Complexity", "chapter": "Algorithmic Thinking",
     "level": 0, "description": "big O, time complexity, space complexity, brute force vs optimal",
     "mnemonic": "Before coding, ask: 'Can this survive the constraints?' -- n = 10^5 already rules out O(n^2).",
     "comic_script": [
         {"speaker": "mira", "text": "What does 'Big O' actually mean? It always sounds so abstract."},
         {"speaker": "dev", "text": "Looking up a word in a dictionary two ways. Flipping page by page -- that's O(n), gets slower as the dictionary grows. Opening to the middle and halving your search each time -- that's O(log n)."},
         {"speaker": "mira", "text": "Both eventually find the word though, right?"},
         {"speaker": "dev", "text": "Sure, but one scales dramatically better. Big O is just describing HOW the work grows as the input grows -- not the exact seconds it takes."},
         {"speaker": "mira", "text": "Why do I need to know this before I even write code?"},
         {"speaker": "dev", "text": "Because if the problem says n could be 100,000, and your gut says 'nested loop,' that's already a red flag -- O(n^2) at that size is way too slow. Better to catch it on paper first."},
         {"speaker": "mira", "text": "So it's basically a sanity check, not academic decoration?"},
         {"speaker": "dev", "text": "Exactly -- it's the fastest, cheapest feedback loop you have, before you've written a single line."},
     ],
     "concept_markdown": """# Algorithmic Thinking

## What is it?
Time complexity describes how the *number of operations* an algorithm performs grows as the input size (usually called `n`) grows -- not how many seconds it takes (that depends on the computer), but how the workload scales.

## How it works
We describe growth with Big O notation, which captures the *dominant* term and ignores constants: an algorithm doing `3n + 7` operations is O(n); one doing `n^2 + 100n` is O(n^2), because for large n the n^2 term swamps everything else. Big Omega (Ω) describes a lower bound (best case), and Big Theta (Θ) describes a tight bound (when best and worst case match).

## Real-world analogy
Looking up a word in a dictionary two ways: flipping page by page (O(n), linear) versus opening to the middle and halving your search each time (O(log n), logarithmic). Both "work," but one scales dramatically better as the dictionary grows.

## Worked example
Given `n = 100,000` and roughly 10^8 operations/second as a rule of thumb:

| Complexity | Operations at n=100,000 | Feasible in ~1 second? |
|---|---|---|
| O(n) | 100,000 | yes, trivially |
| O(n log n) | ~1,700,000 | yes |
| O(n^2) | 10,000,000,000 | no -- 100x too slow |

This is why the first question before writing any code should be: **"Can this solution survive the given constraints?"** If constraints say n <= 10^5 and your instinct is nested loops, that's a signal to look for a better approach *before* you start typing.

## Common mistakes
- Assuming "it worked on the example" means it will pass -- examples are almost always small; the real test is the stated constraints.
- Confusing average-case with worst-case complexity (e.g. hashmap lookups are O(1) average, but O(n) worst case under adversarial collisions).
- Ignoring space complexity -- an O(n)-time solution using O(n) extra space can still fail a strict memory limit.

## When to use it
Always do this complexity check *before* coding, not after a "Time Limit Exceeded." It's the fastest possible feedback loop -- free, and it prevents wasted implementation effort on an approach that can never pass.

## Interview-style question
"What's the time and space complexity of your solution, and can you do better?" -- asked after nearly every coding interview problem. Practice stating complexity out loud, not just knowing it silently.

## Key takeaway
Complexity analysis isn't academic decoration -- it's the fastest sanity check you have, and skipping it is the most common reason a technically-correct idea fails under real constraints."""},

    {"key": "ARRAYS_TRAVERSAL", "name": "Array Traversal & Kadane's Technique", "chapter": "Arrays",
     "level": 1, "description": "single-pass traversal, running min/max, Kadane's maximum subarray technique",
     "mnemonic": "One pass, one running answer -- like reading a sentence once while keeping a tally.",
     "comic_script": [
         {"speaker": "mira", "text": "What's 'array traversal' -- isn't that just... a for loop?"},
         {"speaker": "dev", "text": "Basically, yeah, but with a twist: you keep a RUNNING value as you go. Like a car's odometer -- it doesn't remember every mile individually, just a running total that updates."},
         {"speaker": "mira", "text": "What's Kadane's technique -- I hear that name a lot?"},
         {"speaker": "dev", "text": "It's the classic example -- finding the best possible 'chunk' of the array in one pass, by deciding at each step: keep extending my current streak, or start fresh here?"},
         {"speaker": "mira", "text": "How do I know if a problem needs this pattern?"},
         {"speaker": "dev", "text": "If the answer only depends on a running summary of everything you've seen SO FAR, in order -- that's your cue."},
         {"speaker": "mira", "text": "And if I need to look backward at something way earlier?"},
         {"speaker": "dev", "text": "Then plain traversal isn't enough -- you'd need a hashmap, a stack, or prefix sums instead."},
     ],
     "concept_markdown": """# Array Traversal

## What is it?
Array traversal means visiting each element once, left to right (or right to left), while maintaining some running value -- a sum, a maximum, a count, a flag. It's the simplest and most common pattern in DSA, and a large fraction of "medium" problems are really just a traversal with the right running value.

## How it works
Initialize an accumulator before the loop, then update it at each step based on the current element (and sometimes the accumulator's previous value). Kadane's algorithm for maximum subarray sum is the canonical non-trivial traversal: at each position, decide whether to extend the current subarray or start fresh, via `current_sum = max(x, current_sum + x)`, tracking the best `current_sum` ever seen in a second variable.

## Real-world analogy
A car's odometer: it doesn't remember every mile you've ever driven individually, it just keeps a running total that updates with each new bit of distance.

## Worked example
`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`, Kadane's trace:

| x | current_sum = max(x, current_sum+x) | best so far |
|---|---|---|
| -2 | -2 | -2 |
| 1 | 1 | 1 |
| -3 | -2 | 1 |
| 4 | 4 | 4 |
| -1 | 3 | 4 |
| 2 | 5 | 5 |
| 1 | 6 | 6 |
| -5 | 1 | 6 |
| 4 | 4 | 6 |

Answer: 6 (the subarray `[4, -1, 2, 1]`).

## Common mistakes
- Forgetting all-negative arrays -- the answer there is the *least negative single element*, not 0 (0 would mean "the empty subarray," which most problem definitions disallow).
- Updating the "best" tracker *before* updating the running value, capturing the previous iteration's result instead of the current one.

## When to use it / when not to
Use a plain traversal whenever the answer only depends on a running summary of everything seen so far, in order. If you need to look *backward* at arbitrary earlier elements (not just the running summary), you likely need a different tool -- a hashmap, a stack, or prefix sums.

## Interview-style question
"Can you find the maximum subarray sum in O(n) instead of O(n^2)?" is a common warm-up specifically because it tests whether you can convert brute force into a running-accumulator traversal.

## Key takeaway
Before reaching for a fancier data structure, ask: "can a single pass with a running variable solve this?" -- it's the cheapest tool in the toolbox and solves more problems than beginners expect."""},

    {"key": "ARRAYS_PREFIX_SUM", "name": "Prefix Sum", "chapter": "Arrays",
     "level": 1, "description": "precomputed running totals for O(1) range sum queries",
     "mnemonic": "Prefix sum is a running total you precompute once -- like a bank statement's running balance column.",
     "comic_script": [
         {"speaker": "mira", "text": "If I need to answer 'sum between index 3 and 7' a THOUSAND times, do I really re-add every time?"},
         {"speaker": "dev", "text": "No! Think of a bank statement's running balance column. Instead of re-adding every transaction from account opening, you subtract two running-balance entries."},
         {"speaker": "mira", "text": "So I precompute the running totals ONCE up front?"},
         {"speaker": "dev", "text": "Exactly -- build the prefix array once, then every range-sum query becomes one subtraction. O(1) per query instead of re-scanning."},
         {"speaker": "mira", "text": "What if I mess up whether prefix[i] means 'up to i' or 'before i'?"},
         {"speaker": "dev", "text": "Classic off-by-one trap -- just pick ONE convention and stick with it consistently through the whole problem."},
         {"speaker": "mira", "text": "When would this NOT help?"},
         {"speaker": "dev", "text": "If the array keeps getting UPDATED between queries -- rebuilding the whole prefix array each time defeats the point. That's when you'd need a fancier structure instead."},
     ],
     "concept_markdown": """# Prefix Sum

## What is it?
A prefix sum array precomputes, for every position i, the sum of all elements before it. Once built, the sum of any range `[l, r]` can be answered in O(1) instead of re-adding elements every time.

## How it works
Build `prefix[0] = 0`, then `prefix[i+1] = prefix[i] + nums[i]`. The sum of `nums[l..r]` (inclusive) is `prefix[r+1] - prefix[l]` -- subtracting "everything before l" from "everything up to and including r" leaves exactly the range you want.

## Real-world analogy
A bank statement's running balance column: instead of re-adding every transaction from account opening to answer "what was my balance between March and June," you subtract two running-balance entries.

## Worked example
`nums = [1, 2, 3, 4, 5]` -> `prefix = [0, 1, 3, 6, 10, 15]`. Sum of `nums[1..3]` (values 2, 3, 4 = 9): `prefix[4] - prefix[1] = 10 - 1 = 9`. Correct.

## Common mistakes
- Off-by-one indexing: forgetting whether `prefix[i]` means "sum up to and including i" or "sum before i" -- pick one convention and stay consistent (this lesson uses "before i").
- Rebuilding the prefix array on every query instead of once up front -- defeats the entire point.

## When to use it / when not to
Use it when you'll answer *many* range-sum queries on a *static* (unchanging) array. If the array is updated frequently between queries, a plain prefix sum becomes expensive to rebuild -- a Fenwick tree / segment tree is the upgrade path (not covered in this starter curriculum).

## Interview-style question
"Given many queries asking for the sum between two indices, how would you avoid O(n) work per query?" -- tests whether you reach for precomputation instead of repeating work.

## Key takeaway
Whenever "the same kind of range query" will be asked more than once, ask whether precomputing a running structure turns O(n) per query into O(1)."""},

    {"key": "HASHING", "name": "Hashing (HashMap / HashSet)", "chapter": "Hashing",
     "level": 1, "description": "O(1) average lookup, complement search, frequency counting, grouping",
     "mnemonic": "Think 'phonebook' -- look up a name (key) and instantly get a number (value), no scanning required.",
     "comic_script": [
         {"speaker": "mira", "text": "How does a hashmap find something instantly, without checking every item?"},
         {"speaker": "dev", "text": "A phonebook indexed by name -- you don't read every entry to find 'Smith, John,' you jump straight to the S section."},
         {"speaker": "mira", "text": "How does it know WHERE to jump?"},
         {"speaker": "dev", "text": "It runs your key through a hash function, turning it into a number that roughly tells it where to look. Same trick on lookup -- hash it again, jump straight there."},
         {"speaker": "mira", "text": "When would I reach for this instead of just looping?"},
         {"speaker": "dev", "text": "Anytime you catch yourself thinking 'have I seen this before,' or 'what's the complement of this value' -- that's basically a neon sign pointing at hashing."},
         {"speaker": "mira", "text": "Is there ever a downside?"},
         {"speaker": "dev", "text": "If you genuinely need things in a specific ORDER and queried by position, a hashmap won't help -- it trades order for speed."},
     ],
     "concept_markdown": """# Hashing

## What is it?
A hashmap (dictionary) stores key-value pairs and gives O(1) average-time lookup, insertion, and deletion by key -- no scanning required. A hashset is the same idea without values: just "have I seen this before?"

## How it works
A hash function converts a key into a number (a hash), which determines roughly where in an internal array the pair is stored. Looking up a key hashes it again and jumps straight to that location, instead of checking every stored item one by one.

## Real-world analogy
A phonebook indexed by name: you don't read every entry to find "Smith, John" -- you jump straight to the S section. A hashmap does this automatically for any type of key.

## Worked example
Two Sum: `nums = [2, 7, 11, 15], target = 9`. Walk left to right, and before inserting each number, check if its *complement* (`target - x`) is already in the map:

| x | need = target - x | in map? | action |
|---|---|---|---|
| 2 | 7 | no | insert 2 -> index 0 |
| 7 | 2 | yes (2 -> 0) | return [0, 1] |

This turns an O(n^2) nested-loop search into a single O(n) pass.

## Common mistakes
- Checking "is the complement in the map" *after* inserting the current element -- can incorrectly match an element with itself.
- Using a list/array for "have I seen this" checks when a hashset would make it O(1) instead of O(n) per check.

## When to use it / when not to
**When should you think about hashing?** Whenever a problem needs "have I seen this value before," "what's the complement of this value," or "group items by some shared property," faster than a nested loop. Don't reach for it when order matters and must be preserved *and* queried by position -- an array or a specialized ordered structure fits better there.

## Interview-style question
"Can you solve this without a nested loop?" is often a direct hint toward hashing -- interviewers ask this the moment they see an O(n^2) brute force with an obvious "have I seen X" check inside it.

## Key takeaway
A hashmap trades a bit of space for turning "search" into "lookup" -- recognize the phrase "have I seen this before" as your cue to reach for one."""},

    {"key": "TWO_POINTER", "name": "Two Pointers", "chapter": "Two Pointers",
     "level": 1, "description": "opposite-direction and same-direction pointer techniques on sorted/ordered data",
     "mnemonic": "Two people walking toward each other from opposite ends of a rope.",
     "comic_script": [
         {"speaker": "mira", "text": "Two pointers -- is that just... two loop variables?"},
         {"speaker": "dev", "text": "Sort of, but moving with PURPOSE. Two people at opposite ends of a tug-of-war rope, both stepping toward the middle -- they'll meet way faster than one person walking the whole rope alone."},
         {"speaker": "mira", "text": "How does it actually decide which pointer to move?"},
         {"speaker": "dev", "text": "Say you're looking for a pair summing to a target in a sorted array. Sum too small? Move the left pointer right. Too big? Move the right pointer left."},
         {"speaker": "mira", "text": "Why does the array need to be sorted for this?"},
         {"speaker": "dev", "text": "Because sorted order is what makes 'move this direction' a MEANINGFUL decision -- on unsorted data, you'd have no idea which way actually helps."},
         {"speaker": "mira", "text": "What if I need to remember the ORIGINAL positions, before sorting?"},
         {"speaker": "dev", "text": "Track the original index alongside the value before you sort -- sorting shouldn't mean losing information you still need."},
     ],
     "concept_markdown": """# Two Pointers

## What is it?
The two-pointer technique uses two indices moving through a sorted (or orderable) sequence -- either from opposite ends inward, or both moving the same direction at different speeds -- to avoid the O(n^2) cost of checking every pair.

## How it works
For "find a pair summing to a target in a sorted array": start one pointer at the beginning, one at the end. If the pair's sum is too small, move the left pointer right (increase the sum); if too large, move the right pointer left (decrease the sum). Each comparison eliminates at least one candidate pair, giving O(n) total instead of O(n^2).

## Real-world analogy
Two people at opposite ends of a tug-of-war rope, each stepping toward the middle -- they'll meet (or cross) far faster than one person walking the entire rope alone checking every mark.

## Worked example
`nums = [2, 7, 11, 15], target = 9`, sorted already:

| left | right | sum | action |
|---|---|---|---|
| 2 | 15 | 17 | too big, move right pointer left |
| 2 | 11 | 13 | too big, move right pointer left |
| 2 | 7 | 9 | match! return [0, 1] |

## Common mistakes
- Applying two pointers to an *unsorted* array without sorting first (or realizing the problem's structure already guarantees order).
- Moving both pointers on a "too big" or "too small" result when only one pointer's movement is actually justified by the comparison.

## When to use it / when not to
**Recognition rule:** the data is sorted (or can be usefully sorted) and two positions need to interact based on a comparison. It doesn't apply well when you need to consider *all* pairs regardless of order, or when sorting would destroy information you need (like original indices) -- track the original index alongside the value in that case.

## Interview-style question
"Can you avoid checking every pair?" on a sorted-array problem is the standard prompt toward two pointers -- interviewers will often deliberately give a problem where two pointers works but a wrong greedy variant doesn't, to test real understanding versus pattern-matching.

## Key takeaway
Sorted data plus "two things need to interact" is the strongest signal for two pointers -- it converts an O(n^2) comparison grid into a single O(n) sweep."""},

    {"key": "SLIDING_WINDOW", "name": "Sliding Window", "chapter": "Sliding Window",
     "level": 2, "description": "fixed/variable window over contiguous subarrays or substrings",
     "mnemonic": "A train window sliding along the train -- you only ever see what's currently framed.",
     "comic_script": [
         {"speaker": "mira", "text": "Sliding window sounds fancy. Is it different from two pointers?"},
         {"speaker": "dev", "text": "It's two pointers, specialized for CONTIGUOUS chunks. Imagine dragging a magnifying glass along a line of text -- you only ever see what's currently under the glass."},
         {"speaker": "mira", "text": "When does the window grow versus shrink?"},
         {"speaker": "dev", "text": "You almost always expand the right edge every step. You shrink the left edge only when the current window becomes 'invalid' by whatever rule the problem gives you."},
         {"speaker": "mira", "text": "What kind of rule?"},
         {"speaker": "dev", "text": "Like 'at most 2 distinct characters.' The instant you'd have a 3rd, you shrink from the left until you're valid again."},
         {"speaker": "mira", "text": "How do I recognize a sliding window problem?"},
         {"speaker": "dev", "text": "Words like 'longest substring' or 'smallest subarray' plus some validity condition are basically a neon sign pointing right at this pattern."},
     ],
     "concept_markdown": """# Sliding Window

## What is it?
Sliding window is the two-pointer technique specialized for *contiguous* segments: you maintain a window `[left, right]` over the array/string, expanding and shrinking it based on whether the current window is "valid" for the problem's condition.

## How it works
Every sliding window problem answers four questions: **What is the window?** (a contiguous subarray/substring) **What makes it valid?** (some condition, e.g. "at most k distinct characters") **When do we expand?** (move `right` forward, almost always every iteration) **When do we shrink?** (move `left` forward, when the window becomes invalid, in a `while` loop).

## Real-world analogy
Watching a moving train through a fixed window frame at a platform, or dragging a magnifying glass along a printed line of text -- you only ever see (and reason about) what's currently inside the frame.

## Worked example
Longest substring with at most 2 distinct characters, on `"eceba"`:

| right | char | window | distinct | valid? | action |
|---|---|---|---|---|---|
| 0 | e | "e" | 1 | yes | best=1 |
| 1 | c | "ec" | 2 | yes | best=2 |
| 2 | e | "ece" | 2 | yes | best=3 |
| 3 | b | "eceb" | 3 | no | shrink until valid -> "eb" |
| 4 | a | "eba" | 2 | yes | best stays 3 |

Answer: 3 (`"ece"`).

## Common mistakes
- Using a plain `if` instead of a `while` loop for shrinking -- sometimes you need to shrink more than once per expansion.
- Forgetting to update the frequency map/count when a character *leaves* the window on the left, not just when one enters on the right.

## When to use it / when not to
Use it when the problem explicitly involves a *contiguous* subarray/substring and some notion of validity that changes smoothly as the window edges move. If the elements you need don't have to be contiguous, sliding window doesn't apply -- look at subsequence-based techniques (often DP) instead.

## Interview-style question
"Find the longest/shortest substring satisfying some condition" is the sliding-window interview signature -- the words "longest substring" or "smallest subarray" together with a validity condition are a strong tell.

## Key takeaway
A sliding window is just two pointers with a validity check driving expansion and shrinkage -- master the four-question framework and most window problems become mechanical."""},

    {"key": "BINARY_SEARCH", "name": "Binary Search", "chapter": "Binary Search",
     "level": 1, "description": "search on sorted arrays and on answer spaces",
     "mnemonic": "Guess-the-number 1-100: always ask about the middle, throw away half the possibilities.",
     "comic_script": [
         {"speaker": "mira", "text": "How does binary search find something so fast, even in a huge array?"},
         {"speaker": "dev", "text": "The classic 'guess a number between 1 and 100' game. Optimal strategy: always guess the MIDDLE of what's still possible, not counting up from 1."},
         {"speaker": "mira", "text": "So each guess throws away half the remaining options?"},
         {"speaker": "dev", "text": "Exactly -- you can win in 7 guesses or fewer for 1 to 100. That's the whole power of halving the search space every step."},
         {"speaker": "mira", "text": "Does this only work on sorted arrays?"},
         {"speaker": "dev", "text": "That's the surprising part -- it works on ANY yes/no question where the answer is monotonic. Like 'can I ship all packages within D days?' -- if D days works, D+1 also works."},
         {"speaker": "mira", "text": "What happens if that monotonic property doesn't actually hold?"},
         {"speaker": "dev", "text": "Then binary search will confidently give you a WRONG answer without any error -- always double-check monotonicity before reaching for this."},
     ],
     "concept_markdown": """# Binary Search

## What is it?
Binary search finds a target (or a boundary) in O(log n) time by repeatedly halving the search space -- but its real power is searching an *answer space*, not just an array.

## How it works
Maintain `lo` and `hi` bounds. Check the midpoint; if it's the target, done. If the target must be larger, move `lo` past the midpoint; if smaller, move `hi` below the midpoint. Each check eliminates half the remaining candidates, giving O(log n) total checks.

## Real-world analogy
The "guess a number between 1 and 100" game: the optimal strategy always guesses the midpoint of what's still possible, not counting up from 1 -- you can win in 7 guesses or fewer for 1-100 (2^7 = 128).

## Worked example
Find 7 in `[1,3,5,7,9,11]`:

| lo | hi | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 5 | 5<7, lo=3 |
| 3 | 5 | 4 | 9 | 9>7, hi=3 |
| 3 | 3 | 3 | 7 | found, return 3 |

## Common mistakes
- Infinite loops from `mid` calculations that don't make progress (e.g. `hi = mid` instead of `hi = mid - 1` when `mid` has already been ruled out).
- Assuming binary search only works on sorted *arrays* -- it works on any monotonic *answer space*: "once true, always true for larger (or smaller) candidates."

## When to use it / when not to
Beyond "search a sorted array," use it whenever you can ask "is answer X feasible?" and feasibility is monotonic in X (e.g. "can I ship all packages within D days?" -- if D days works, D+1 days also works). If feasibility isn't monotonic, binary search on the answer will silently give a wrong result -- verify monotonicity first.

## Interview-style question
"Can you do this in better than O(n)?" on a sorted-input problem is the standard nudge -- and "binary search on the answer" is a favorite advanced follow-up once basic binary search is mastered.

## Key takeaway
Binary search isn't "an algorithm for arrays" -- it's a general strategy for any monotonic yes/no question, and recognizing the monotonicity is the real skill."""},

    {"key": "STACK", "name": "Stack & Monotonic Stack", "chapter": "Stack",
     "level": 1, "description": "LIFO, matching/parentheses problems, monotonic stack for next-greater-element",
     "mnemonic": "A stack of plates -- the last one placed on top is the first one taken off (LIFO).",
     "comic_script": [
         {"speaker": "mira", "text": "What's special about a stack versus a regular list?"},
         {"speaker": "dev", "text": "Picture a stack of plates in a cafeteria -- you can only take the TOP plate, and only add a new plate to the top. Never the middle."},
         {"speaker": "mira", "text": "How does that help with checking balanced parentheses?"},
         {"speaker": "dev", "text": "Push every opening bracket. On a closing bracket, pop and check it matches. If it doesn't match, or the stack's empty -- invalid."},
         {"speaker": "mira", "text": "What's a 'monotonic stack'? That name sounds intimidating."},
         {"speaker": "dev", "text": "Just a stack that stays sorted as you go -- before pushing a new item, you pop anything that would break the order. Great for 'find the next bigger thing' style problems."},
         {"speaker": "mira", "text": "When would I use a QUEUE instead of a stack?"},
         {"speaker": "dev", "text": "The moment you need 'oldest thing first' instead of 'most recent thing first' -- that's a completely different order, worth a completely different structure."},
     ],
     "concept_markdown": """# Stack

## What is it?
A stack supports two O(1) operations: push (add to the top) and pop (remove from the top) -- last-in-first-out (LIFO). It's the natural fit for "most recent unmatched thing" problems.

## How it works
For matching brackets: push every opening bracket. On a closing bracket, pop the stack and check it matches -- if it doesn't match (or the stack is empty), the string is invalid. A **monotonic stack** keeps elements in increasing or decreasing order by popping anything that violates the order before pushing a new element -- used for "next greater element" style problems.

## Real-world analogy
A stack of plates in a cafeteria: you can only take the top plate, and you can only add a new plate to the top -- never the middle or bottom directly.

## Worked example
Monotonic stack for "days until warmer temperature," `temps = [73,74,75,71,69,72,76,73]`: walk left to right keeping a stack of *indices* with decreasing temperatures. When today's temp beats the stack's top index's temp, pop it and record `today_index - popped_index` as its answer. This produces `[1,1,4,2,1,1,0,0]` in a single O(n) pass, instead of O(n^2) checking every future day for every day.

## Common mistakes
- Forgetting to check `if not stack` before popping/peeking -- popping an empty stack crashes.
- Using a stack when the problem actually needs FIFO order (a queue) -- if you need "oldest unprocessed item," that's a queue, not a stack.

## When to use it / when not to
Use a stack for nested/matching structures (parentheses, function call order, undo history) or when you need, for every element, "the next element that breaks some ordering" (monotonic stack). Don't use it when you need to process items in the order they arrived -- that's a queue.

## Interview-style question
"Validate balanced parentheses" and "next greater element" are the two canonical stack interview questions -- explaining *why* a stack (not a queue or array) is the right tool for each shows you've understood the pattern, not just memorized the code.

## Key takeaway
"Most recently added, first to be resolved" is the stack's signature -- parentheses matching and monotonic next-greater/smaller problems are its two biggest use cases."""},

    {"key": "RECURSION", "name": "Recursion", "chapter": "Recursion",
     "level": 1, "description": "base case, recursive case, call stack, recursion tree",
     "mnemonic": "Russian nesting dolls -- each doll contains a smaller version of itself, down to the smallest (base case).",
     "comic_script": [
         {"speaker": "mira", "text": "Recursion makes my head spin -- a function calling ITSELF?"},
         {"speaker": "dev", "text": "Russian nesting dolls! Each doll contains a smaller version of itself, until you reach the smallest solid one that doesn't open anymore."},
         {"speaker": "mira", "text": "That smallest doll is the 'base case'?"},
         {"speaker": "dev", "text": "Exactly -- the point where the function stops calling itself and just answers directly, without recursing further."},
         {"speaker": "mira", "text": "What happens if I forget the base case?"},
         {"speaker": "dev", "text": "The dolls never stop opening -- infinite recursion, until your program crashes from running out of stack space."},
         {"speaker": "mira", "text": "Is there always a non-recursive way to write the same thing?"},
         {"speaker": "dev", "text": "Usually yes, with an explicit stack replacing the implicit one recursion uses automatically -- being able to translate between the two shows you understand recursion as a MECHANISM, not magic."},
     ],
     "concept_markdown": """# Recursion

## What is it?
A recursive function solves a problem by calling itself on a smaller version of the same problem, until a **base case** is reached that can be answered directly, without further recursion.

## How it works
Every recursive function needs two parts: a base case (stops the recursion) and a recursive case (does a little work, then calls itself on a strictly smaller input, making progress toward the base case). The computer tracks each in-progress call on a **call stack** -- itself a stack (see the Stack lesson) -- which is why very deep recursion can overflow it.

## Real-world analogy
Russian nesting dolls (matryoshka): each doll contains a smaller doll, until you reach the smallest solid doll (the base case) that doesn't open further.

## Worked example
`factorial(4)`:
```
factorial(4) = 4 * factorial(3)
             = 4 * (3 * factorial(2))
             = 4 * (3 * (2 * factorial(1)))
             = 4 * (3 * (2 * 1))      <- base case: factorial(1) = 1
             = 24
```
The calls "stack up" waiting for the innermost one to resolve first, then unwind back out, multiplying as they return.

## Common mistakes
- Forgetting the base case entirely, or writing one that's never reached -- causes infinite recursion until a stack overflow crash.
- Not making progress toward the base case (e.g. calling `f(n)` again instead of `f(n-1)`).
- Recomputing the same subproblem many times (plain recursive Fibonacci is the classic example) -- the fix is memoization, covered in Dynamic Programming.

## When to use it / when not to
Use recursion when a problem naturally breaks into "solve a smaller version of the same problem, then combine" -- trees, backtracking, and divide-and-conquer are built on this. Avoid deep unbounded recursion (thousands of levels) in languages/runtimes with small default stack limits -- an iterative approach with an explicit stack may be safer.

## Interview-style question
"Can you rewrite this recursive solution iteratively?" tests whether you understand recursion as a mechanism (an implicit stack), not magic -- translating between the two is a strong signal of real understanding.

## Key takeaway
Identify the base case first, then ask "how does this problem reduce to a smaller version of itself?" -- that reduction step is the entire recursive case."""},

    {"key": "DP_BASICS", "name": "Dynamic Programming Foundations", "chapter": "Dynamic Programming",
     "level": 2, "description": "repeated subproblems, memoization, tabulation, 1D DP",
     "mnemonic": "Sticky notes for answers you've already worked out, so you never re-solve the same subproblem twice.",
     "comic_script": [
         {"speaker": "mira", "text": "DP always felt like magic to me. What's actually going on?"},
         {"speaker": "dev", "text": "Sticky notes on a desk! First time you work out 'ways to climb 5 stairs,' you write the answer on a note. Next time you need it, you read the note instead of recalculating."},
         {"speaker": "mira", "text": "So it's just... caching answers?"},
         {"speaker": "dev", "text": "That's genuinely the whole trick -- when plain recursion recomputes the SAME subproblem over and over, DP saves each answer once so it's never redone."},
         {"speaker": "mira", "text": "How do I even start a DP problem without freezing up?"},
         {"speaker": "dev", "text": "Say out loud, in words, four things: what's the STATE, how do smaller states build the TRANSITION, what's the BASE case, and what's the final ANSWER. Code comes after, not before."},
         {"speaker": "mira", "text": "That sounds a lot less scary than 'DP' sounds."},
         {"speaker": "dev", "text": "It really is memoized recursion -- nothing more mystical than that."},
     ],
     "concept_markdown": """# Dynamic Programming Foundations

## What is it?
Dynamic programming (DP) applies when a recursive solution recomputes the same subproblems many times -- DP caches (memoizes) those answers so each subproblem is solved exactly once.

## How it works
Every DP problem should explicitly identify four things: **State** (what varies between subproblems, e.g. "the current step number"), **Transition** (how a state's answer is built from smaller states' answers), **Base case** (the smallest states, answered directly), and the final **Answer** (usually the largest state, or an aggregate over several). Implement it top-down (recursion + a cache, called memoization) or bottom-up (an explicit loop filling a table, called tabulation).

## Real-world analogy
Sticky notes on a desk: the first time you work out "ways to climb 5 stairs," you write the answer on a sticky note. Next time you need it as part of a bigger question, you read the note instead of recalculating from scratch.

## Worked example
Climbing stairs, `n=4`, 1 or 2 steps at a time. State: `ways(i)` = ways to reach step i. Transition: `ways(i) = ways(i-1) + ways(i-2)` (you arrive at step i either from i-1 or i-2). Base cases: `ways(1)=1, ways(2)=2`.

| i | ways(i) |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 1+2=3 |
| 4 | 2+3=5 |

Answer: 5.

## Common mistakes
- Jumping straight to code without first writing State/Transition/Base case in words -- the #1 cause of "I don't know where to start" on DP problems.
- Off-by-one errors in the base cases, which then silently corrupt every state built on top of them.
- Using O(n) space for the full DP table when only the last one or two states are ever needed (an easy space optimization, missed).

## When to use it / when not to
Use DP when a recursive solution shows overlapping subproblems (the same inputs recurring) *and* optimal substructure (the best overall answer is built from best answers to subproblems). If subproblems don't overlap, plain recursion or divide-and-conquer is enough and DP adds needless complexity.

## Interview-style question
"What's the state and transition here?" is what a good interviewer listens for -- verbalizing State/Transition/Base case *before* coding is often worth more than the code itself in a DP interview.

## Key takeaway
DP is memoized recursion, nothing more mystical -- always state the four parts (State, Transition, Base case, Answer) out loud before writing a single line of code."""},

    {"key": "HEAP", "name": "Heap / Priority Queue", "chapter": "Heap",
     "level": 2, "description": "min/max heap, top-K problems, frequency-based ranking",
     "mnemonic": "A hospital ER -- not first-come-first-served, always treats the most urgent case first.",
     "comic_script": [
         {"speaker": "mira", "text": "What makes a heap different from just sorting a list?"},
         {"speaker": "dev", "text": "A hospital emergency room! Patients aren't seen in arrival order -- the most critical case is always treated next, no matter when they walked in."},
         {"speaker": "mira", "text": "So a heap always keeps the 'most urgent' thing instantly accessible?"},
         {"speaker": "dev", "text": "Right -- O(1) to peek at it, and O(log n) to add or remove. Way cheaper than fully re-sorting everything each time something changes."},
         {"speaker": "mira", "text": "When would I use this over just sorting once?"},
         {"speaker": "dev", "text": "'Top K' problems -- like the K largest elements. A size-K heap does that in O(n log k), way better than a full O(n log n) sort when K is small."},
         {"speaker": "mira", "text": "Any common gotcha?"},
         {"speaker": "dev", "text": "Most languages' built-in heap is a MIN-heap by default -- if you need a max-heap, you usually simulate it by negating the values."},
     ],
     "concept_markdown": """# Heap / Priority Queue

## What is it?
A heap (priority queue) keeps the smallest (min-heap) or largest (max-heap) element accessible in O(1), with O(log n) insertion and removal -- the go-to tool whenever you repeatedly need "the current best" from a changing set.

## How it works
Internally, a heap is a binary tree stored in an array, maintaining the invariant that every parent is smaller (min-heap) or larger (max-heap) than its children -- so the root is always the extreme value. Adding or removing an element only needs to fix the tree along one path (O(log n)), rather than re-sorting everything.

## Real-world analogy
A hospital emergency room: patients aren't seen in arrival order (that would be a queue) -- the most critical case is always treated next, and new arrivals slot in by urgency, not by when they walked in.

## Worked example
"Kth largest element," `nums = [3,2,1,5,6,4], k=2`: keep a min-heap of size k. Push the first k elements `{3,2}` (min=2). For each remaining element, if it's bigger than the heap's minimum, swap it in: 1 (skip), 5 (swap in, pop 2, heap={3,5}, min=3), 6 (swap in, pop 3, heap={5,6}, min=5), 4 (skip). Final heap `{5,6}`, minimum (the answer) = 5 -- the 2nd largest element.

## Common mistakes
- Reaching for a full sort (O(n log n)) when only the top-k elements are needed -- a size-k heap does it in O(n log k), better when k is small.
- Forgetting that most languages' built-in heap (e.g. Python's `heapq`) is a *min*-heap by default -- simulate a max-heap by negating values if needed.

## When to use it / when not to
Use a heap for "top-K," "K smallest/largest," "merge K sorted things," or any situation needing repeated access to "the current best" from a changing set. Don't use it if you need access to elements by arbitrary rank (not just the extreme) -- a sorted structure fits better there.

## Interview-style question
"Find the K most frequent/largest elements without fully sorting" is the standard heap prompt -- listen for "top K" or "Kth" in a problem statement as your cue.

## Key takeaway
Whenever a problem repeatedly asks "what's currently the best/worst," a heap keeps that answer at O(1) access while staying cheap to update."""},

    {"key": "STRINGS", "name": "Strings", "chapter": "Strings",
     "level": 1, "description": "character traversal, frequency counting, palindromes, anagrams, string building",
     "mnemonic": "A string is just an array of characters wearing a costume -- most array techniques transfer directly.",
     "comic_script": [
         {"speaker": "mira", "text": "Do I need a whole new bag of tricks for string problems?"},
         {"speaker": "dev", "text": "Barely! A string is just an array of characters wearing a costume -- two pointers, sliding window, hashing all transfer over directly."},
         {"speaker": "mira", "text": "Then why does everyone warn about string concatenation being slow?"},
         {"speaker": "dev", "text": "Because strings are usually IMMUTABLE -- like re-copying an entire letter by hand every time you add one more sentence, instead of writing on separate scraps and stapling them at the end."},
         {"speaker": "mira", "text": "So `s += c` in a loop is secretly expensive?"},
         {"speaker": "dev", "text": "Very -- a loop of n appends can silently become O(n^2). Collect pieces in a list and join them once at the end instead."},
         {"speaker": "mira", "text": "Any tip for approaching a new string problem?"},
         {"speaker": "dev", "text": "Ask: 'would this be a normal array problem if these were just numbers?' The answer's almost always yes -- map it back to the technique it actually is."},
     ],
     "concept_markdown": """# Strings

## What is it?
A string is a sequence of characters -- so nearly every array technique you already know (traversal, two pointers, sliding window, hashing) applies to strings directly, with a few string-specific wrinkles layered on top.

## How it works
The biggest wrinkle: strings are usually **immutable** in most languages, so `s += c` inside a loop silently becomes O(n) *per append* (a new string is allocated each time), making a loop of n appends O(n^2) overall. The fix: collect pieces in a list and join them once (`''.join(pieces)`) at the end -- O(n) total. Palindrome checks use two pointers from both ends, moving inward. Anagram checks either sort both strings and compare (O(n log n)) or compare character-frequency counts (O(n), faster).

## Real-world analogy
Building a string with repeated concatenation is like re-copying an entire letter by hand every time you add one more sentence, instead of writing sentences on separate scraps of paper and stapling them together once at the end.

## Worked example
Checking `"race a car"` for palindrome-ness, ignoring spaces and case: filter to `"raceacar"`, then compare with two pointers from both ends: `r` vs `r` (match), `a` vs `a` (match), `c` vs `c` (match), `e` vs `a` -- mismatch, not a palindrome. It stops as soon as a mismatch is found.

## Common mistakes
- Building strings with `+=` inside a loop over many iterations -- silently quadratic.
- Forgetting to normalize case and strip non-alphanumeric characters before a "does this ignore punctuation/case" comparison.
- Assuming `sorted(word)` and frequency-count comparisons are interchangeable in performance -- sorting is O(n log n), a frequency map is O(n).

## When to use it / when not to
Treat a string problem as an array problem first -- ask "would this be a traversal/two-pointer/sliding-window/hashing problem if these were just numbers?" The answer is almost always yes. Reach for specialized string structures (like a Trie) only when you need fast *prefix* queries across many strings at once.

## Interview-style question
"Check if two strings are anagrams" and "check if a string is a palindrome, ignoring punctuation" are the two most common warm-up string questions -- both are really array techniques wearing a string costume.

## Key takeaway
Don't learn "string algorithms" as a separate category -- map every string problem back to the array technique it actually is, and watch for the immutable-concatenation trap."""},

    {"key": "LINKED_LIST", "name": "Linked List", "chapter": "Linked List",
     "level": 1, "description": "node traversal, reversal, fast/slow pointers, cycle detection, merging",
     "mnemonic": "A treasure hunt -- each clue (node) only tells you where to find the next clue.",
     "comic_script": [
         {"speaker": "mira", "text": "Why would anyone use a linked list instead of a regular array?"},
         {"speaker": "dev", "text": "A treasure hunt where each clue only tells you the LOCATION of the next clue -- you can't skip to clue 5 without visiting 1 through 4."},
         {"speaker": "mira", "text": "That sounds worse than an array in every way!"},
         {"speaker": "dev", "text": "Except one huge thing -- inserting a brand-new clue between two existing ones just means rewriting two 'next location' notes, no shifting a whole array of elements."},
         {"speaker": "mira", "text": "What's the trickiest part of reversing a linked list?"},
         {"speaker": "dev", "text": "You need THREE pointers in flight -- previous, current, and next -- saved BEFORE you overwrite current's pointer, or you'll permanently lose the rest of the list."},
         {"speaker": "mira", "text": "When would I actually prefer an array?"},
         {"speaker": "dev", "text": "Whenever you need random access by index, or cache-friendliness matters -- arrays sit together in memory, linked lists are scattered all over the place."},
     ],
     "concept_markdown": """# Linked List

## What is it?
A linked list is a sequence of nodes, where each node holds a value and a pointer (`.next`) to the following node -- unlike an array, there's no random access; to reach node i, you must walk from the head one step at a time.

## How it works
That's the whole trade-off versus an array: O(1) insertion/deletion at a known position (just re-point a couple of `.next` links, no shifting elements), but O(n) access to an arbitrary position. **Reversal** walks forward while re-pointing each node's `.next` backward, needing three pointers in flight: `prev`, `curr`, and a saved `next` (saved *before* overwriting `curr.next`, or you'd lose the rest of the list). **Fast/slow pointers** (Floyd's algorithm): a slow pointer advances one step, a fast pointer advances two -- if there's a cycle, they eventually meet inside it; if the fast pointer reaches the end (`None`) first, there's no cycle. The same trick finds a list's middle node in one pass.

## Real-world analogy
A treasure hunt where each clue only tells you the location of the *next* clue -- you can't skip ahead to clue 5 without first visiting clues 1-4, but inserting a brand-new clue between two existing ones just means rewriting two "next location" notes.

## Worked example
Reversing `1 -> 2 -> 3`:

| step | prev | curr | next (saved) | list so far |
|---|---|---|---|---|
| start | None | 1 | - | 1->2->3 |
| 1 | 1 | 2 | 2 | None<-1, 2->3 |
| 2 | 2 | 3 | 3 | None<-1<-2, 3 |
| 3 | 3 | None | - | None<-1<-2<-3 |

Return `prev` (now pointing at 3) as the new head: `3 -> 2 -> 1`.

## Common mistakes
- Overwriting `curr.next` *before* saving it -- permanently loses the rest of the original list.
- Off-by-one errors with a "dummy head" sentinel node -- a common trick to avoid special-casing an empty result list, but easy to forget to return `dummy.next` instead of `dummy` itself.
- Losing the head reference entirely by advancing the *head* pointer itself instead of a separate traversal pointer.

## When to use it / when not to
Use a linked list when insertions/deletions happen frequently at arbitrary positions and you don't need random access by index. Prefer an array when you need O(1) access by index, or when cache-friendliness matters (arrays are contiguous in memory; linked lists are scattered, slower in practice despite equal Big-O in some cases).

## Interview-style question
"Reverse a linked list" and "detect a cycle" are two of the most-asked linked list questions specifically because they test whether you can manage multiple pointers correctly without losing references -- easy to fumble under interview pressure.

## Key takeaway
Linked list problems are really "pointer bookkeeping" problems -- draw the nodes and arrows on paper before writing code, and track exactly which pointer you're overwriting and when."""},

    {"key": "QUEUE_DEQUE", "name": "Queue / Deque", "chapter": "Queue / Deque",
     "level": 1, "description": "FIFO, circular queue, double-ended queue, BFS foundation, sliding window maximum",
     "mnemonic": "A line at a ticket counter (FIFO) -- a deque is a line you're also allowed to jump into from the front.",
     "comic_script": [
         {"speaker": "mira", "text": "What's the actual difference between a stack and a queue?"},
         {"speaker": "dev", "text": "A queue's a ticket-counter line -- first in line, first served (FIFO). A stack's the opposite -- last one in is first served."},
         {"speaker": "mira", "text": "Why does BFS specifically need a queue and not a stack?"},
         {"speaker": "dev", "text": "Because BFS must explore nodes in the order it discovered them -- level by level. Use a stack by accident, and you silently get DFS order instead -- wrong answer for 'shortest path' questions, no error thrown."},
         {"speaker": "mira", "text": "And a deque -- that's just a fancier queue?"},
         {"speaker": "dev", "text": "A boarding line that also lets priority passengers cut in at the front -- push or pop from EITHER end, O(1) each."},
         {"speaker": "mira", "text": "When would I actually need both ends?"},
         {"speaker": "dev", "text": "Sliding window maximum -- you evict old, useless values from the front while adding new candidates at the back, all in one structure."},
     ],
     "concept_markdown": """# Queue / Deque

## What is it?
A queue is first-in-first-out (FIFO): the earliest-added element is the first removed. A deque (double-ended queue) generalizes this, allowing O(1) push/pop from *both* ends.

## How it works
A queue is the foundation of breadth-first search: you must explore discovered nodes in the order you discovered them (level by level), which is FIFO order -- using a stack instead gives depth-first order, the wrong sequence for "shortest path" questions. A monotonic deque (used for sliding window maximum) keeps element *indices* in decreasing order of value: before adding a new index, pop from the back any indices whose values are now known to be smaller (they can never be the answer again while the new, larger value is in the window); pop from the front any index that has fallen outside the current window.

## Real-world analogy
A queue is a ticket-counter line: first in line, first served. A deque is more like a boarding line that also lets priority passengers cut in at the front -- add or remove from either end.

## Worked example
Sliding window maximum, `nums=[1,3,-1,-3,5], k=3`. Maintain a deque of indices with decreasing values:
- i=0 (val 1): deque=[0]
- i=1 (val 3): 3>nums[0]=1, pop 0; deque=[1]
- i=2 (val -1): append; deque=[1,2]. Window full: max = nums[1] = 3
- i=3 (val -3): append; deque=[1,2,3]. max = nums[1] = 3
- i=4 (val 5): 5 beats everything in deque, pop all, deque=[4]; max = 5

## Common mistakes
- Using a stack (LIFO) where FIFO order is actually required -- BFS with a stack silently becomes DFS, giving wrong "shortest path" answers without erroring.
- Forgetting to evict indices that have fallen outside the current window from the *front* of a monotonic deque.

## When to use it / when not to
Use a queue whenever "process things in the order they were discovered" matters -- BFS is the headline use case. Use a deque specifically when you need efficient operations at *both* ends, like the monotonic-deque sliding-window-maximum pattern. Neither applies if order doesn't matter, or if you specifically need last-in-first-out behavior (that's a stack).

## Interview-style question
"Find the shortest path in an unweighted graph" should immediately make you think "BFS with a queue," not DFS -- interviewers use this to check you know *why* BFS guarantees shortest paths and DFS doesn't.

## Key takeaway
FIFO order is the queue's signature, and it's precisely why BFS (not DFS) finds shortest paths in unweighted graphs -- a deque is the same idea, generalized to both ends."""},

    {"key": "TREES", "name": "Binary Trees", "chapter": "Trees",
     "level": 2, "description": "tree terminology, DFS/BFS traversal orders, height, diameter, lowest common ancestor",
     "mnemonic": "A family tree -- one root ancestor, branching down into children.",
     "comic_script": [
         {"speaker": "mira", "text": "Why do so many tree problems get solved with recursion?"},
         {"speaker": "dev", "text": "Because a tree IS naturally recursive -- a family tree, one root ancestor branching into children and grandchildren. Most questions get answered by looking at children's answers first."},
         {"speaker": "mira", "text": "What's the difference between preorder, inorder, and postorder? I always mix them up."},
         {"speaker": "dev", "text": "Preorder (root first) is for copying a tree. Inorder (left, root, right) visits a search tree in sorted order. Postorder (children before parent) fits when a node's answer NEEDS its children's answers first -- like computing height."},
         {"speaker": "mira", "text": "So for height, I'd use postorder?"},
         {"speaker": "dev", "text": "Right -- you can't know a node's height until you know both its children's heights."},
         {"speaker": "mira", "text": "Any tip for writing tree recursion without getting lost?"},
         {"speaker": "dev", "text": "Write the base case first -- 'if node is None, return X' -- then ask 'how do I COMBINE the left and right subtree's answers at this node?' That combining step is basically the whole problem."},
     ],
     "concept_markdown": """# Binary Trees

## What is it?
A tree is a graph with no cycles and exactly one path between any two nodes -- most commonly a *binary* tree, where each node has at most two children (left and right).

## How it works
Traversal order matters, and each has a specific use: **preorder** (root, left, right) is natural for copying/serializing a tree. **Inorder** (left, root, right) visits a *binary search tree* in sorted order. **Postorder** (left, right, root) processes children before their parent -- natural when a node's answer depends on its children's answers, like computing height. **Level order** (BFS with a queue) visits row by row. Most tree problems are naturally recursive: solve the left subtree, solve the right subtree, combine the two results at the current node.

## Real-world analogy
A family tree: one root ancestor at the top, branching down into children and grandchildren -- and just like a family tree, most questions ("how many generations below them?") are naturally answered by looking at children's answers first.

## Worked example
Max depth of `[3,9,20,null,null,15,7]` (node 3 has children 9 and 20; 20 has children 15 and 7): `max_depth(3) = 1 + max(max_depth(9), max_depth(20))`. `max_depth(9) = 1` (leaf). `max_depth(20) = 1 + max(1,1) = 2`. So `max_depth(3) = 1 + max(1, 2) = 3`.

## Common mistakes
- Off-by-one in depth/height definitions -- is an empty tree depth 0 or -1? Pin down the convention the problem uses before coding.
- Forgetting the base case `if node is None: return <base value>` -- every recursive tree function needs one.
- Confusing "balanced" (subtree heights differ by at most 1, everywhere) with "complete" (every level full except possibly the last, filled left-to-right) -- different properties.

## When to use it / when not to
Recognize a tree problem by hierarchical, branching structure with no cycles. If nodes can have multiple parents, or cycles are possible, you're looking at a general graph instead (see the Graphs lesson) -- tree algorithms assume the acyclic, single-parent structure.

## Interview-style question
"Find the maximum depth" and "invert a binary tree" are classic warm-ups because a clean recursive solution is short but requires correctly identifying the base case and combining step.

## Key takeaway
Nearly every tree problem is "solve the subtrees, then combine at the current node" -- write that combining step in words before writing any code."""},

    {"key": "BST", "name": "Binary Search Trees", "chapter": "Binary Search Trees",
     "level": 2, "description": "BST property, search/insert/delete, validation, successor/predecessor",
     "mnemonic": "A BST is a family tree that's alphabetized -- left is always 'smaller', right is always 'bigger'.",
     "comic_script": [
         {"speaker": "mira", "text": "What makes a BST different from a regular binary tree?"},
         {"speaker": "dev", "text": "It's alphabetized! Every descendant to the left of any person has a 'smaller' value, every descendant to the right has a 'bigger' one -- at EVERY node, not just the root."},
         {"speaker": "mira", "text": "Why does 'at every node' matter so much?"},
         {"speaker": "dev", "text": "Because the classic mistake is only checking a node against its immediate parent -- but a node deep in the left subtree must be smaller than EVERY ancestor above it, not just the one right next to it."},
         {"speaker": "mira", "text": "How do you actually validate that correctly?"},
         {"speaker": "dev", "text": "Pass down a valid (low, high) range as you descend, narrowing it at each step -- that catches violations a purely local check would miss."},
         {"speaker": "mira", "text": "Does a BST ALWAYS give fast search?"},
         {"speaker": "dev", "text": "Only if it's balanced! Insert already-sorted data into a naive BST and it degrades into basically a straight line -- O(n), just like a linked list."},
     ],
     "concept_markdown": """# Binary Search Trees

## What is it?
A binary search tree (BST) is a binary tree with one extra invariant at every node: everything in its left subtree is smaller, everything in its right subtree is larger.

## How it works
That invariant is what makes search, insert, and delete O(log n) on a *balanced* BST: each comparison eliminates an entire half of the remaining nodes -- the same idea as binary search on a sorted array. Inorder traversal (left, root, right) of a BST visits every value in sorted order. **Important subtlety when validating a BST:** checking only `node.left.val < node.val < node.right.val` locally is *not* sufficient -- a node deep in the left subtree must be smaller than *every* ancestor above it, not just its immediate parent. The correct approach passes down a valid `(low, high)` range that narrows as you descend.

## Real-world analogy
A family tree that's also alphabetized: every descendant to the left of any person has a "smaller" name, every descendant to the right has a "bigger" one -- letting you find anyone by repeatedly asking "smaller or bigger?" and discarding half the tree each time.

## Worked example
Searching for 6 in a BST rooted at 8, with left subtree rooted at 3 and right subtree rooted at 10: 6 < 8, go left to 3. 6 > 3, go right into 3's right subtree. Continue until found or you reach an empty spot. Each step eliminates an entire subtree from consideration.

## Common mistakes
- Validating a BST with only a local parent-child check instead of a range check inherited from every ancestor.
- Forgetting that a BST's O(log n) guarantee depends on it being *balanced* -- an unlucky insertion order (e.g. already-sorted data) can degrade a naive BST into a straight line, effectively O(n), like a linked list.

## When to use it / when not to
Use a BST when you need ordered data with efficient insert/delete/search all at once (a plain sorted array has O(n) insert; a BST fixes that while keeping fast search). If you don't need ordering, a hashmap is simpler and offers O(1) average lookups instead of O(log n).

## Interview-style question
"Validate that a binary tree satisfies the BST property" is a classic trap question -- most first attempts get the local-check version wrong, and a good interviewer watches for whether you catch the ancestor-range issue yourself.

## Key takeaway
The BST invariant must hold against *every* ancestor, not just the immediate parent -- and it's precisely what turns tree search into the tree-shaped equivalent of binary search."""},

    {"key": "TRIE", "name": "Trie (Prefix Tree)", "chapter": "Trie",
     "level": 3, "description": "prefix trees, insert/search, autocomplete, word search",
     "mnemonic": "A dictionary where words sharing a prefix share the same branch -- an index of an index.",
     "comic_script": [
         {"speaker": "mira", "text": "How does autocomplete suggest words so fast as I type?"},
         {"speaker": "dev", "text": "A dictionary organized as nested folders by letter -- a 'C' folder contains an 'A' subfolder, which contains an 'R' subfolder marked 'complete word: car.'"},
         {"speaker": "mira", "text": "So 'car' and 'cat' would share the same C-A folders?"},
         {"speaker": "dev", "text": "Exactly -- they only split where they actually differ. Checking 'does any word start with ca' just means walking two folders deep."},
         {"speaker": "mira", "text": "Why not just use a regular hashset of words?"},
         {"speaker": "dev", "text": "A hashset is great for exact matches, but terrible at PREFIX questions -- a trie's whole advantage is answering 'does anything start with this' in time proportional to the prefix length, not the number of words stored."},
         {"speaker": "mira", "text": "What's the one thing people forget when building one?"},
         {"speaker": "dev", "text": "A flag marking 'a complete word ends here' -- without it, you can't tell if 'car' is an actual word or just a prefix of 'card.'"},
     ],
     "concept_markdown": """# Trie (Prefix Tree)

## What is it?
A trie stores strings character by character down a tree, where every node represents "the prefix formed by the path from the root to here."

## How it works
Words sharing a prefix (`car`, `card`, `care`) share the same initial branch, splitting only where they differ. Each node typically stores a fixed-size array or hashmap of children keyed by "next character," plus a boolean flag for "a complete word ends here" (to distinguish `car` being a word from merely being a prefix of `card`). Checking "does any word start with `ca`?" costs O(length of the prefix), regardless of how many words are stored.

## Real-world analogy
A dictionary organized as nested folders by letter: a "C" folder contains an "A" subfolder, which contains an "R" subfolder marked "complete word: car," and inside that a "D" subfolder marked "complete word: card" -- looking up any prefix just means walking the matching chain of folders.

## Worked example
Inserting `"cat"` and `"car"`: both share the path root -> c -> a, then split -- `cat` continues to a `t` node marked "word end," `car` continues to a separate `r` node also marked "word end." Searching for the prefix `"ca"` walks root -> c -> a and confirms the node exists, regardless of whether "ca" is itself a complete word.

## Common mistakes
- Forgetting the "is this a complete word" flag, making it impossible to distinguish a real word from a valid prefix of a longer word.
- Using a trie when a simple hashset would do -- a trie's real advantage is *prefix* queries; for exact-word-only lookups, a hashset is simpler and just as fast.

## When to use it / when not to
Use a trie for autocomplete, prefix search, or spell-check style problems with many prefix queries against a fixed dictionary of words. Skip it for simple "is this exact word present" lookups -- that's what a hashset is for.

## Interview-style question
"Design an autocomplete system" almost always expects a trie -- explaining *why* a trie beats a hashset specifically for prefix queries is the key insight interviewers listen for.

## Key takeaway
A trie is a hashset upgraded for prefix questions -- reach for it the moment a problem asks about *prefixes* of stored strings, not just exact matches."""},

    {"key": "GRAPHS", "name": "Graphs (BFS/DFS)", "chapter": "Graphs",
     "level": 3, "description": "adjacency list/matrix, BFS, DFS, connected components, cycle detection",
     "mnemonic": "A graph is a social network -- people (nodes) and friendships (edges), not necessarily a hierarchy.",
     "comic_script": [
         {"speaker": "mira", "text": "How is a graph different from a tree? They look similar."},
         {"speaker": "dev", "text": "A social network -- people are nodes, friendships are edges. Unlike a family tree, there's no single 'root,' and relationships can form cycles, like mutual friend groups."},
         {"speaker": "mira", "text": "Why do I always need a 'visited' set for graphs?"},
         {"speaker": "dev", "text": "Because that cycle possibility means a traversal without tracking visited nodes can loop forever -- you'd just keep bouncing between the same friends endlessly."},
         {"speaker": "mira", "text": "When do I use BFS versus DFS?"},
         {"speaker": "dev", "text": "BFS for shortest path in an UNWEIGHTED graph -- it guarantees the first time you reach a node is via the shortest route. DFS is for connectivity or cycle detection, where you just need full exploration."},
         {"speaker": "mira", "text": "What if I use DFS for a shortest-path question by mistake?"},
         {"speaker": "dev", "text": "You'll find A path, just not necessarily the SHORTEST one -- a subtle bug, since it still 'works,' just wrong."},
     ],
     "concept_markdown": """# Graphs

## What is it?
A graph generalizes a tree: nodes can have multiple parents, cycles are allowed, and edges can be directed or undirected, weighted or unweighted.

## How it works
Represent a graph as an **adjacency list** (a dict/array mapping each node to its neighbors) for most problems -- O(V+E) space, versus O(V^2) for an adjacency matrix, which wastes space on sparse graphs. **BFS** (queue-based) explores level by level -- use it for shortest path in an *unweighted* graph, since it guarantees the first time you reach a node is via a shortest path. **DFS** (stack-based, often via recursion) explores as deep as possible before backtracking -- use it for connectivity, cycle detection, and topological sort. Always track a `visited` set -- forgetting it turns any traversal into an infinite loop the moment there's a cycle.

## Real-world analogy
A social network: people are nodes, friendships are edges -- unlike a family tree, there's no single "root," relationships can form cycles (mutual friend groups), and there's no implied hierarchy.

## Worked example
Counting connected components in a graph with 5 nodes and edges `[[0,1],[1,2],[3,4]]`: DFS/BFS from node 0 reaches {0,1,2}. The next unvisited node is 3, and DFS/BFS from there reaches {3,4}. Two launches from unvisited nodes = 2 connected components. (Union-Find answers the same question without full traversal, especially efficient when edges arrive one at a time.)

## Common mistakes
- Forgetting a `visited` set entirely -- turns any traversal into an infinite loop the moment a cycle exists.
- Using DFS when BFS is required for a *shortest path* question in an unweighted graph -- DFS finds *a* path, not necessarily the shortest one.
- Building an adjacency matrix for a huge, sparse graph -- wastes enormous memory versus an adjacency list.

## When to use it / when not to
Reach for graph traversal whenever relationships aren't strictly hierarchical -- multiple connections per node, or cycles, are the tell. If the structure is guaranteed acyclic with exactly one parent per node, it's really a tree, and tree-specific techniques may be simpler.

## Interview-style question
"Find the shortest path between two nodes" (unweighted) should immediately trigger BFS, not DFS -- and "how many separate groups/islands/components are there" should trigger repeated BFS/DFS launches or Union-Find.

## Key takeaway
The graph vs. tree distinction is about whether cycles and multiple parents are possible -- and BFS vs. DFS is about whether you need shortest-path guarantees (BFS) or just full exploration/connectivity (either works)."""},

    {"key": "GREEDY", "name": "Greedy Algorithms", "chapter": "Greedy",
     "level": 3, "description": "greedy choice property, interval scheduling, activity selection",
     "mnemonic": "Always grab the best-looking coin right now and hope it adds up -- works only when local best = global best.",
     "comic_script": [
         {"speaker": "mira", "text": "Greedy sounds risky -- just grab whatever looks best right now?"},
         {"speaker": "dev", "text": "Yep, and it's risky if you don't PROVE it works. Making change by always grabbing the biggest coin that fits is a coincidence of how our currency's DESIGNED -- for arbitrary denominations, it can give a wrong answer."},
         {"speaker": "mira", "text": "So how do I know if greedy is actually safe for a given problem?"},
         {"speaker": "dev", "text": "You need to argue the locally-best choice can NEVER be worse than any alternative -- not just notice it passes the example test cases."},
         {"speaker": "mira", "text": "Any classic example where the sort order matters a lot?"},
         {"speaker": "dev", "text": "Interval scheduling -- sort by END time, not start time. Sorting by start can pick a long interval first that blocks out many shorter ones that would've fit."},
         {"speaker": "mira", "text": "What if I can't find a proof and I'm not sure it works?"},
         {"speaker": "dev", "text": "That's usually your sign the problem actually needs DP instead."},
     ],
     "concept_markdown": """# Greedy Algorithms

## What is it?
A greedy algorithm makes the locally-best choice at each step and never reconsiders it, hoping that local optimality adds up to a globally optimal answer.

## How it works
**This only works when the problem has the greedy-choice property** -- you must be able to *argue* why the locally best choice can never be worse than any alternative, not just observe that greedy happens to work on the examples. The classic pattern is interval scheduling: to fit the maximum number of non-overlapping intervals, sort by *end time* and greedily take the next interval that starts at or after the last taken one ends. Sorting by *start* time instead is a common bug -- picking the interval that starts earliest can block out many shorter intervals that would otherwise fit.

## Real-world analogy
Making change with the fewest coins by always grabbing the largest coin that fits: this works for many real currency systems, but is a *coincidence* of how those denominations are designed -- for an arbitrary set of denominations, always-grab-the-largest can give a wrong (non-minimal) answer, which is exactly why the greedy-choice property must be proven, not assumed.

## Worked example
Intervals `[[1,100],[11,22],[1,11],[2,12]]`, max non-overlapping: sort by end time -> `[1,11]`, `[2,12]`, `[11,22]`, `[1,100]`. Take `[1,11]` (count=1, last_end=11). Skip `[2,12]` (starts before 11). Take `[11,22]` (starts at 11 >= 11; count=2, last_end=22). Skip `[1,100]`. Answer: 2. Sorting by *start* time instead would pick `[1,100]` first and block everything else -- answer 1, wrong.

## Common mistakes
- Assuming a greedy approach is correct because it passed the example test cases -- always look for a counterexample or a correctness argument first.
- Sorting by the wrong key (start time instead of end time is the single most common interval-scheduling bug).

## When to use it / when not to
Use greedy when you can prove the greedy-choice property (an "exchange argument" -- showing any optimal solution can be transformed into the greedy one without getting worse -- is the standard proof technique). If you can't construct that argument, or you find a counterexample, the problem likely needs DP instead.

## Interview-style question
"Prove your greedy choice is always safe" is what separates a strong greedy answer from a lucky guess -- interviewers often follow up a correct greedy solution by asking *why* it works.

## Key takeaway
Greedy is fast and simple *when it's provably correct* -- the discipline is proving the greedy-choice property, not just noticing that a greedy idea happens to pass the examples."""},

    {"key": "BACKTRACKING", "name": "Backtracking", "chapter": "Backtracking",
     "level": 3, "description": "decision trees, choice/constraint/undo, subsets, permutations, N-Queens",
     "mnemonic": "Exploring a maze: try a path, hit a dead end, backtrack, try the next path.",
     "comic_script": [
         {"speaker": "mira", "text": "How's backtracking different from regular recursion?"},
         {"speaker": "dev", "text": "Exploring a maze by hand -- try a path, and the moment you hit a dead end, backtrack to the last junction and try the next unexplored direction."},
         {"speaker": "mira", "text": "So it's choose, recurse, then... undo?"},
         {"speaker": "dev", "text": "Exactly the three steps -- make a choice, recurse into its consequences, then UNDO the choice before trying the next alternative. That undo step is what people forget most."},
         {"speaker": "mira", "text": "What happens if I forget to undo?"},
         {"speaker": "dev", "text": "Elements incorrectly linger into later branches that never should've had them -- a really sneaky bug since the code still technically runs."},
         {"speaker": "mira", "text": "How do I avoid exploring the ENTIRE giant tree of possibilities?"},
         {"speaker": "dev", "text": "Pruning -- check the constraint BEFORE recursing deeper, so you skip whole invalid branches instead of fully exploring them and throwing the result away."},
     ],
     "concept_markdown": """# Backtracking

## What is it?
Backtracking is depth-first search over a decision tree of choices: at each step, **make a choice**, **recurse** into its consequences, then **undo the choice** (backtrack) before trying the next alternative.

## How it works
This is exactly how you enumerate subsets (include or exclude each element), permutations (choose which remaining element goes next), and constraint puzzles like N-Queens (place a queen, recurse into the next row; if no placement works, undo and try a different square in the previous row). **Pruning** is what makes backtracking practical: check the constraint *before* recursing deeper (e.g. "does this queen placement conflict with any placed queen?"), so you skip entire invalid subtrees instead of fully exploring them and discarding the result.

## Real-world analogy
Exploring a maze by hand: try a path, and the moment you hit a dead end, backtrack to the last junction and try the next unexplored direction -- you never erase progress you made correctly, only undo the specific wrong turn.

## Worked example
Generating subsets of `[1,2,3]` via include/exclude at each position: start with an empty path. At index 0, branch into "include 1" and "exclude 1." Each branches again into "include/exclude 2," and again for 3 -- a decision tree with 2^3 = 8 leaves, each a complete subset. Recording the current partial path at *every* node of the tree (not just the leaves) gives all 8 subsets, since every partial state is itself a valid subset.

## Common mistakes
- Forgetting to "undo" a choice (e.g. `path.pop()`) after recursing -- causes elements to incorrectly linger in later branches.
- Not pruning early enough -- checking a constraint only at a complete leaf instead of as soon as it can be checked, wasting huge amounts of work on doomed subtrees.
- Sharing the same list across recursive calls without copying it at the point of recording an answer (`result.append(path)` instead of `result.append(path[:])`) -- later mutations then corrupt already-recorded answers.

## When to use it / when not to
Use backtracking to enumerate *all* valid configurations satisfying some constraint (all subsets, all permutations, all valid board placements), when the search space is small enough for exponential exploration (ideally heavily pruned) to be acceptable. If you only need the *count* or *best* configuration, DP might solve it faster without full enumeration.

## Interview-style question
"Generate all subsets/permutations" and "solve N-Queens" are the standard backtracking prompts -- interviewers listen for whether you articulate the choice/recurse/undo structure cleanly, and whether you remember to copy the path before recording it.

## Key takeaway
Backtracking is DFS over choices with an undo step -- the discipline is making a choice, recursing, and always undoing it symmetrically before trying the next option."""},

    {"key": "BIT_MANIPULATION", "name": "Bit Manipulation", "chapter": "Bit Manipulation",
     "level": 2, "description": "binary representation, AND/OR/XOR/shifts, bitmasks, set/unset/toggle bits",
     "mnemonic": "Binary is a row of light switches -- AND/OR/XOR/shift flip and move them.",
     "comic_script": [
         {"speaker": "mira", "text": "Why would XOR-ing a whole array together find the 'unique' number?"},
         {"speaker": "dev", "text": "A row of light switches -- XOR turns a switch on only when two panels DISAGREE. Two panels that agree, then agree again, leave the switch off."},
         {"speaker": "mira", "text": "So if a number appears TWICE, it just cancels itself out?"},
         {"speaker": "dev", "text": "Exactly -- x^x = 0. XOR every value together, and every paired-up number cancels, leaving only the one that appeared an odd number of times."},
         {"speaker": "mira", "text": "When would I actually need a trick like this instead of just a hashmap?"},
         {"speaker": "dev", "text": "Specifically when the constraints demand O(1) EXTRA space -- a hashmap would work fine functionally, bit tricks are for when memory is genuinely the constraint."},
         {"speaker": "mira", "text": "Any gotcha to watch for?"},
         {"speaker": "dev", "text": "Right-shifting NEGATIVE numbers behaves differently across languages -- worth double-checking before relying on it."},
     ],
     "concept_markdown": """# Bit Manipulation

## What is it?
Every integer is stored as a row of binary digits (bits). Bitwise operators manipulate those bits directly, often enabling clever O(1)-per-operation tricks that would otherwise need loops or extra memory.

## How it works
`AND` (`&`) keeps only bits set in *both* operands. `OR` (`|`) keeps bits set in *either*. `XOR` (`^`) keeps bits set in *exactly one* -- useful because `x ^ x = 0` and `x ^ 0 = x`, meaning XOR-ing an entire list together cancels every value appearing an even number of times, leaving only the value appearing an odd number of times. `x << k` multiplies by 2^k; `x >> k` divides by 2^k (for non-negative x). Common idioms: `x & (x - 1)` clears the lowest set bit (counts set bits in O(number of set bits) rather than O(bit-width)); `x & 1` checks if x is odd; `1 << i` creates a mask with only bit i set, letting you test/set/clear/toggle that specific bit in another value.

## Real-world analogy
A row of light switches: AND turns a switch on only if both control panels agree, OR turns it on if either agrees, and XOR turns it on only when the two panels *disagree* -- which is exactly why XOR-ing duplicates cancels them (two panels that agree, then agree again, leave the switch off).

## Worked example
Single Number: `nums = [4,1,2,1,2]`. XOR everything together: `4^1^2^1^2 = 4^(1^1)^(2^2) = 4^0^0 = 4`. Every paired value cancels via `x^x=0`, leaving only the unpaired 4 -- O(n) time, O(1) space, no hashmap needed.

## Common mistakes
- Assuming bit tricks are "necessary" when a simpler hashmap-based solution would do -- reach for bit manipulation specifically when the constraints demand O(1) extra space, not by default.
- Forgetting that right-shift behavior on *negative* numbers is language-dependent (arithmetic vs. logical shift) -- verify this before relying on it.

## When to use it / when not to
Reach for bit tricks when a problem explicitly asks for O(1) extra space on a "find the unique/missing/duplicate element" style question, or when working with sets of booleans compactly (a "bitmask" representing which of up to ~30 items are included/excluded, common in advanced DP). Don't reach for bit tricks by default when a plain hashmap solution is clear and the space constraint doesn't demand otherwise.

## Interview-style question
"Can you solve this in O(1) space instead of O(n)?" on a "find the single/missing number" problem is the standard nudge toward XOR tricks -- explaining *why* `x^x=0` makes this work is what separates understanding from memorization.

## Key takeaway
`x ^ x = 0` and `x ^ 0 = x` are the two facts underlying most XOR tricks -- bit tricks in general are a space-optimization tool to reach for when O(1) extra space is explicitly required."""},

    {"key": "UNION_FIND", "name": "Union-Find (Disjoint Set Union)", "chapter": "Union-Find",
     "level": 3, "description": "disjoint set union, path compression, union by rank, connectivity queries",
     "mnemonic": "Clubs merging together -- once two people share a club, you only ever ask 'which club are you in?'",
     "comic_script": [
         {"speaker": "mira", "text": "Why not just use BFS/DFS every time I need to check if two things are connected?"},
         {"speaker": "dev", "text": "You could -- but if you're asking that question over and over as edges keep arriving, Union-Find answers it in near-O(1) WITHOUT a full traversal each time."},
         {"speaker": "mira", "text": "How does that work?"},
         {"speaker": "dev", "text": "People joining clubs -- once two people are confirmed to share a club, you never re-derive that fact. You just ask 'what's your club's representative?' and compare."},
         {"speaker": "mira", "text": "What are 'path compression' and 'union by rank' actually doing?"},
         {"speaker": "dev", "text": "Keeping the 'clubs' shallow so finding someone's representative stays fast -- skip both, and it can degrade to O(n) per check in the worst case, a long chain."},
         {"speaker": "mira", "text": "When would this NOT be the right tool?"},
         {"speaker": "dev", "text": "If you need the actual PATH between two nodes, not just whether they're connected -- that's BFS/DFS territory instead."},
     ],
     "concept_markdown": """# Union-Find (Disjoint Set Union)

## What is it?
Union-Find (Disjoint Set Union, DSU) tracks a collection of elements partitioned into disjoint groups, supporting two near-O(1) operations: `find(x)` (which group is x in?) and `union(x, y)` (merge x's group and y's group).

## How it works
Each group has a representative (root). `find(x)` follows parent pointers up to the root, with **path compression** (making every visited node point directly to the root) so future lookups are near O(1). `union(x, y)` finds both roots and links one under the other, with **union by rank/size** (attach the smaller tree under the bigger one) to keep trees shallow. Together, these give amortized O(α(n)) per operation -- α is the inverse Ackermann function, effectively constant for any realistic input size.

## Real-world analogy
People joining clubs: once two people are confirmed to be in the same club (union), you never re-derive that fact -- you just ask "what's your club's representative?" (find) and compare.

## Worked example
Edges `[[0,1],[1,2],[3,4]]`, 5 nodes: union(0,1) links their roots. union(1,2) -> find(1)'s root now includes 2, forming group {0,1,2}. union(3,4) forms {3,4}. Two distinct roots remain -> 2 connected components, without ever running a full BFS/DFS traversal.

## Common mistakes
- Forgetting path compression or union by rank -- without both, Union-Find degrades to O(n) per operation in the worst case (a long chain), losing its entire advantage.
- Comparing elements directly instead of comparing their `find()` roots to check "are these connected?"

## When to use it / when not to
Use Union-Find when edges/connections arrive one at a time (or all at once) and you need to repeatedly answer "are these two connected?" or "how many groups exist?" -- especially when you don't need the actual path, just connectivity. If you need the shortest path or full traversal order, use BFS/DFS instead.

## Interview-style question
"Detect if adding an edge creates a cycle in an undirected graph" is a classic Union-Find question -- if two nodes are already in the same set before you union them, the new edge creates a cycle.

## Key takeaway
Union-Find answers "are these connected?" in near-O(1) without ever traversing the graph -- reach for it whenever connectivity, not path detail, is all that's asked."""},

    {"key": "TOPOLOGICAL_SORT", "name": "Topological Sort", "chapter": "Topological Sort",
     "level": 3, "description": "Kahn's algorithm, in-degree, cycle detection in directed graphs, dependency ordering",
     "mnemonic": "Getting dressed: socks before shoes -- a valid order respects every 'must come before' rule at once.",
     "comic_script": [
         {"speaker": "mira", "text": "What does 'topological sort' actually give you?"},
         {"speaker": "dev", "text": "Getting dressed -- socks before shoes, shirt before jacket. It finds AN order that satisfies every 'must come before' rule at once."},
         {"speaker": "mira", "text": "Is there always just one correct order?"},
         {"speaker": "dev", "text": "Nope -- multiple valid orders can exist. Don't over-constrain your check to one exact expected sequence."},
         {"speaker": "mira", "text": "How does Kahn's algorithm actually build that order?"},
         {"speaker": "dev", "text": "Start with everything that has zero prerequisites. Process one, which 'unlocks' its dependents by decrementing their prerequisite count -- once a dependent hits zero, it's ready too."},
         {"speaker": "mira", "text": "What if the order comes out SHORTER than the total node count?"},
         {"speaker": "dev", "text": "That means a cycle exists -- some nodes never became ready, an impossible set of prerequisites, like course A needing course B which needs course A."},
     ],
     "concept_markdown": """# Topological Sort

## What is it?
A topological sort orders the nodes of a **directed acyclic graph (DAG)** so every edge u->v places u before v -- a valid ordering only exists if the graph has no cycle.

## How it works
**Kahn's algorithm** (BFS-based): compute each node's in-degree (incoming-edge count). Start with all in-degree-0 nodes in a queue (no prerequisites). Repeatedly pop a node, add it to the output order, and decrement its neighbors' in-degree -- if a neighbor's in-degree hits 0, it's now ready and gets queued. If the output order ends up shorter than the total node count, a cycle exists (some nodes never became ready) -- this is also how you *detect* a cycle in a directed graph.

## Real-world analogy
Getting dressed: socks before shoes, a shirt before a jacket -- topological sort finds *an* order satisfying every such "before" rule simultaneously (multiple valid orders can exist).

## Worked example
Courses with prerequisites `[[1,0],[2,0],[3,1],[3,2]]` (meaning "to take course X you need Y" as `[X,Y]`): course 0 has no prerequisites (in-degree 0), start there. Taking 0 unlocks 1 and 2 (in-degree drops to 0 for both). Taking 1 and 2 unlocks 3 (its in-degree drops from 2 to 0). Valid order: `[0, 1, 2, 3]`.

## Common mistakes
- Forgetting a topological order isn't unique -- multiple valid orderings can exist; don't over-constrain a check to one exact expected sequence.
- Not detecting cycles -- if you don't check "did every node get processed," a cyclic dependency (an impossible set of prerequisites) silently produces an incomplete, wrong-looking order instead of an explicit error.

## When to use it / when not to
Use it whenever tasks have "must happen before" dependencies and you need one valid execution order -- build systems, course scheduling, package dependency resolution. It doesn't apply to undirected graphs, or directed graphs where cycles are expected/allowed.

## Interview-style question
"Can you finish all courses given these prerequisites?" is the standard framing -- the real question underneath is "does this directed graph have a cycle?", answered for free as a side effect of attempting a topological sort.

## Key takeaway
Topological sort and cycle detection in a directed graph are the same algorithm viewed two ways -- if Kahn's algorithm can't process every node, the leftover nodes are stuck in a cycle."""},

    {"key": "DIJKSTRA", "name": "Dijkstra's Shortest Path", "chapter": "Graphs",
     "level": 4, "description": "single-source shortest paths with non-negative weights, priority-queue-based relaxation",
     "mnemonic": "A GPS always exploring the currently-closest unvisited place next -- never guessing, always provably closest so far.",
     "comic_script": [
         {"speaker": "mira", "text": "Isn't Dijkstra's just BFS but for weighted graphs?"},
         {"speaker": "dev", "text": "That's actually a great way to think about it! A GPS route planner always investigating the currently-NEAREST unvisited intersection next, locking in its shortest distance once reached."},
         {"speaker": "mira", "text": "Why does it need a heap instead of a plain queue like BFS?"},
         {"speaker": "dev", "text": "Because edges have different COSTS now -- a plain queue assumes every step costs the same. The heap always pulls out whichever unvisited node is currently closest, regardless of visit order."},
         {"speaker": "mira", "text": "Why does it specifically require non-negative weights?"},
         {"speaker": "dev", "text": "Once you pop a node, its distance is treated as FINAL. A negative edge could sneak in later and find an even shorter path, breaking that guarantee entirely."},
         {"speaker": "mira", "text": "So what do I use if negative weights ARE possible?"},
         {"speaker": "dev", "text": "Bellman-Ford -- built specifically to handle that case Dijkstra can't."},
     ],
     "concept_markdown": """# Dijkstra's Shortest Path

## What is it?
Dijkstra's algorithm finds the shortest path from a source node to every other node in a graph with **non-negative** edge weights.

## How it works
It's BFS's weighted cousin: instead of a plain queue (correct only when all edges cost the same), Dijkstra uses a **min-heap** keyed by "current known shortest distance," always expanding the closest not-yet-finalized node next. When you pop a node from the heap, its distance is guaranteed final -- true only because all weights are non-negative; a negative edge could still find a shorter path later, breaking the guarantee (which is why Dijkstra requires non-negative weights, and Bellman-Ford exists for graphs that might have negative edges).

## Real-world analogy
A GPS/delivery route planner always investigating the currently-nearest unvisited intersection next, locking in its shortest distance once reached -- a widening ripple of certainty spreading outward from the start.

## Worked example
Edges (0->1, weight 4), (0->2, weight 1), (2->1, weight 1), source 0: start dist={0:0}. Pop 0, relax neighbors: dist[1]=4, dist[2]=1. Pop 2 (dist 1, smallest remaining), relax: dist[1] = min(4, 1+1) = 2. Pop 1 (dist 2, now finalized). Shortest distances: `{0:0, 1:2, 2:1}` -- the path 0->2->1 (cost 2) beat the direct edge 0->1 (cost 4).

## Common mistakes
- Using Dijkstra on a graph with negative edge weights -- silently gives wrong answers instead of erroring; check for negative weights first and use Bellman-Ford if they exist.
- Forgetting to skip a node popped from the heap if a better distance to it was already finalized (a node may be pushed multiple times with different candidate distances).

## When to use it / when not to
Use Dijkstra for single-source shortest paths on a weighted graph with non-negative weights. Use plain BFS instead if all edges have equal weight. Use Bellman-Ford if negative weights are possible, or Floyd-Warshall for all-pairs shortest paths on a small graph.

## Interview-style question
"Find the shortest path in a weighted graph" should trigger "are weights non-negative?" as your first clarifying question -- that answer determines whether Dijkstra applies at all.

## Key takeaway
Dijkstra is BFS with a priority queue instead of a plain queue, correct specifically because non-negative weights guarantee "closest so far" is never later beaten by a detour."""},

    {"key": "DP_KNAPSACK", "name": "Knapsack-Family DP", "chapter": "Dynamic Programming",
     "level": 3, "description": "0/1 knapsack, unbounded knapsack, coin change, subset-sum shaped problems",
     "mnemonic": "Packing a knapsack with a weight limit: take an item whole or leave it -- never fractions (that's the '0/1' rule).",
     "comic_script": [
         {"speaker": "mira", "text": "Why is it called '0/1' knapsack? 0 and 1 of what?"},
         {"speaker": "dev", "text": "Literally packing a knapsack before a hike with a strict weight limit -- for each item, you decide ONCE: pack it whole (1), or leave it behind (0). No 'pack half a tent.'"},
         {"speaker": "mira", "text": "How's that different from 'coin change'?"},
         {"speaker": "dev", "text": "Coin change is the UNBOUNDED version -- each coin type can be reused as many times as you want, unlike an item you can only take once."},
         {"speaker": "mira", "text": "What's the actual state I should track?"},
         {"speaker": "dev", "text": "dp[i][capacity] -- the best value achievable using the first i items with that much capacity left. For each item, either skip it, or take it if it fits, and keep the better option."},
         {"speaker": "mira", "text": "Common way people get this wrong?"},
         {"speaker": "dev", "text": "Looping the capacity dimension in the wrong DIRECTION -- it's what actually enforces 'used once' versus 'used unlimited times,' and flipping it silently gives the wrong variant's answer."},
     ],
     "concept_markdown": """# Knapsack-Family DP

## What is it?
The 0/1 knapsack pattern appears whenever you choose a subset of items under a capacity constraint (weight, budget, count) to maximize or minimize some value -- each item is fully included or fully excluded, never split or repeated.

## How it works
State: `dp[i][c]` = the best value achievable using the first i items with capacity c. Transition: for item i, either skip it (`dp[i-1][c]`) or take it if it fits (`value[i] + dp[i-1][c - weight[i]]`) -- take the better option. Base case: `dp[0][c] = 0`. This generalizes to "coin change" (minimum coins to make an amount, where each coin type can be reused -- the "unbounded" knapsack) and "subset sum" (can some subset hit an exact target?).

## Real-world analogy
Literally packing a knapsack before a hike with a strict weight limit: for each candidate item, you decide once -- pack it whole, or leave it behind. There's no "pack half a tent."

## Worked example
Items (value, weight): (60,10), (100,20), (120,30), capacity 50. Best combination: items 2 and 3 (100+120=220, weight 50, fits exactly) beats item 1+2 (160) or all three (weight 60, over capacity). The DP table considers, for each item and each capacity, whether including that item improves the achievable value.

## Common mistakes
- Iterating the capacity loop in the wrong direction for the *unbounded* variant (coin change: reuse allowed) versus the *0/1* variant (each item once) -- this direction enforces "used once" vs. "used unlimited times," and getting it backward silently gives the wrong variant's answer.
- Forgetting the space optimization: since `dp[i]` only depends on `dp[i-1]`, a 1D rolling array replaces the full 2D table, cutting O(n×capacity) space to O(capacity).

## When to use it / when not to
Recognize this from "maximize/minimize value under a capacity/budget constraint, choosing a subset of items." If items can be split fractionally, a greedy approach (fractional knapsack) is simpler and provably optimal -- DP is specifically needed because the *indivisible* (0/1) version lacks the greedy-choice property.

## Interview-style question
"Given coins of certain denominations, what's the minimum number of coins to make a target amount?" is the most commonly asked knapsack-family question -- interviewers often follow up by asking whether a greedy "always use the biggest coin" approach works (it doesn't, for arbitrary denominations).

## Key takeaway
Whenever you see "choose a subset under a capacity constraint," the state is (item index, remaining capacity) -- write that down first, and the transition (include vs. exclude) usually follows immediately."""},

    {"key": "DP_STRING", "name": "String DP (LCS & Edit Distance)", "chapter": "Dynamic Programming",
     "level": 3, "description": "longest common subsequence, edit distance, two-string comparison DP",
     "mnemonic": "Comparing two strings letter by letter, always asking 'do these match right here, or do I edit/skip?'",
     "comic_script": [
         {"speaker": "mira", "text": "What's 'edit distance' -- and why does it need a whole 2D table?"},
         {"speaker": "dev", "text": "Think 'track changes' in a word processor comparing two drafts -- it lines up matching phrases and marks the minimal edits needed to turn one draft into the other. That's edit distance, formalized."},
         {"speaker": "mira", "text": "Why a 2D table specifically?"},
         {"speaker": "dev", "text": "dp[i][j] compares the first i characters of one string against the first j of the other. Match? Carry the diagonal answer forward for free. Mismatch? Try insert, delete, or replace, and take whichever costs least."},
         {"speaker": "mira", "text": "How's LCS -- longest common subsequence -- different from a common SUBSTRING?"},
         {"speaker": "dev", "text": "Subsequence just needs the characters in ORDER, not necessarily touching. Substring must be contiguous. Very different DP transitions for each."},
         {"speaker": "mira", "text": "Any tip for not getting lost in the indices?"},
         {"speaker": "dev", "text": "Draw the 2D grid by hand once on paper -- the recurrence becomes visual instead of abstract, and the off-by-one traps get a lot easier to spot."},
     ],
     "concept_markdown": """# String DP (LCS & Edit Distance)

## What is it?
String DP problems (Longest Common Subsequence, Edit Distance, and relatives) compare two strings position by position, building a 2D table where `dp[i][j]` represents the answer using the first i characters of one string and the first j of the other.

## How it works
For **Longest Common Subsequence (LCS)**: if `s1[i-1] == s2[j-1]`, that character extends a shared subsequence: `dp[i][j] = 1 + dp[i-1][j-1]`. Otherwise, take the best of skipping a character from either string: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`. For **Edit Distance** (minimum insert/delete/replace operations to turn one string into another): matching characters cost nothing (`dp[i][j] = dp[i-1][j-1]`); on a mismatch, take the best of insert/delete/replace, each costing 1 plus a smaller subproblem: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.

## Real-world analogy
"Track changes" in a word processor comparing two drafts: it lines up matching words/phrases and marks the minimal insertions/deletions/replacements needed to turn one draft into the other -- exactly what edit distance computes formally.

## Worked example
LCS of `"abcde"` and `"ace"`: `a==a` matches (length 1). `b` vs `c` mismatch, carry forward the best. `c==c` matches, extending to length 2. `d` vs `e` mismatch. `e==e` matches, extending to length 3. LCS length = 3 (the subsequence `"ace"`).

## Common mistakes
- Confusing "subsequence" (characters in order, not necessarily contiguous) with "substring" (must be contiguous) -- they need entirely different DP transitions.
- Off-by-one errors in the table's index offset -- `dp[i][j]` conventionally represents the first `i`/`j` characters, so the `dp[0][*]`/`dp[*][0]` empty-string base cases are easy to get wrong.

## When to use it / when not to
Recognize this shape whenever a problem compares two sequences and asks for a similarity measure, minimum transformation cost, or shared/aligned structure. If only one string is involved (no comparison between two), you're more likely looking at a different DP shape (like palindrome DP) or a non-DP string technique entirely.

## Interview-style question
"What's the minimum number of edits to turn one word into another?" (edit distance) is frequently asked specifically because the transition requires correctly reasoning about three operations (insert/delete/replace) at once, not just one.

## Key takeaway
Two-string DP problems almost always reduce to "match and extend diagonally, or skip a character from one side" -- draw the 2D grid by hand once, and the recurrence becomes visual instead of abstract."""},

    {"key": "ADVANCED_PATTERNS", "name": "Sweep Line & Difference Arrays", "chapter": "Advanced Patterns",
     "level": 4, "description": "sweep line over interval events, difference arrays for range updates, prefix XOR",
     "mnemonic": "A sweep line is a single vertical line dragged across all events, left to right, reacting to each one in order.",
     "comic_script": [
         {"speaker": "mira", "text": "How do you find the minimum meeting rooms needed without checking every pair of meetings?"},
         {"speaker": "dev", "text": "A sweep line! Like slowly dragging a ruler across a timeline of overlapping calendar events -- at every 'starts' or 'ends' mark, you update your count of currently-active meetings."},
         {"speaker": "mira", "text": "And the busiest moment during that sweep is the answer?"},
         {"speaker": "dev", "text": "Exactly -- the counter's MAXIMUM value during the whole sweep. Turns an O(n^2) pairwise-overlap check into one O(n log n) pass."},
         {"speaker": "mira", "text": "What's a 'difference array' -- is that related?"},
         {"speaker": "dev", "text": "Same event-driven spirit, different job -- for applying '+v to a whole range' many times efficiently. You mark the start and end of each range, then take one final running sum to materialize everything at once."},
         {"speaker": "mira", "text": "What's the most common mistake with either of these?"},
         {"speaker": "dev", "text": "Forgetting to break ties correctly when two events land at the exact same time -- like a meeting ending right as another starts, where the order you process them actually matters."},
     ],
     "concept_markdown": """# Sweep Line & Difference Arrays

## What is it?
A family of techniques sharing one idea: process a set of *events* in sorted order, maintaining a running state that only changes at those event points -- rather than checking every possible moment.

## How it works
**Sweep line**: convert each interval into two events (a "start" and an "end"), sort all events by position, and sweep left to right updating a counter (e.g. "how many meetings are active right now") -- the answer (like "minimum meeting rooms needed") is the counter's maximum value during the sweep. **Difference array**: to apply "+v to every element in range [l, r]" many times efficiently, record `diff[l] += v` and `diff[r+1] -= v`, then take a prefix sum once at the end to materialize all updates in O(n + updates) instead of O(n × updates). **Prefix XOR**: like prefix sum but for XOR -- `prefix_xor[i]` gives the XOR of any range in O(1).

## Real-world analogy
A sweep line is like slowly dragging a ruler across a timeline of overlapping calendar events: at every "meeting starts" or "meeting ends" mark the ruler crosses, you update your count of currently-active meetings, and the busiest moment is your answer.

## Worked example
Meeting Rooms II, intervals `[[0,30],[5,10],[15,20]]`: events sorted by time: (0,start), (5,start), (10,end), (15,start), (20,end), (30,end). Sweep: at 0, active=1 (max=1). At 5, active=2 (max=2). At 10, active=1. At 15, active=2 (max stays 2). At 20, active=1. At 30, active=0. Minimum rooms needed = 2 (the peak simultaneous count).

## Common mistakes
- Sorting events by time but not breaking ties correctly (an "end" event at the same time as a "start" event usually should be processed first, freeing the room before the new meeting needs it) -- wrong tie-breaking silently overcounts.
- Forgetting the difference array's final prefix-sum step -- the diff array alone doesn't hold final values, only the *deltas* between them.

## When to use it / when not to
Reach for sweep line whenever a problem is about overlapping intervals and a running count/state (max overlap, total covered length). Reach for a difference array when many range-update operations need to be applied efficiently before a single final readout. Neither applies if you need the state at *every intermediate point*, not just the final aggregate.

## Interview-style question
"What's the minimum number of meeting rooms required to schedule all these intervals without conflict?" is the canonical sweep-line question -- a common wrong answer tries to greedily pair meetings instead of tracking the simultaneous-overlap count directly.

## Key takeaway
When a problem is fundamentally about intervals overlapping over time, converting each interval into two sorted events turns an O(n^2) pairwise-overlap check into a single O(n log n) sweep."""},
]

# (skill_key, prerequisite_key)
PREREQUISITES = [
    ("ALGORITHMIC_THINKING", "PROGRAMMING_BASICS"),
    ("ARRAYS_TRAVERSAL", "ALGORITHMIC_THINKING"),
    ("ARRAYS_PREFIX_SUM", "ARRAYS_TRAVERSAL"),
    ("HASHING", "ARRAYS_TRAVERSAL"),
    ("TWO_POINTER", "ARRAYS_TRAVERSAL"),
    ("SLIDING_WINDOW", "TWO_POINTER"),
    ("BINARY_SEARCH", "ARRAYS_TRAVERSAL"),
    ("STACK", "ALGORITHMIC_THINKING"),
    ("RECURSION", "ALGORITHMIC_THINKING"),
    ("DP_BASICS", "RECURSION"),
    ("HEAP", "ARRAYS_TRAVERSAL"),
    ("STRINGS", "ARRAYS_TRAVERSAL"),
    ("LINKED_LIST", "ALGORITHMIC_THINKING"),
    ("QUEUE_DEQUE", "ALGORITHMIC_THINKING"),
    ("TREES", "RECURSION"),
    ("BST", "TREES"),
    ("TRIE", "TREES"),
    ("TRIE", "STRINGS"),
    ("GRAPHS", "QUEUE_DEQUE"),
    ("GRAPHS", "RECURSION"),
    ("GREEDY", "ARRAYS_TRAVERSAL"),
    ("BACKTRACKING", "RECURSION"),
    ("BIT_MANIPULATION", "ALGORITHMIC_THINKING"),
    ("UNION_FIND", "ALGORITHMIC_THINKING"),
    ("TOPOLOGICAL_SORT", "GRAPHS"),
    ("DIJKSTRA", "GRAPHS"),
    ("DIJKSTRA", "HEAP"),
    ("DP_KNAPSACK", "DP_BASICS"),
    ("DP_STRING", "DP_BASICS"),
    ("DP_STRING", "STRINGS"),
    ("ADVANCED_PATTERNS", "ARRAYS_PREFIX_SUM"),
    ("ADVANCED_PATTERNS", "HEAP"),
]
