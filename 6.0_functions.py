"""Exercise 6.0 — Naming a piece of work

WHAT THE PROGRAM MUST DO
    Write a function that computes something useful about the list you built in exercise
    4.0, then call it three times with different inputs and display the three results.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?  (what your function receives)
    2. What happens to it?
    3. What comes out?  (what your function returns)
    4. What is your function called, and does its name say what it does without reading
       the code?

WHAT THE AI CANNOT KNOW
    What is worth computing about your data, and what to call it. A function named
    "process" or "do_stuff" fails this exercise even if it works.

    Your function must RETURN its result, not print it. Find out why that difference
    matters and write the reason in a comment. It is the whole point of the exercise.

CHECK IT YOURSELF
    Call your function with an empty list. Note what happens. Then decide whether that
    behaviour is acceptable, and say so in a comment.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: two numbers (a, b)
# 2. Process: add the two numbers
# 3. Out: the sum of the two numbers
# 4. My function name, and why return rather than print: compute_sum; because it allows the caller to decide what to do with the result, rather than being hardcoded to print it

# Your code below
print("hello world")

number_1 = 10
number_2 = 20

Sum = number_1 + number_2
print("The sum of", number_1, "and", number_2, "is", Sum)

number_3 = 100
number_4 = 220

Sum = number_3 + number_4
print("The sum of", number_3, "and", number_4, "is", Sum)

def compute_sum(a, b):
    return a + b


result1 = compute_sum(10, 20)
result2 = compute_sum(100, 220)
print("The sum of 10 and 20 is", result1)
print("The sum of 100 and 220 is", result2)
