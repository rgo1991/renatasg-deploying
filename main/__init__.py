from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#Secret key is used to sign session cookies for protection against cookie data tampering
app.config['SECRET_KEY'] = '41570e8b023610560c5c76480ac34c7b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # redirect user to login page if they user /account url manually and are not logged in
login_manager.login_message_category = 'info' # Updates flashed message style on login page, when trying to access /account url manually and are not logged in

from main import routes



