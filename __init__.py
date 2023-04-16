import calendar
import os
from datetime import date

from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='eazy',
        DATABASE=os.path.join(app.instance_path, 'tasklist.sqlite')
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # confirm instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.context_processor
    def date_today():
        day_str = calendar.day_name[date.today().weekday()]
        date_str = date.today().strftime('%B %d, %Y')
        return {'date_today': "{0}, {1}".format(day_str, date_str)}
    
    # initialize the database
    from .db import init_db
    db.init_app(app)
            
    # import the todo list
    from . import tasks
    app.register_blueprint(tasks.bp)
    app.add_url_rule('/', endpoint='index') # == app.add_url_rule(url_for('dashboard.index'))

    return app