import os
import logging

from flask import Flask

from FlaskApp.__init__ import db, login_manager
from FlaskApp.views import view

app = Flask(__name__)

# Routing
app.register_blueprint(view)


# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = 'A random key to use CRF for forms'

# Initialize other components
db.init_app(app)
login_manager.init_app(app)


if __name__ == "__main__":
    app.run(
        debug=True,
        host='localhost',
        port=5000
    )
	
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
