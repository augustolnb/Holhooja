from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditionForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User, Acesso, Sensores
from datetime import datetime

from urllib.parse import urlsplit

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    # USUARIOS ADMIN
    if current_user.status == 1 and current_user.tipo == 1:
        sensores = db.session.scalar(sa.select(Sensores).where(Sensores.id == 1))
        notifs = notifs = db.session.query(User).filter(User.status == 0).all()
        users = db.session.query(Acesso).filter(Acesso.register_type == "in").all()

        # filtra apenas a data
        #data = user.data_criacao.strftime("%d/%m/%y")

        """
        adicionar as notificações sobre numero de usuarios logados no sistema
        baseado na data, no tipo de registro e no ultimo id de cada usuário
        """
        #for user in users:



        return render_template('index_admin.html', title='Dash admin', sensores=sensores, notifs=notifs, users=users)
    
    # USUARIOS DEFAULT
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
            flash('Matricula ou senha invalidas')
            return redirect(url_for('login'))
        if user.status == 0:
            flash('Usuário ainda sem aprovação')
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
        user.set_password(form.senha.data)
        user.set_tipo(0) # default
        user.set_status(0) # aguardando
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

@app.route('/usuarios')
@login_required
def usuarios():
    users = db.session.query(User).all()
    return render_template('usuarios.html', users=users)

@app.route('/usuarios/mudar_tipo/<id>')
@login_required
def mudar_tipo(id):
    users = db.session.query(User).all()
    user = db.first_or_404(sa.select(User).where(User.id == id))
    if user.tipo == 1:
        user.set_tipo(0)
    elif user.tipo == 0:
        user.set_tipo(1)
    db.session.add(user)
    db.session.commit()
    flash('Cadastro atualizado!')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/mudar_status/<id>')
@login_required
def mudar_status(id):
    users = db.session.query(User).all()
    user = db.first_or_404(sa.select(User).where(User.id == id))
    if user.status == 1:
        user.set_status(-1)
    elif user.status == -1:
        user.set_status(1)
    db.session.add(user)
    db.session.commit()
    flash('Cadastro atualizado!')
    return redirect(url_for('usuarios'))





@app.route('/usuarios/editar/<id>')
@login_required
def editar_usuario(id):
    form = EditionForm()
    user = db.session.scalar(sa.select(User).where(User.id == id))
    return render_template('editar_usuario.html', title="Editar dados", form=form, user=user)










## FALTANDO FINALIZAR A LOGICA DE IMPLEMENTAÇÃO 
@app.route('/contatos/<matricula>')
@login_required
def contatos(matricula):
    user = db.first_or_404(sa.select(User).where(User.matricula == matricula))
    ultimo_acesso = db.session.query(Acesso).filter(Acesso.user_id == user.id).order_by(Acesso.data_criacao.desc()).all()
    
    print(ultimo_acesso)
    
    flash('Botao contatos!')
    
    return redirect(url_for('index'))


