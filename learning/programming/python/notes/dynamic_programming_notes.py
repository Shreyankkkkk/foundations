#================================================================================================================================================================
#                                                                         Dynamic Programming
#================================================================================================================================================================
'''
Dynamic programming is an algorithmic technique that solves complex problems by breaking them down into simpler subproblems and storing the results 
to avoid redundant calculations. This approach transforms problems that would normally take exponential time into ones that can be solved in polynomial time.

Core Principles:
    Overlapping Subproblems:
        The same smaller problems appear multiple times when solving the larger problem. Instead of recalculating 
        these subproblems repeatedly, we store their solutions.
    Optimal substructures:
        The optimal solution to the problem contains optimal solutions to its subproblems. This means we can build up the best solution 
        by combining the best solutions to smaller parts.

Dynamic Programming Solutios:
    Memoization (Top Down Approach):
        Memoization stores the results of expensive function calls and returns the cached result when the same inputs occur again:

    Tabulation (Bottom Up Approach):
        Tabulation builds the solution from the ground up, filling a table with solutions to subproblems:
    -------------------------------------------------------------------------------------------------------------------------------

    Key advantages of tabulation
        No recursion overhead: Unlike memoization, there's no recursive call stack.
        Predictable execution: We calculate values in a predetermined order (1, 2, 3, 4, 5...).
        Cache-friendly: Sequential array access optimizes memory usage.
        Easy to optimize: Can reduce space complexity to O(1) since we only need the last two values.

    Real-World Applications
        Dynamic programming has widespread applications in computer science and beyond:
        Route Optimization: GPS systems use dynamic programming algorithms to find shortest paths between locations.
        Text Processing: Spell checkers and autocomplete features often rely on dynamic programming to calculate edit distances between words.
        Financial Modeling: Investment strategies and portfolio optimization frequently employ dynamic programming techniques.
        Resource Allocation: The knapsack problem and its variants appear in scheduling, budgeting, and resource management.

When to Use Dynamic Programming
    Dynamic programming is effective when:
        The problem can be broken down into overlapping subproblems.
        The problem exhibits optimal substructure.
        A naive recursive solution would involve repeated calculations.
        You need to optimize for time complexity at the cost of space complexity.
    
    Common dynamic programming patterns include optimization problems (finding minimum/maximum values), 
    counting problems (number of ways to achieve something), and decision problems that can be broken down into smaller decisions.
'''

