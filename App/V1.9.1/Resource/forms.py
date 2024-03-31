from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

class RegisterForm(FlaskForm):
    
   
    nome_completo = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=8, max=45)], 
                                        render_kw={"placeholder": "Nome Completo"})

    matricula = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=14, max=14)], 
                                        render_kw={"placeholder": "Matricula"})    

    email = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=10, max=40)], 
                                        render_kw={"placeholder": "Email"})
    
    curso = SelectField(u'Curso', choices=[('EE', 'Engenharia Elétrica'), 
                                            ('EC', 'Engenharia Civil'),
                                            ('EA', 'Engenharia Agronômica'),
                                            ('SI', 'Sistemas para Internet'),
                                            ('FI', 'Física'),
                                            ('MA', 'Matemática'),
                                            ('LE', 'Letras'),
                                            ('GP', 'Gestão Pública')],
                                validators=[InputRequired()])
    
    submit = SubmitField('Enviar')

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
    matricula = StringField(validators=[
                                        InputRequired(), 
                                        Length(min=10, max=30)], 
                                        render_kw={"placeholder": "Matricula"})
    submit = SubmitField('Enviar')  