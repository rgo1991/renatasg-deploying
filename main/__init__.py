from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Secret key is used to sign session cookies for protection against cookie data tampering
app.config['SECRET_KEY'] = '41570e8b023610560c5c76480ac34c7b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.app_context().push()

from main import routes



