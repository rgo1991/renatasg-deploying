from flask import render_template, url_for, flash, redirect, request
from main.forms import RegistrationForm, LoginForm
from main.models import User, Post
from main import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': '123',
        'title': '123',
        'content': '123',
        'date_posted': '123'
    },
    {
        'author': '123',
        'title': '123',
        'content': '123',
        'date_posted': '123'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

#define the register function. That accepts POST and GET html requests from users (allows user to submit things via the form)
@app.route("/register",  methods=['GET', 'POST'])
def register():
    # If user is already logged in, clicking on register will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm() # Create a class instance called form
    if form.validate_on_submit(): # Create a validation for the form.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password that the user creates.
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Create user from user supplied fields
        db.session.add(user) # Create user in database
        db.session.commit()  # Commit database changes
        flash(f'Account created for {form.username.data}!', 'success') # Create a flash message that will use 'success' bootstrap template
        return redirect(url_for('login')) # Return user to homepage once form has been successfully submited
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already logged in, clicking on login will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Check if email provided matches with anyting in DB
        if user and bcrypt.check_password_hash(user.password, form.password.data): # if 'user' is not none and password matches encrypted password. Log the user in
            login_user(user, remember=form.remember.data) # log the user in using login_user module from flask_login
            next_page = request.args.get('next') # 44.00 in video. basically if the 'next' param exists. User will be redirected to page they were originally trying to access (/account) after login
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required # Route only displays if the user is logged in
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) 	
    return render_template('account.html', title='Account', image_file=image_file)
