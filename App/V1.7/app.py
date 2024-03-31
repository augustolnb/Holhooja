from flask_cors import CORS
from flask_restful import Api
from datetime import datetime
#from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from flask import Flask, render_template, url_for, redirect, request
#from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from Models.users_model import User
from Models.registros_model import Registros
from Resource.forms import RecForm, LoginForm, RegisterForm
from database import db

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

#api = Api(app)
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
            if bcrypt.check_password_hash(user.password, form.password.data):
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
                    return redirect(url_for('dashboard'))
                if user.tipo == 2:

                    return redirect(url_for('admin_dash'))
                    #return render_template('admin_dash.html', usuario=user.matricula)


    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin_dash', methods=['GET', 'POST'])
@login_required
def admin_dash(): #usuarios = User.query.all()#post = User.query.filter(User.id == current_user.id).all()
    user = User.query.filter_by(matricula=current_user.matricula).first()

    if request.method == "POST":
        return "Vc usou o método post"
        #return render_template('admin_dash.html', user=user)

    return render_template('admin_dash.html')

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