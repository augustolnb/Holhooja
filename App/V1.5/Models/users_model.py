# -*- coding: utf-8 -*-
from base import db
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
    tipo = db.Column(db.Integer) # 1-> usuário comum || 2-> usuário adm
#    status = db.Column(db.Integer)
    data_cadastro = db.Column(db.String(12))
#    admin_pai = db.Column(db.String(40))

    # Linha de dita o tipo de relação entre user e registros
    listas = db.relationship("registros_model", back_populates="users")

    def __init__(self,nome,email):
        self.nome_completo = nome_completo
        self.matricula = matricula
        self.password = password
        self.email = email
        self.curso = curso
        self.tipo = tipo
        self.dataCadastro = datetime.now()

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def encontrar_pela_matricula(cls, matricula):
        return cls.query.filter_by(matricula=matricula).first()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
