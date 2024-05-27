from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User, Acesso, Sensores

from urllib.parse import urlsplit

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():

    if current_user.status == 1 and current_user.tipo == 1:
        sensores = db.session.scalar(sa.select(Sensores).where(Sensores.id == 1))
        notifs = notifs = db.session.query(User).filter(User.status == 0).all()

        return render_template('index_admin.html', title='Dash admin', sensores=sensores, notifs=notifs)
    
    if current_user.status == 1 and current_user.tipo == 0:
        return render_template('index.html', title='Dash default')

    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("\nUsuario autenticado\n")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.matricula == form.matricula.data))
        if user is None or not user.check_password(form.senha.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        acesso =  Acesso(user_id=user.id , register_type="in")
        db.session.add(acesso)
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout/<id>')
def logout(id):
    logout_user()
    acesso =  Acesso(user_id=id , register_type="out")
    db.session.add(acesso)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(matricula=form.matricula.data, nome=form.nome.data, email=form.email.data, curso=form.curso.data)
        user.set_password(form.password1.data)
        user.set_tipo(1) # admin
        user.set_status(1) # aprovado
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<matricula>')
@login_required
def user(matricula):
    user = db.first_or_404(sa.select(User).where(User.matricula == matricula))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/aprovar_status/<matricula>')
@login_required
def aprovar_status(matricula):
    user = db.first_or_404(sa.select(User).where(User.matricula == matricula))
    user.set_status(1) # aprovado
    db.session.add(user)
    db.session.commit()
    flash('Usuario aprovado!')
    
    return redirect(url_for('index'))

@app.route('/reprovar_status/<matricula>')
@login_required
def reprovar_status(matricula):
    user = db.first_or_404(sa.select(User).where(User.matricula == matricula))
    user.set_status(-1) # reprovado
    db.session.add(user)
    db.session.commit()
    flash('Usuario Reprovado!')
    
    return redirect(url_for('index'))
