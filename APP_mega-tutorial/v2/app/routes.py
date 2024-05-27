from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User

@app.route('/')

@app.route('/index')
def index():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("\nUsuario autenticado\n")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.matricula == form.matricula.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))