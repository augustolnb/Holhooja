from flask_cors import CORS
from flask_restful import Api
from datetime import datetime
#from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from flask import Flask, render_template, url_for, redirect
#from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#from Models.users_model import User
#from Models.registros_model import Registros
from Resource.forms import RecForm, LoginForm, RegisterForm

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'thisisasecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#api = Api(app)
CORS(app,resources={r"/*": {"origins": "*"}}) #O uso do cors
#cria as tabelas do banco de dados, caso elas não estejam criadas
@app.before_first_request
def create_tables():
    print("criar tabelas")
    db.create_all()
#fim criaçaõ de tabelas

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(80))
    matricula = db.Column(db.String(20), db.ForeignKey('registros.matricula'), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    curso = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.Integer) # 1-> usuário comum || 2-> usuário adm
#    status = db.Column(db.Integer)
    data_cadastro = db.Column(db.DateTime)
#    admin_pai = db.Column(db.String(40))
    #registro_id = db.Column(db.Integer, )
    registro = db.relationship("Registros", primaryjoin='User.matricula == Registros.matricula')  # Relationship with Registro model

    def __init__(self, nome_completo, matricula, password, email, curso, tipo):
        self.nome_completo = nome_completo
        self.matricula = matricula
        self.password = password
        self.email = email
        self.curso = curso
        self.tipo = tipo
        self.data_cadastro = datetime.now() # selecionar apenas o dd/mm/aaaa


    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pela_matricula(cls, matricula):
        return cls.query.filter_by(matricula=matricula).first()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()

class Registros(db.Model, UserMixin):    
    __tablename__ = 'registros'
    matricula = db.Column(db.String(20), primary_key=True, nullable=False)
    login_hour = db.Column(db.DateTime)
    logout_hour = db.Column(db.DateTime)

    def __init__(self, matricula):
        self.matricula = matricula
        self.login_hour = datetime.now()

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pela_matricula(cls, matricula):
        return cls.query.filter_by(matricula=matricula).first()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()

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
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                # Tentativa de adicionar um registro ao banco 20/02
                new_registro = Registros(matricula=form.matricula.data)
                db.session.add(new_registro)
                db.session.commit()

                if user.tipo == 1:
                    return redirect(url_for('dashboard'))
                if user.tipo == 2:
                    return redirect(url_for('admin_dash'))

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin_dash', methods=['GET', 'POST'])
@login_required
def admin_dash():
    return render_template('admin_dash.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(nome_completo=form.nome_completo.data, matricula=form.matricula.data, password=hashed_password, email=form.email.data, curso=form.curso.data, tipo=form.tipo.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    form = RecForm()

    return render_template('recuperar.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)