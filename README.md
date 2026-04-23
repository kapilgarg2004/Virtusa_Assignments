# Virtusa_Assignments
This repository has a set of practice use cases that were done as part of a performance review. The goal is to show that I can solve problems and is good at using a variety of technologies.

# Use Cases Included

# Core Java: The "SafeLog" Password Validator
Business Case: A cybersecurity firm needs a tool for their "Employee Portal" that forces employees to create strong passwords. Standard "if-else" isn't enough; they need a modular approach.

Problem Statement
Build a Password Strength Checker that validates a string against corporate security policies and provides specific feedback on why a password failed.

Student Tasks:
1. The Policy: The password must be:
○ At least 8 characters long.
○ Contain at least one Uppercase letter.
○ Contain at least one Digit (0-9).
2. Looping Logic: Use a for loop to iterate through the string and Character.isUpperCase() / Character.isDigit() to check requirements.
3. Feedback System: Instead of just saying "Invalid," the program should print specifically: "Missing a digit" or "Too short."
4. Retry Mechanism: Use a while loop to keep asking the user for a password until they enter a valid one.

Deliverable: A single PasswordValidator.java file that demonstrates string manipulation and loop control.



# SQL: The "Digital Library" Audit
Business Case: A local community college has a database of books and student borrows. They are struggling to track "Overdue" books and want to know which categories of books are most popular to decide what to buy next.

Problem Statement
Create a relational system to track book loans and generate a "Penalty Report" for books not returned within 14 days.

Student Tasks:
1. Table Creation: Create Books, Students, and IssuedBooks (with IssueDate and ReturnDate).
2. Overdue Logic: Write a query to find all students who haven't returned a book where the IssueDate was more than 14 days ago and ReturnDate is NULL.
3. Popularity Index: Use COUNT and GROUP BY on the Category column to show which genre (e.g., Fiction, Science, History) is borrowed the most.
4. Data Cleanup: Write a DELETE or UPDATE statement to remove student records who haven't borrowed a book in over 3 years (Inactive accounts).

Deliverable: A .sql file containing the DDL (table creation) and the analytical queries.



# Python Project: Smart "Expense Tracker" with Insights
Problem Statement
Many individuals struggle to track daily expenses and understand spending patterns. Build a Python application that allows users to log, categorize, and analyze their expenses.

Objectives:
● Record daily expenses (date, category, amount, description)
● Categorize spending (Food, Travel, Bills, etc.)
● Generate monthly summaries and insights

Key Features:
● CLI or simple GUI input system
● Data storage using CSV or JSON
● Monthly expense summary
● Category-wise breakdown (pie chart using libraries like matplotlib)
● Detect highest spending category

Expected Outcome: A tool that helps users understand where their money goes and suggests areas to reduce spending.

Every use case is set up to show how to use it in real life, how to write clean code, and how to find quick fixes.


# BY: "Kapil Garg" - Manipal University Jaipur
