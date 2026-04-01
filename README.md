# Hospital Management System (DSA Assignment)

## Overview
This project is a Hospital Management System developed using Python Flask, SQLite, HTML, and CSS. It demonstrates practical application of Data Structures and Algorithms to solve a real-world healthcare management problem.

## Features
- Add patient records
- View all patients
- Edit patient information
- Delete patient records
- Search patients
- Sort patients by severity
- DSA demonstration routes

## Data Structures Used
### 1. Linked List
Used to manage patient records dynamically.

### 2. Binary Search Tree
Used to organize patients based on severity level.

### 3. Recursion
Used in inorder traversal of the binary tree.

### 4. Hash Table
Used for fast patient lookup by ID.

### 5. Queue
Used to simulate patient flow in order of arrival.

### 6. Stack
Used to track system actions like add, delete, and update.

## Technologies
- Python
- Flask
- SQLite
- HTML/CSS

## Run Instructions
1. Install Flask:
```bash
pip install flask

Data Structures and Algorithms Used
1. Linked List

A custom Linked List was implemented to store and manage patient records dynamically.
It supports:

appending new patients
deleting patient records
searching for patients
traversing all stored records

This is useful because patient records can be added and removed frequently in a hospital system.

2. Binary Tree (Binary Search Tree)

A Binary Search Tree (BST) was implemented to organize patients based on severity level.
It supports:

insertion of patients
searching by severity
inorder traversal of records

This allows structured organization and efficient searching of patient data.

3. Recursive Algorithms

Recursion was used in the Binary Search Tree implementation.
Recursive methods are used for:

tree insertion
inorder traversal
tree search

This satisfies the recursive algorithm requirement of the assignment.

4. Hash Table

A custom Hash Table was implemented for fast patient lookup using patient IDs.
It supports:

insert
get/search
delete
display

Collision handling is done using chaining.

This allows fast access to patient records.

5. Sorting Algorithm

A custom Insertion Sort algorithm was implemented to sort patients by severity level in descending order.

This ensures the project includes a proper algorithmic sorting implementation rather than relying only on database sorting.

6. Searching Algorithms

The system includes multiple searching techniques:

Linked List search
Binary Search Tree search
Hash Table lookup
Database keyword search

These are used to efficiently locate patient records based on different criteria such as:

patient ID
severity
name
condition
phone number
bed number
#Updated final version#