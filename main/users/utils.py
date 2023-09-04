import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from main import mail

# Save a picture that the user uploads to the profile_pics dir
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # Get file extension
    picture_fn = random_hex + f_ext # create new file name from random hex + extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # create full path to file name

    # Resize pic once its uploaded
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save it
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='renatas.gorodeckas2@gmail.com', recipients=[user.email])
    msg.body = f'''Reset Password {url_for('users.reset_token', token=token, _external=True)}'''
    mail.send(msg)