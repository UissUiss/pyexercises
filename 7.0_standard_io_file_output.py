"""Exercise 7.0 — Collecting data and saving it

WHAT THE PROGRAM MUST DO
    Ask the user for the information needed to record one entry, then save it to a CSV
    file. Running the program twice must produce two entries, not overwrite the first.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?  (name your file, and list your columns)
    4. Which columns did you choose, and what would you actually do with this file once
       it has two hundred rows in it?

WHAT THE AI CANNOT KNOW
    Your columns. They must be the ones you would really need to collect for a purpose
    you can state. See 7.0_student_data.csv for the shape of a header line, not for
    the columns to use.

    Two behaviours are yours to decide, and an assistant will guess them wrong:
    what happens the very first time, when the file does not exist yet and needs its
    header line, and what happens when a value the user typed is not acceptable.

CHECK IT YOURSELF
    Run your program three times with different values. Then open the file and count
    the lines. You should have three entries and exactly one header line. If you have
    three header lines, or one entry, your program is wrong.

DELIVERABLE
    This file, plus the CSV your program produced.
"""

# 1. In: user input for first name, last name, date of birth, and student ID
# 2. Process:open the CSV file in append mode, write the header line if the file is empty, and write the user input as a new row in the file
# 3. Out, file name and columns:    7.0_student_data.csv with columns: First_name, Last_name, Birth, Student_id
# 4. Which columns and what to do with the file: I chose these columns because they are essential for identifying and keeping track of students. Once the file has two hundred rows, it
# 4. Why these columns, and what this file is for: These columns are necessary for maintaining a comprehensive student database that can be used for enrollment, academic tracking, and communication purposes.


# Your code below
print("please fill in the following details:")
first_name = input("First Name: ")
last_name = input("Last Name: ")
birth = input("Date of Birth (YYYY-MM-DD): ")
student_id = input("Student ID: ")

with open("7.0_student_data.csv", "a") as file:
    file.write("First_name,Last_name,Birth,Student_id\n")
    file.write(first_name + "," + last_name + "," + birth + "," + student_id + "\n")

print("Data saved to 7.0_student_data.csv")