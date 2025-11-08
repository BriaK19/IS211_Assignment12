from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-string"

# In-memory store for to-do items (resets when the server restarts)
# Each item is a dict: {"task": str, "email": str, "priority": "Low"|"Medium"|"High"}
todo_items = []


def validate_email(email: str) -> bool:
    """Very small email sanity check (enough for this assignment)."""
    if not email or "@" not in email:
        return False
    local, _, domain = email.partition("@")
    return bool(local) and "." in domain


@app.route("/")
def index():
    # Render the table and the form
    return render_template("index.html", todos=todo_items)


@app.route("/submit", methods=["POST"])
def submit():
    task = (request.form.get("task") or "").strip()
    email = (request.form.get("email") or "").strip()
    priority = (request.form.get("priority") or "").strip()

    valid_priorities = {"Low", "Medium", "High"}

    # Basic validations per assignment
    errors = []
    if not task:
        errors.append("Task is required.")
    if not validate_email(email):
        errors.append("Please enter a valid email address.")
    if priority not in valid_priorities:
        errors.append("Priority must be Low, Medium, or High.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("index"))

    todo_items.append({"task": task, "email": email, "priority": priority})
    flash("To-Do item added.", "success")
    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear():
    todo_items.clear()
    flash("All To-Do items cleared.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Access at http://localhost:5000
    app.run(debug=True)
