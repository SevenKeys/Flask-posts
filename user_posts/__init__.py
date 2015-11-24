from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from user_posts.main.views import main
from user_posts.auth.views import admin
from user_posts.data.models import Author, db

from config import get_instance_folder_path, configure_app

# Define the WSGI application object
app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            template_folder='templates')

# Configurations
configure_app(app)

# Initialization and creation database from models
db.init_app(app)

# Registration modules
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html', path=request.path), 404

@app.errorhandler(405)
def method_not_allowed(error):
	return render_template('errors/405.html'), 405

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('errors/500.html',error=e), 500
