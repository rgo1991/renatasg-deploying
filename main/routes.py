from flask import render_template, url_for, flash, redirect, request, abort
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from main.models import User, Post
from main import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='renatas.gorodeckas2@gmail.com', recipients=[user.email])
    msg.body = f'''Reset Password {url_for('reset_token', token=token, _external=True)}'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # If user is already logged in, clicking on register will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instructions on how to reset password')
        return redirect('home')
    return render_template('reset_request.html', title='Reset password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # If user is already logged in, clicking on register will redirect them to home page instead.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): # Create a validation for the form.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password that the user creates.
        user.password = hashed_password
        db.session.commit()  # Commit database changes
        flash(f'Password has been updated!', 'success') # Create a flash message that will use 'success' bootstrap template
        return redirect(url_for('login')) # Return user to homepage once f
    return render_template('reset_token.html', title='Reset Token', form=form)

