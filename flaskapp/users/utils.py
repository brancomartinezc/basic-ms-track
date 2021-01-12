from flask import url_for
from flaskapp import mail
from flask_mail import Message

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''To reset your password, pleas visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you didn't request a password reset, ignore this email.
'''
    mail.send(msg)