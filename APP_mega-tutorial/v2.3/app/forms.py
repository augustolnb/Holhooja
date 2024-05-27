from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired,  Email, EqualTo

import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    matricula = StringField(validators=[DataRequired(),
                                        InputRequired(), 
                                        Length(min=14, max=14)], 
                                        render_kw={"placeholder": "Matricula"})

    password = PasswordField(validators=[DataRequired(),
                                         InputRequired(), 
                                         Length(min=8, max=20)], 
                                         render_kw={"placeholder": "Senha"})

    remember_me = BooleanField('Lembrar senha')

    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    nome = StringField(validators=[DataRequired(),
                                    InputRequired(), 
                                    Length(min=3, max=40)], 
                                    render_kw={"placeholder": "Nome Completo"})

    matricula = StringField(validators=[DataRequired(),
                                        InputRequired(), 
                                        Length(min=14, max=14)], 
                                        render_kw={"placeholder": "Matricula"})

    password1 = PasswordField(validators=[DataRequired(),
                                         InputRequired(), 
                                         Length(min=8, max=20)], 
                                         render_kw={"placeholder": "Senha"})

    password2 = PasswordField(validators=[DataRequired(),
                                         InputRequired(), 
                                         Length(min=8, max=20), 
                                         EqualTo('password1')],
                                         render_kw={"placeholder": "Senha novamente"})

    email = StringField(validators=[    InputRequired(), 
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
    

    submit = SubmitField('Registrar')

    def validate_matricula(self, matricula):
        user = db.session.scalar(sa.select(User).where(
            User.matricula == matricula.data))
        if user is not None:
            raise ValidationError('Matricula ja registrada.\nVerifique o numero de matricula ou procure um administrador')

    """
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
    """