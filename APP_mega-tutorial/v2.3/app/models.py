from app import db
from app import login
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, DATETIME, ForeignKey, FLOAT
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy as sa
import sqlalchemy.orm as so

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model): 
    __tablename__ = 'user' 
    id = Column(Integer, primary_key=True) 
    nome = Column(String(80), nullable=False) 
    matricula = Column(String(25), nullable=False) 
    password_hash = Column(String(255))
    email = Column(String(80), nullable=False) 
    curso = Column(String(4), nullable=False) 
    tipo = Column(Integer) # 1 > admin || 0 > default
    status = Column(Integer) # 0 > aguardando || 1 > aprovado || -1 > reprovado/inativo
    data_criacao = Column(DATETIME, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<User {}>'.format(self.nome)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_status(self, status):
        self.status = status

class Acesso(db.Model): 
    __tablename__ = 'acesso' 
    id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey('user.id')    ) 
    #amb_id = Column(Integer, nullable=False) 
    data_criacao = Column(DATETIME, nullable=False, default=datetime.now)
    register_type = Column(String(5)) # INPUT / OUTPUT

    def __repr__(self):
        return '<Acesso ID: {}>'.format(self.id)

class Sensores(db.Model): 
    __tablename__ = 'sensores' 
    id = Column(Integer, primary_key=True) 
    #amb_id = Column(Integer, nullable=False) 
    umidade = Column(FLOAT)
    temperatura = Column(FLOAT)
    luminosidade = Column(Integer)
    movimento = Column(Integer)
    ultima_leitura = Column(DATETIME, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Sensores ID: {}>'.format(self.id)