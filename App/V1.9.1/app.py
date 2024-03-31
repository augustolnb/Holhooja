from database import db
from flask_cors import CORS
from datetime import datetime
#from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, url_for, redirect, request, jsonify
#from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import login_user, LoginManager, login_required, logout_user

from Models.users_model import User
from Models.registros_model import Registros
from Resource.forms import RecForm, LoginForm, RegisterForm


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'thisisasecretkey'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app,resources={r"/*": {"origins": "*"}}) #O uso do cors
#cria as tabelas do banco de dados, caso elas não estejam criadas
@app.before_first_request
def create_tables():
    print("criar tabelas")
    db.create_all()
#fim criaçaõ de tabelas

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
                                      
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(matricula=form.matricula.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data) and user.status == 1:
                login_user(user)
                # Tentativa de adicionar um registro ao banco 20/03
                # O trecho de código abaixo funcionar apenas 1 vez, ou seja, 
                # depois que o usuário tem o primeiro registro criado, 
                # a adição de um novo registro se torna incompativel
                """new_registro = Registros(matricula=form.matricula.data)
                try:
                    db.session.add(new_registro)
                    db.session.commit()
                except:
                    return redirect(url_for('login'))
                """
                if user.tipo == 1:
                    id = user.id
                    matricula = user.matricula
                    data = user.data_cadastro
                    return render_template('dashboard.html', id=id, matricula=matricula, nome=user.nome_completo, data=data)

                if user.tipo == 2:
                    id = user.id
                    matricula = user.matricula
                    data = user.data_cadastro
                    return render_template('admin_dash.html', id=id, matricula=matricula, nome=user.nome_completo, data=data)

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html')

@app.route('/admin_dash', methods=['GET', 'POST'])
@login_required
def admin_dash(): #usuarios = User.query.all()#post = User.query.filter(User.id == current_user.id).all()

    #users = User.query.all()
    solicitacoes = User.query.filter_by(status=0).all()

    return render_template('admin_dash.html', solicitacoes=solicitacoes)

@app.route('/aprovar/<int:id>', methods=['GET', 'POST'])
@login_required
def aprovar(id):
    user = User.query.get_or_404(id)
    user.status = 1 # aprovado
    try:
        db.session.commit()
        solicitacoes = User.query.filter_by(status=0).all()
        return redirect('/admin_dash')
    except: 
        return "Houve um erro no processamento do BD"

@app.route('/reprovar/<int:id>', methods=['GET', 'POST'])
@login_required
def reprovar(id):
    user = User.query.get_or_404(id)
    user.status = 2 # reprovado
    try:
        db.session.commit()
        solicitacoes = User.query.filter_by(status=0).all()
        return redirect('/admin_dash')
    except: 
        return "Houve um erro no processamento do BD"

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    
    # ADICIONAR NO BANCO O REGISTRO DA HORA DE LOGOUT

    """    user = Registros.query.filter_by(matricula=form.matricula.data).first()
    user.logout_hour = datetime.now()
    db.session.add(close_registro)
    db.session.commit()"""

    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash("1234@lpa")
        new_user = User(nome_completo=form.nome_completo.data, matricula=form.matricula.data, email=form.email.data, curso=form.curso.data, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect('/login')
        except: 
            return "Houve um erro no processamento do BD"
            
    return render_template('register.html', form=form)

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    form = RecForm()
    return render_template('recuperar.html', form=form)

@app.route('/senha_nova/<int:id>', methods=['GET', 'POST'])  # <int:id>
@login_required
def senha_nova(id):
    user = User.query.get_or_404(id)
    return render_template("senha_nova.html", id=id, nome=user.nome_completo)

@app.route('/mudar_senha/<int:id>', methods=['GET', 'POST'])  # <int:id>
@login_required
def mudar_senha(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":

        senha1 = request.form['senha1']
        senha2 = request.form['senha2']

        if senha1 == senha2:   
            user.password = bcrypt.generate_password_hash(senha1)
            try:
                db.session.commit()
                mensagem = "Senha atualizada com sucesso!"
                if user.tipo == 1: # usuario comum
                    return render_template('dashboard.html', id=id, matricula=user.matricula, mensagem=mensagem, nome=user.nome_completo, data=user.data_cadastro)
                elif user.tipo == 2: # usuario adm
                    return render_template('admin_dash.html', id=id, matricula=user.matricula, mensagem=mensagem, nome=user.nome_completo, data=user.data_cadastro)
            except: 
                return "Houve um erro na atualização da senha"
                
        return render_template("senha_nova.html", id=id, nome=user.nome_completo)






if __name__ == "__main__": 
    app.run(debug=True)