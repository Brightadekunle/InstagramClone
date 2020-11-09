from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from clone import db


from . import auth
from .forms import RegistrationForm, LoginForm, PasswordResetForm, PasswordResetRequestForm
from ..models import User
from ..email import send_mail


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate():
        print('Yeah')
        user = User(name=form.name.data, username=form.username.data.lower(), password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
        flash('Invalid email or password.', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/reset-request', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_mail(user.email, 'Reset your password',
                      'auth/email/reset_password', user=user, token=token)
            flash(
                'An email with instructions to reset your email has been sent to you', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = PasswordResetForm()
    if form.validate():
        new_password = form.password.data
        print('Yeah')
        if User.reset_password(token, new_password):
            db.session.commit()
            flash('Your password has been updated!.', 'success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
