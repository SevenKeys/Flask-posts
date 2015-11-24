import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_instance_folder_path():
    return os.path.join(BASE_DIR, 'instance') 

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b' 

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(BASE_DIR),'tmp/user_posts.db')
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f' 

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '792842bc-c4df-4de1-9177-d5207bd9faa6'

config = {
    "development": "user_posts.config.DevelopmentConfig",
    "testing": "user_posts.config.TestingConfig",
    "default": "user_posts.config.DevelopmentConfig"
}

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)