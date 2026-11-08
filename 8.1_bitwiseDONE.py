"""Exercise 8.1 — Bitwise operators (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Represent a set of permissions as bits, combine two of them, test whether a third is
    present, then add it and remove one.

ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What are your permissions about? Not files: invent a set from your own field,
       such as who may view, edit and publish a campaign.

WHAT THE AI CANNOT KNOW
    Your permission set and what each one means in your context.

CHECK IT YOURSELF
    Display the value in binary at each step and read the bits yourself.

DELIVERABLE
    This file, with your comments and your code.
"""

# Exercise 8.1 — Bitwise operators (bonus, not graded)

# 1. What goes in?
# Three permissions: VIEW, EDIT and PUBLISH.

# 2. What happens to it? We represent each permission using a different bit.
# We combine permissions, check if one exists,
# add a permission and remove another.

# 3. What comes out?
# The program displays the permissions in binary
# after every operation.

# 4. What are your permissions about?
# My permissions are about managing a social media campaign.
# VIEW = Can see the campaign.
# EDIT = Can modify the campaign.
# PUBLISH = Can publish the campaign.

# Your code below 

# Assign one bit to each permission
VIEW = 1       # 001
EDIT = 2       # 010
PUBLISH = 4    # 100

# Start with VIEW and EDIT permissions
permissions = VIEW | EDIT

print("Initial permissions:", format(permissions, '03b'))

# Check if PUBLISH permission is present
print("Has PUBLISH?", bool(permissions & PUBLISH))

# Add PUBLISH permission
permissions = permissions | PUBLISH
print("After adding PUBLISH:", format(permissions, '03b'))

# Remove EDIT permission
permissions = permissions & ~EDIT
print("After removing EDIT:", format(permissions, '03b'))
