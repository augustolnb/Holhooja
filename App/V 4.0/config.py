import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mariadb+mariadbconnector://augusto:1234@127.0.0.1:3306/sql_db"
