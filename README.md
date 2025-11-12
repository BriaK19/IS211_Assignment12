# Week 12 Flask Assignment — Student & Quiz Tracker

This project was created for **IS211: Software Application Programming II** at **CUNY School of Professional Studies**.  
It demonstrates how to use the **Flask framework** with a **SQLite database** to build a simple web application for tracking students, quizzes, and quiz results.

---

## **Project Overview**

This web application allows a teacher to:
- Add students and quizzes
- Record quiz results for each student
- View a list of all students, quizzes, and results stored in the database

The goal of this assignment was to extend a Flask application using a **relational database** (SQLite) and connect it to a web interface for interaction.

---

## **Technologies Used**

- **Python 3**
- **Flask 3.0**
- **SQLite 3**
- **HTML / Jinja Templates**

---

## **File Structure**
├── app.py # Main Flask application file
├── schema.sql # SQL script for creating database tables
├── requirements.txt # Python dependencies
├── hw13.db # SQLite database file (auto-created on first run)
└── templates/ # HTML templates for the web interface
├── base.html
├── add_student.html
├── add_quiz.html
├── add_result.html
├── dashboard.html
└── student_results.html

---

## **Setup Instructions**

1. **Clone this repository:**
   ```bash
   git clone https://github.com/BriaK19/IS211_Assignment12.git
   cd IS211_Assignment12

   python3 -m venv .venv
source .venv/bin/activate   # On Mac/Linux
.venv\Scripts\activate      # On Windows

pip install -r requirements.txt

sqlite3 hw13.db < schema.sql

python app.py

http://127.0.0.1:5000

Features
Add new students and quizzes via web forms
Record quiz results
View results in a dashboard interface
Persistent storage using SQLite
Organized templates with Flask’s Jinja2 rendering engine
