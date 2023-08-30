from flask import render_template, url_for, flash, redirect
from main.forms import RegistrationForm, LoginForm
from main.models import User, Post
from main import app


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
    form = RegistrationForm() # Create a class instance called form
    if form.validate_on_submit(): # Create a validation for the form.
        flash(f'Account created for {form.username.data}!', 'success') # Create a flash message that will use 'success' bootstrap template
        return redirect(url_for('home')) # Return user to homepage once form has been successfully submited
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
