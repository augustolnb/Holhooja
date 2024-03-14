from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
"""Declaração do objetivo db foi modificado"""
#db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # incluido 04/03

"""Nova posição após a modificação"""
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(20), unique=True)
    nome_completo = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(80))
    matricula = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    curso = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.Integer) # 1-> usuário comum || 2-> usuário adm
    status = db.Column(db.Integer)
    data_ingresso = db.Column(db.String(12))
    admin_pai = db.Column(db.String(40))

class Registros(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), nullable=False)
    login_hour = db.Column(db.String(20), nullable=False)
    logout_hour = db.Column(db.String(40), nullable=False)
    stranger_key = db.Column(db.Integer, nullable=False)


class RegisterForm(FlaskForm):
    tipo = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=1, max=1)], 
                                        render_kw={"placeholder": "Comum(1) || Adm(2)"})
     
    password = PasswordField(validators=[
                                        InputRequired(), 
                                        Length(min=8, max=20)], 
                                        render_kw={"placeholder": "Password"})
      
    nome_completo = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=8, max=45)], 
                                        render_kw={"placeholder": "Nome Completo"})

    matricula = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=14, max=14)], 
                                        render_kw={"placeholder": "Matricula"})

    curso = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=10, max=30)], 
                                        render_kw={"placeholder": "E-mail"})

    email = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=10, max=30)], 
                                        render_kw={"placeholder": "Curso"})
    '''
    foto = PasswordField(validators=[
                                        InputRequired(), 
                                        Length(min=8, max=20)], 
                                        render_kw={"placeholder": "Password"})
    '''
    submit = SubmitField('Enviar')
    '''
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
    '''

class LoginForm(FlaskForm):
    matricula = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=14, max=14)], 
                                        render_kw={"placeholder": "Matricula"})

    password = PasswordField(validators=[
                                         InputRequired(), 
                                         Length(min=8, max=20)], 
                                         render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class RecForm(FlaskForm):
    email = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=10, max=30)], 
                                        render_kw={"placeholder": "Informe sua matricula"})
    submit = SubmitField('Enviar')                                        

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
                if user.tipo == 1:
                    return redirect(url_for('dashboard'))
#                    return "Usuário COMUM"
                if user.tipo == 2:
                    return redirect(url_for('admin_dash'))
#                    return "Usuário ADMIN"


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