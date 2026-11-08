"""Exercise 9.0 — Surviving what you did not expect

Useful for the final exam: two campaigns in the exam dataset have zero conversions.

WHAT THE PROGRAM MUST DO
    Ask the user for a number, divide something by it, and keep running whatever the
    user types. Never crash.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which two different failures can happen here, and should they produce the same
       message to the user? Decide before coding.

WHAT THE AI CANNOT KNOW
    Your answer to question 4, and how many attempts you allow before giving up.

    An assistant will often propose catching every error at once. Find out why catching
    each failure separately is better, and write the reason in a comment.

CHECK IT YOURSELF
    Run it with: a normal number, then zero, then the word "abc", then an empty line.
    Four runs, four behaviours, all described in a comment. If any of them stopped your
    program, it is not finished.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: a number from the user
# 2. Process: The program attempts to convert the input to a float and divides 100 by that number. If the input is invalid (not a number) or if the user inputs zero, it will catch the exceptions and display appropriate error messages without crashing.
# 3. Out: The program will output the result of the division if the input is valid, or an error message if the input is invalid or zero. It will also inform the user when the maximum number of attempts has been reached.
# 4. The two failures, and whether they deserve the same message: The two failures are ValueError (when the input is not a number) and ZeroDivisionError (when the user inputs zero). They deserve different messages because they represent different types of errors.


# Your code below
# The program allows 4 attempts.
attempts = 0
max_attempts = 4

while attempts < max_attempts:

    user_input = input("Enter a number: ")
    attempts += 1

    try:
        number = float(user_input)

        result = 100 / number

        print("Result:", result)
        break

    except ValueError:
        print("Invalid input! Please enter a valid number.")

    except ZeroDivisionError:
        print("You cannot divide by zero!")

else:
    print("Maximum attempts reached. Goodbye!")
