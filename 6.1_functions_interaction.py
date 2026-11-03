"""Exercise 6.1 — Small functions working together

WHAT THE PROGRAM MUST DO
    Write three small functions, each doing one thing, and a fourth that uses the other
    three to answer one question about your data.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?  (say which function does what, in order)
    3. What comes out?
    4. What question does your fourth function answer, and why does splitting it into
       three make it easier to check?

WHAT THE AI CANNOT KNOW
    Your question and your split. Ask an assistant for "three functions" and it will
    invent three; they will not be the three your question needs. Decide the split first,
    on paper, then ask.

    One function, one job. If you cannot describe what one of yours does in a single
    sentence without using the word "and", it is doing two things.

CHECK IT YOURSELF
    Test each of the three small functions on its own before combining them. Write in a
    comment the input and expected output you used for each. That is three test cases,
    and they are part of the deliverable.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: numbers
# 2. Process, function by function: def is_even(number): checks if number is even; def is_zero(number): checks if number is zero; def describe(number): uses the two functions above to describe one number
# 3. Out: descriptions of the numbers
# 4. The question my fourth function answers: "What is the nature of this number?" Splitting it into three makes it easier to check because each function has a single responsibility and can be tested independently.


# Your code below
def is_even(number):
    """True when the number divides by two exactly."""
    return number % 2 == 0
from examples.functions.functions_calling_functions import is_zero



def is_zero(number):
    """True when the number is zero."""
    return number == 0

def describe(number):
    """Uses the two functions above to describe one number."""
    if is_zero(number):
        return f"{number} is zero"
    if is_even(number):
        return f"{number} is even"
    return f"{number} is odd"


def is_positive(num):
    return num > 0

def is_negative(num):
    return num < 0

def detailed_message(num):
    if is_zero(num):
        return f"{num} is zero"
    elif is_positive(num):
        return f"{num} is positive"
    elif is_negative(num):
        return f"{num} is negative"
    elif is_even(num):
        return f"{num} is even"
    else:
        return f"{num} is odd"

number = 5
print(detailed_message(-4))


