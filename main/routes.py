from flask import render_template, url_for, flash, redirect, request, abort
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from main.models import User, Post
from main import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
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

# Save a picture that the user uploads to the profile_pics dir
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # Get file extension
    picture_fn = random_hex + f_ext # create new file name from random hex + extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # create full path to file name

    # Resize pic once its uploaded
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save it
    i.save(picture_path)
    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    # Display current user info in the form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # Set user profile pic to current_user.image_file
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # Return the account.html template for this page
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been submited', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted', 'success')
    return redirect(url_for('home'))
