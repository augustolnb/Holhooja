from app import db
from app import login
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, DATETIME, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy as sa
import sqlalchemy.orm as so

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model): 
    __tablename__ = 'user' 
    id = Column(Integer, primary_key=True) 
    #manager_id = Column(ForeignKey("manager_id"))
    nome = Column(String(255), nullable=False) 
    matricula = Column(String(255), nullable=False) 
    password = Column(String(255))

    # PROBLEMAS COM USO DA CHAVE ESTRAGEIRA
    #reports_to = relationship("Acesso", foreign_keys=manager_id)

    def __repr__(self):
        return '<User {}>'.format(self.nome)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Acesso(db.Model): 
    __tablename__ = 'acesso' 
    id = Column(Integer, primary_key=True) 
    #user_id = Column(Integer, ForeignKey('User.id')) 
    #amb_id = Column(Integer, nullable=False) 
    data_criacao = Column(DATETIME, nullable=False, default=datetime.now)  
    """
    __mapper_args__ = {
        "inherit_condition": user_id == User.id,
        "polymorphic_identity": "acesso",
    }
    """
    def __repr__(self):
        #return '<User ID: {}>'.format(self.user_id)
        return '<User ID: {}>'.format(self.id)









    """
    email = Column(String(255), unique=True, nullable=False) 
    password = Column(String(255), nullable=False) 
    curso = Column(String(255)) 
    tipo = Column(Integer, nullable=False, default=1) 
    status = Column(Integer, nullable=False, default=0) 
    data_criacao = Column(DATETIME, nullable=False, default=datetime.now)  
    """