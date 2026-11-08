"""Exercise 10.0 — Checking the shape of text (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Validate three pieces of information typed by the user, and only save them when all
    three are acceptable.

ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What are your three fields, and what makes a value acceptable for each? Write the
       rule in plain English before writing any pattern.

WHAT THE AI CANNOT KNOW
    Your three rules. "A valid email" is not a rule, it is a wish. Say what you accept
    and what you reject, and be ready to defend a borderline case.

WHAT TO WATCH
    An assistant will hand you a pattern that looks like line noise. Do not accept it
    until it has explained it to you piece by piece, and you have written that
    explanation in your own words above it.

CHECK IT YOURSELF
    For each field, prepare one value that must pass and two that must fail. Run all
    nine. Any surprise goes in a comment.

DELIVERABLE
    This file, with your comments and your code.
"""

# Your code below

import re
tests = {
    "Campaign name": [
        ("SpringSale_2026", True),
        ("ab", False),
        ("Spring Sale", False)
    ],
    "Campaign ID": [
        ("123456", True),
        ("12345", False),
        ("12A456", False)
    ],
    "Campaign hashtag": [
        ("#Summer2026", True),
        ("Summer2026", False),
        ("#ab", False)
    ]
}

patterns = {
    "Campaign name": r"[A-Za-z0-9_]{3,20}",
    "Campaign ID": r"[0-9]{6}",
    "Campaign hashtag": r"#[A-Za-z0-9]{3,15}"
}

print("TESTING THE NINE VALUES")
print("------------------------")

for field, values in tests.items():
    for value, expected in values:
        result = bool(re.fullmatch(patterns[field], value))
        print(field, "|", value, "|", result)

# ------------------------------------------------
# ASK THE USER FOR INFORMATION
# ------------------------------------------------

print("\nENTER YOUR CAMPAIGN INFORMATION")
print("--------------------------------")

name = input("Campaign name: ")
campaign_id = input("Campaign ID: ")
hashtag = input("Campaign hashtag: ")

# Validate all three fields
valid_name = bool(re.fullmatch(patterns["Campaign name"], name))
valid_id = bool(re.fullmatch(patterns["Campaign ID"], campaign_id))
valid_hashtag = bool(re.fullmatch(patterns["Campaign hashtag"], hashtag))

# Save only if ALL three values are valid
if valid_name and valid_id and valid_hashtag:

    campaign = {
        "name": name,
        "id": campaign_id,
        "hashtag": hashtag
    }

    print("\nAll information is valid!")
    print("Campaign successfully saved:")
    print(campaign)

else:
    print("\nInvalid information!")
    print("Nothing was saved.")

    if not valid_name:
        print("- Campaign name is invalid.")

    if not valid_id:
        print("- Campaign ID is invalid.")

    if not valid_hashtag:
        print("- Campaign hashtag is invalid.")
