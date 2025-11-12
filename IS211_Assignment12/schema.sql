 PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quizzes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  num_questions INTEGER NOT NULL CHECK(num_questions >= 1),
  quiz_date TEXT NOT NULL         -- store ISO date 'YYYY-MM-DD'
);

CREATE TABLE IF NOT EXISTS results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  quiz_id INTEGER NOT NULL,
  score INTEGER NOT NULL CHECK(score BETWEEN 0 AND 100),
  UNIQUE(student_id, quiz_id),
  FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
  FOREIGN KEY(quiz_id) REFERENCES quizzes(id)   ON DELETE CASCADE
);
