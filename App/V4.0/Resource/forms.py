from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

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