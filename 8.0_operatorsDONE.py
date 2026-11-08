"""Exercise 8.0 — Operators (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Take two values of your choice and display, as a readable table, the result of every
    comparison between them and of the logical combinations of those results.

 ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it? 
    3. What comes out?
    4. Which two values did you pick, and which comparison result surprised you? 

    
WHAT THE AI CANNOT KNOW
    Your two values. Pick a pair where the answer is not obvious: two strings with
    different capitalisation, a number and the same number written as text, or zero and
    an empty string.

CHECK IT YOURSELF
    Predict each result before running. Count how many you got right.

DELIVERABLE
    This file, with your comments and your code.
"""
# 1. In: and b, two values of your choice
# 2. Process: compare the two values using all comparison operators and logical combinations
# 3. Out: a table showing the results of all comparisons and logical combinations
# 4. My message, and why: I picked 0 and "0" (string), to demonstrate how Python handles comparisons between different data types.



# Your code below
a = 0
b = "0"

# Store all comparison results
comparisons = {
    "a == b (Equal)": a == b,
    "a != b (Not equal)": a != b,
    "a < b (Less than)": "Can't compare a number to a string",
    "a > b (Greater than)": "Can't compare a number to a string",
    "a <= b (Less or equal)": "Can't compare a number to a string",
    "a >= b (Greater or equal)": "Can't compare a number to a string"

}

# Logical combinations
logical = {
    "AND (== and !=)": (a == b) and (a != b),
    "OR (== or !=)": (a == b) or (a != b),
    "NOT (==)": not (a == b)
}

# Display comparison results
print("COMPARISON RESULTS")

for operation, result in comparisons.items():
    print(f"{operation:<28} | {result}")

# Display logical results
print("\nLOGICAL RESULTS")

for operation, result in logical.items():
    print(f"{operation:<28} | {result}")
