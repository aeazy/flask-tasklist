from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('tasks', __name__)

@bp.route('/')
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT id, title, body, date_created'
        '  FROM tasks'
        '  ORDER BY date_created DESC'
    ).fetchall()
    return render_template('index.html', tasks=tasks)

@bp.route('/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title cannot be empty'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tasks (title, body)'
                '  VALUES (?, ?)',
                (title, body)
            )
            db.commit()
            return redirect(url_for('tasks.index'))
    return redirect(url_for('tasks.index'))

def get_task(id):
    task = get_db().execute(
        'SELECT id, title, body, date_created'
        '  FROM tasks'
        '  WHERE id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} does not exist!")

    return task

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title cannot be empty'
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE tasks SET title = ?, body = ?'
                '  WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('tasks.index'))
        
    return render_template('tasks/update.html', task=task)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tasks.index'))

@bp.route('/<int:id>/completed', methods=('GET', 'POST'))
def complete(id):
    get_task(id)
    # initialize db
    db = get_db()
    db.execute(
        'INSERT INTO completed_tasks (task_id, title, body, date_created)'
        'SELECT id, title, body, date_created FROM tasks WHERE id = ?', (id,)
    )
    db.execute(
        'DELETE FROM tasks WHERE id = ?', (id,)
    )
    db.commit()
    
    return redirect(url_for('tasks.index'))

@bp.route('/<int:id>/undo', methods=('GET', 'POST'))
def undo(id):
    db = get_db()
    db.execute(
        'INSERT INTO tasks (title, body, date_created)'
        'SELECT title, body, date_created FROM completed_tasks WHERE task_id = ?', (id,)
    )
    db.execute(
        'DELETE FROM completed_tasks WHERE task_id = ?', (id,)
    )
    db.commit()
    
    return redirect(url_for('tasks.completed_index'))

@bp.route('/completedTasks', methods=('GET', 'POST'))
def completed_index():
    db = get_db()
    completed_tasks = db.execute(
        'SELECT task_id, title, body, date_created, date_completed'
        '  FROM completed_tasks'
        '  ORDER BY date_completed DESC'
    ).fetchall()
    
    return render_template('tasks/completedTasks.html', completed_tasks=completed_tasks)

def get_completed_task(id):
    completed_task = get_db().execute(
        'SELECT id, task_id, title, body, date_created'
        '  FROM completed_tasks'
        '  WHERE task_id = ?',
        (id,)
    ).fetchone()

    if completed_task is None:
        abort(404, f"Completed task id {id} does not exist!")

    return completed_task


@bp.route('/<int:id>/deleteforever', methods=('GET', 'POST'))
def delete_forever(id):
    get_completed_task(id)
    db = get_db()
    db.execute('DELETE FROM completed_tasks WHERE task_id = ?', (id,))
    db.commit()
    return redirect(url_for('tasks.completed_index'))
