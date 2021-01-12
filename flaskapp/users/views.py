from flask import render_template, url_for, redirect, request, flash, Blueprint
from flaskapp import db, bcrypt, mail
from flaskapp.users.forms import SignupForm, LoginForm, UpdateAccountForm, RequestResetForm, PasswordResetForm
from flaskapp.models import User
from flask_login import login_user, logout_user, current_user, login_required
from flaskapp.users.utils import send_reset_email

users = Blueprint('users', __name__)

@users.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created, you can signup now.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/signup.html', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect email or password.', 'danger')
    return render_template('users/login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('users/account.html', form=form)

@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with instructions to reset your password has been sent.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', form=form)

@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or expired.', 'danger')
        return redirect(url_for('users.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('The password has been updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', form=form)