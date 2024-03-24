# -*- coding: utf-8 -*-
from database import db
from datetime import datetime
from flask_login import UserMixin

class Registros(db.Model, UserMixin):    
    __tablename__ = 'registros'
    usuario_id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), nullable=False)
    login_hour = db.Column(db.String(20), nullable=False)
    logout_hour = db.Column(db.String(40), nullable=False)
    stranger_key = db.Column(db.Integer, nullable=False)
    dataCadastro = db.Column(db.DateTime)

    def __init__(self, matricula, usuario_id):
        self.matricula = matricula
        self.usuario_id = usuario_id
        self.dataCadastro = datetime.now()

    def adicionar(self):
        db.session.add(self)
        db.session.commit()
    """
    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    """
    @classmethod
    def encontrar_pela_matricula(cls, matricula):
        return cls.query.filter_by(matricula=matricula).first()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()