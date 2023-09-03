from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
#Secret key is used to sign session cookies for protection against cookie data tampering
app.config['SECRET_KEY'] = '41570e8b023610560c5c76480ac34c7b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) # create db instance
app.app_context().push() # needed for SQLalchemy to create db. Got from internet myself
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # redirect user to login page if they user /account url manually and are not logged in
login_manager.login_message_category = 'info' # Updates flashed message style on login page, when trying to access /account url manually and are not logged in
app.config['MAIL_SERVER'] = 'smtn.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_TLS'] = True
app.config['MAIL_USER'] = 'renatas.gorodeckas2'
app.config['MAIL_PASSWORD'] = 'Milikoniumokykla1991!'
mail = Mail(app)

from main import routes



