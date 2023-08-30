## Code in this module will be used to validate user input,
## when the user tries to register or login to our site.

# Main function thar our main class will inherit from
from flask_wtf import FlaskForm
# StringField is needed if youre going to have string values in your class
# PasswordField is needed if youre going to have passwords in yoru class
# SubmitField is for the submit button
# Booleanfield allows for true false values. Good for keeping users logged in after they close app. User in 'remember' variable below
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Validators to validate the variables. Handy becuase you dont have to write the verification functions yourself
# Datarequired tells that this variable is required. Lenght allows to specify min and max lenght of variable
# Email verifies thats its a valid email.
# Equalto checks if a field is equal to another field. Used to confirm passwords for example
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

