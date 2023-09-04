import os

class Config:
    # In the video he sets the sensitive info in this config to environment variables and references them that way. But i wasnt arsed.
    # ENV variables are set in the .bash_profile or a private dot(.) file
    SECRET_KEY = '41570e8b023610560c5c76480ac34c7b'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtn.googlemail.com'
    MAIL_PORT = 587
    MAIL_USER_TLS = True
    MAIL_USER = 'renatas.gorodeckas2'
    MAIL_PASSWORD = 'Milikoniumokykla1991!'