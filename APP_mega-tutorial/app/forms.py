from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired

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
