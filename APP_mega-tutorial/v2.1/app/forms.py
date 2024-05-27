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
                                         render_kw={"placeholder": "Password"})

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    nome = StringField(validators=[DataRequired(),
                                    InputRequired(), 
                                    Length(min=3, max=20)], 
                                    render_kw={"placeholder": "Nome"})

    matricula = StringField(validators=[DataRequired(),
                                        InputRequired(), 
                                        Length(min=14, max=14)], 
                                        render_kw={"placeholder": "Matricula"})

    password1 = PasswordField(validators=[DataRequired(),
                                         InputRequired(), 
                                         Length(min=8, max=20)], 
                                         render_kw={"placeholder": "Password"})

    password2 = PasswordField(validators=[DataRequired(),
                                         InputRequired(), 
                                         Length(min=8, max=20), 
                                         EqualTo('password1')],
                                         render_kw={"placeholder": "Repeat Password"})

    submit = SubmitField('Register')

    def validate_matricula(self, matricula):
        user = db.session.scalar(sa.select(User).where(
            User.matricula == matricula.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    """
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
    """