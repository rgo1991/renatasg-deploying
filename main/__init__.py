from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from main.config import Config


db = SQLAlchemy() # create db instance
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # redirect user to login page if they user /account url manually and are not logged in
login_manager.login_message_category = 'info' # Updates flashed message style on login page, when trying to access /account url manually and are not logged in

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # Import the configs from the config.py file
    app.app_context().push()  # needed for SQLalchemy to create db. Got from internet myself

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from main.users.routes import users
    from main.posts.routes import posts
    from main.main.routes import main
    from main.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app



