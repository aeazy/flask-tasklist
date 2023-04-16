DROP TABLE IF EXISTS tasks;

DROP TABLE IF EXISTS completed_tasks;

CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT,
  date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE completed_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    title TEXT,
    body TEXT,
    date_created TIMESTAMP, 
    date_completed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 