from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.models import User, Post
from main.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from main.users.utils import save_picture, send_reset_email
from flask import Blueprint

users = Blueprint('users', __name__)


#define the register function. That accepts POST and GET html requests from users (allows user to submit things via the form)
@users.route("/register",  methods=['GET', 'POST'])
def register():
    # If user is already logged in, clicking on register will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm() # Create a class instance called form
    if form.validate_on_submit(): # Create a validation for the form.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password that the user creates.
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Create user from user supplied fields
        db.session.add(user) # Create user in database
        db.session.commit()  # Commit database changes
        flash(f'Account created for {form.username.data}!', 'success') # Create a flash message that will use 'success' bootstrap template
        return redirect(url_for('users.login')) # Return user to homepage once form has been successfully submited
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already logged in, clicking on login will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Check if email provided matches with anyting in DB
        if user and bcrypt.check_password_hash(user.password, form.password.data): # if 'user' is not none and password matches encrypted password. Log the user in
            login_user(user, remember=form.remember.data) # log the user in using login_user module from flask_login
            next_page = request.args.get('next') # 44.00 in video. basically if the 'next' param exists. User will be redirected to page they were originally trying to access (/account) after login
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required # Route only displays if the user is logged in
def account():
    form = UpdateAccountForm()
    # If the update account form passes validation in that new values dont exist in db then update the current user values
    if form.validate_on_submit():
        # if the user also ulaoded a picture then save pic using function and set it as user profile pic
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    # Display current user info in the form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # Set user profile pic to current_user.image_file
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # Return the account.html template for this page
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # If user is already logged in, clicking on register will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instructions on how to reset password')
        return redirect('home')
    return render_template('reset_request.html', title='Reset password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # If user is already logged in, clicking on register will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): # Create a validation for the form.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password that the user creates.
        user.password = hashed_password
        db.session.commit()  # Commit database changes
        flash(f'Password has been updated!', 'success') # Create a flash message that will use 'success' bootstrap template
        return redirect(url_for('users.login')) # Return user to homepage once f
    return render_template('reset_token.html', title='Reset Token', form=form)

