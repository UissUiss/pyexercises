"""Exercise 2.0 — Asking the user

WHAT THE PROGRAM MUST DO
    Ask the user for two pieces of information, then display a sentence that uses both.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which two pieces of information did you choose, and for what purpose?
       Imagine a real form in your future job. Not "name and age" unless you can
       say what you would do with them.

WHAT THE AI CANNOT KNOW
    Your two fields, and the sentence you want at the end. Decide both before you ask.

    One of your two values will almost certainly need to be a number. Find out what
    happens when you try to add 1 to something the user typed, and deal with it.

CHECK IT YOURSELF
    Run your program and answer with an empty line. Then with a space. Then with text
    where you expected a number. Write in a comment what happened each time.
    You are not asked to fix it yet, only to see it.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: my name and age
# 2. Process: my name and age with print("my name is", name) and print("my age is", age), where name = input("enter your name:") and age = input("enter your age:")
# 3. Out: my name is <name>, my age is <age>
# 4. My two fields, and what I would do with them:  just name and age, to know the name and age of the user


# Your code below
name = input("enter your name:")
age = input("enter your age:")
print("my name is", name)
print ("my age is", age)
print("My name is " + name + "and my age is " + age)
