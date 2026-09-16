"""
Real, deterministically-graded quiz questions for the two theory-only skills
that the DSA track's per-skill mastery gate excludes (Algorithmic Thinking &
Complexity has zero seeded coding problems to build practical mastery
against; Programming Foundations is treated the same way since it's
conceptual/foundational rather than pattern-recognition practice). These
questions stand in for mastery specifically for DSA-track tier eligibility --
mastery on these two skills is still tracked and shown as learning progress,
it just isn't part of the "every skill clears the cutoff" gate.
"""

QUIZZES = {
    "ALGORITHMIC_THINKING": [
        {
            "question": "What is the time complexity of binary search on a sorted array of n elements?",
            "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
            "correct_index": 1,
            "explanation": "Binary search halves the search space every step, so the number of steps needed grows as log n.",
        },
        {
            "question": "A function has two separate, non-nested loops, each running n times one after the other. What is its overall time complexity?",
            "options": ["O(n^2)", "O(2n), which simplifies to O(n)", "O(log n)", "O(n!)"],
            "correct_index": 1,
            "explanation": "Sequential (non-nested) loops add: n + n = 2n steps, and constants are dropped in Big-O, giving O(n).",
        },
        {
            "question": "Why is a brute-force nested-loop solution to Two Sum considered O(n^2)?",
            "options": [
                "It uses a hash map internally",
                "For each of the n elements, it scans up to n other elements to find a pair",
                "It sorts the array first",
                "It calls itself recursively n times",
            ],
            "correct_index": 1,
            "explanation": "The outer loop runs n times, and for each of those, the inner loop scans up to n elements -- n * n = n^2 total comparisons.",
        },
        {
            "question": "What does 'space complexity' measure?",
            "options": [
                "How fast an algorithm runs",
                "How much extra memory an algorithm uses, relative to input size",
                "The number of lines of code",
                "The number of test cases needed to verify it",
            ],
            "correct_index": 1,
            "explanation": "Space complexity is about memory growth as input size grows, the same way time complexity is about runtime growth.",
        },
    ],
    "PROGRAMMING_BASICS": [
        {
            "question": "In a loop that runs `for i = 0; i < n; i++`, how many times does the loop body execute?",
            "options": ["n - 1", "n", "n + 1", "It depends on the language"],
            "correct_index": 1,
            "explanation": "i takes the values 0, 1, ..., n-1 -- exactly n values -- before i < n becomes false.",
        },
        {
            "question": "What is the base case in a recursive function for?",
            "options": [
                "To make the function run faster",
                "To stop the recursion so it doesn't run forever",
                "To declare variables",
                "To handle errors only",
            ],
            "correct_index": 1,
            "explanation": "Without a base case that stops the recursive calls, a recursive function would call itself indefinitely (until it crashes).",
        },
        {
            "question": "What's the difference between a function's parameter and a local variable declared inside its body?",
            "options": [
                "There is no difference",
                "A parameter receives a value from the caller; a local variable is created and used only inside the function body",
                "Local variables are always faster to access",
                "Parameters can't be reassigned but local variables can",
            ],
            "correct_index": 1,
            "explanation": "Parameters are the function's inputs, supplied by whoever calls it; local variables exist only for that one call's internal bookkeeping.",
        },
        {
            "question": "In most languages, what happens to a variable declared inside a loop's body on each new iteration?",
            "options": [
                "It keeps its value from the previous iteration",
                "It is freshly created (or reset) each iteration, unless it was declared outside the loop",
                "It automatically becomes a global variable",
                "It causes a compile error",
            ],
            "correct_index": 1,
            "explanation": "A variable scoped inside the loop body is a new binding each iteration -- if you need a value to persist across iterations, it must be declared outside the loop.",
        },
    ],
}
