#Project Nth Fibonacci Number Calculator
'''
Build an Nth Fibonacci Number Calculator
Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

You should create a function named fibonacci.
You should define a list named sequence within the fibonacci function, and it should be initialized with the values [0, 1].
The fibonacci function should accept one parameter, a non-negative integer n.
Calling fibonacci(n) should use a dynamic programming approach to compute and return the n-th number from the Fibonacci sequence, where each number is the sum of the two preceding numbers.
Each computed Fibonacci number should be appended to the sequence list.
'''

def fibonacci(number):
    if number < 0:
        raise ValueError("Fibonacci number should be non-negative integer")
    
    sequence = [0, 1]
    value_prev, value_current = sequence[0], sequence[1]
    for _ in range(number):
        value_next = value_prev + value_current
        sequence.append(value_next)

        value_prev = value_current
        value_current = value_next
    
    return sequence[number]