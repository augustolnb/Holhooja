# -*- coding: utf-8 -*-
from database import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(80))
    matricula = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    curso = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.Integer, default=1)
    """ tipo
    1 > Comum
    2 > Administrador
    """
    status = db.Column(db.Integer, default=0)
    """ status
    0 > aguardando
    1 > aprovado/ativo
    2 > reprovado
    3 > inativo
    """
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, nome_completo, matricula, email, curso, password):
        self.nome_completo = nome_completo
        self.matricula = matricula
        self.email = email
        self.curso = curso
        self.password = password

    def __repr__(self):
        return {
            "id": self.id,
            "nome_completo": self.nome_completo,
            "matricula": self.matricula,
            "senha": self.password
        }
