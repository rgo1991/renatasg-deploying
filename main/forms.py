## Code in this module will be used to validate user input,
## when the user tries to register or login to our site.

# Main function thar our main class will inherit from
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# StringField is needed if youre going to have string values in your class
# PasswordField is needed if youre going to have passwords in yoru class
# SubmitField is for the submit button
# Booleanfield allows for true false values. Good for keeping users logged in after they close app. User in 'remember' variable below
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# Validators to validate the variables. Handy becuase you dont have to write the verification functions yourself
# Datarequired tells that this variable is required. Lenght allows to specify min and max lenght of variable
# Email verifies thats its a valid email.
# Equalto checks if a field is equal to another field. Used to confirm passwords for example
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User
from flask_login import current_user


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

    def validate_username(self, username):
        # Check if the username supplied in current form matches with any username already in database.
        # If there is a match the 'user' will have a value of the match, if not then 'user' will be None.
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        # Check if the username supplied in current form matches with any username already in database.
        # If there is a match the 'user' will have a value of the match, if not then 'user' will be None.
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email already exists. Please choose a different one')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email already exists. Please choose a different one')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')