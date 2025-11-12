from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from pathlib import Path
from datetime import datetime

APP_SECRET = "change-me"  # ok for class demo
DB_PATH = Path("hw13.db")

app = Flask(__name__)
app.secret_key = APP_SECRET

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(load_sample=True):
    with get_db() as conn, open("schema.sql","r") as f:
        conn.executescript(f.read())
        if load_sample:
            # Only insert if empty
            s_count = conn.execute("SELECT COUNT(*) c FROM students").fetchone()["c"]
            q_count = conn.execute("SELECT COUNT(*) c FROM quizzes").fetchone()["c"]
            r_count = conn.execute("SELECT COUNT(*) c FROM results").fetchone()["c"]
            if s_count == 0:
                conn.execute("INSERT INTO students(first_name,last_name) VALUES(?,?)",
                             ("John","Smith"))
            if q_count == 0:
                conn.execute(
                    "INSERT INTO quizzes(subject,num_questions,quiz_date) VALUES(?,?,?)",
                    ("Python Basics", 5, "2015-02-05")
                )
            if r_count == 0:
                # join to get ids
                sid = conn.execute("SELECT id FROM students WHERE last_name='Smith'").fetchone()["id"]
                qid = conn.execute("SELECT id FROM quizzes WHERE subject='Python Basics'").fetchone()["id"]
                conn.execute(
                    "INSERT INTO results(student_id,quiz_id,score) VALUES(?,?,?)",
                    (sid, qid, 85)
                )

def login_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped

@app.route("/init")
def init():
    init_db(load_sample=True)
    flash("Database initialized with sample data.", "info")
    return redirect(url_for("login"))

# -------- AUTH ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()
        if u == "admin" and p == "password":
            session["user"] = "admin"
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "error")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------- DASHBOARD ----------
@app.route("/dashboard")
@login_required
def dashboard():
    with get_db() as conn:
        students = conn.execute("SELECT id, first_name, last_name FROM students ORDER BY id").fetchall()
        quizzes  = conn.execute("SELECT id, subject, num_questions, quiz_date FROM quizzes ORDER BY id").fetchall()
    return render_template("dashboard.html", students=students, quizzes=quizzes)

# -------- STUDENTS ----------
@app.route("/student/add", methods=["GET","POST"])
@login_required
def add_student():
    if request.method == "POST":
        first = request.form.get("first_name","").strip()
        last  = request.form.get("last_name","").strip()
        if not first or not last:
            flash("First and last name are required.", "error")
            return render_template("add_student.html")
        with get_db() as conn:
            conn.execute("INSERT INTO students(first_name,last_name) VALUES(?,?)", (first,last))
        return redirect(url_for("dashboard"))
    return render_template("add_student.html")

@app.route("/student/<int:student_id>")
@login_required
def view_student_results(student_id):
    with get_db() as conn:
        student = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        rows = conn.execute(
            """
            SELECT r.id, r.score, q.id AS quiz_id, q.subject, q.quiz_date
            FROM results r
            JOIN quizzes q ON q.id = r.quiz_id
            WHERE r.student_id=?
            ORDER BY q.id
            """,
            (student_id,)
        ).fetchall()
    if not rows:
        return render_template("student_results.html", student=student, rows=None)
    return render_template("student_results.html", student=student, rows=rows)

# -------- QUIZZES ----------
@app.route("/quiz/add", methods=["GET","POST"])
@login_required
def add_quiz():
    if request.method == "POST":
        subject = request.form.get("subject","").strip()
        num_q   = request.form.get("num_questions","").strip()
        date    = request.form.get("quiz_date","").strip()  # expects YYYY-MM-DD from <input type=date>
        try:
            num_q = int(num_q)
            datetime.fromisoformat(date)  # validate format
        except Exception:
            flash("Please provide a valid number of questions and date.", "error")
            return render_template("add_quiz.html")
        if not subject:
            flash("Subject is required.", "error")
            return render_template("add_quiz.html")
        with get_db() as conn:
            conn.execute(
                "INSERT INTO quizzes(subject,num_questions,quiz_date) VALUES(?,?,?)",
                (subject, num_q, date)
            )
        return redirect(url_for("dashboard"))
    return render_template("add_quiz.html")

# -------- RESULTS ----------
@app.route("/results/add", methods=["GET","POST"])
@login_required
def add_result():
    with get_db() as conn:
        students = conn.execute("SELECT id, first_name || ' ' || last_name AS name FROM students ORDER BY id").fetchall()
        quizzes  = conn.execute("SELECT id, subject || ' (' || quiz_date || ')' AS label FROM quizzes ORDER BY id").fetchall()

    if request.method == "POST":
        sid = request.form.get("student_id")
        qid = request.form.get("quiz_id")
        score = request.form.get("score")
        try:
            sid = int(sid); qid = int(qid); score = int(score)
        except Exception:
            flash("All fields are required and must be valid.", "error")
            return render_template("add_result.html", students=students, quizzes=quizzes)

        with get_db() as conn:
            try:
                conn.execute(
                    "INSERT INTO results(student_id, quiz_id, score) VALUES(?,?,?)",
                    (sid, qid, score)
                )
            except sqlite3.IntegrityError:
                flash("That student already has a result for this quiz or references are invalid.", "error")
                return render_template("add_result.html", students=students, quizzes=quizzes)
        return redirect(url_for("dashboard"))

    return render_template("add_result.html", students=students, quizzes=quizzes)

if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db(load_sample=True)
    app.run(debug=True)
