# -*- coding: utf-8 -*-
from database import db
from datetime import datetime
from flask_login import UserMixin
from Models.users_model import User
from Models.registros_model import Registros

class Visita(db.Model, UserMixin):
    __tablename__="visita"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registro_id = db.Column(db.Integer, db.ForeignKey('registros.id'))
    data = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', foreign_keys=user_id)
    registro = db.relationship('Registros', foreign_keys=registro_id)

    def __init__(self, user_id, registro_id):
        self.user_id = user_id
        self.registro_id = registro_id

    def __repr__(self):
        return "Visita número #{} realizada dia {} pelo usuário {}".format(self.id, self.data, self.user_id)