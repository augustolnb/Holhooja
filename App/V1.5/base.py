# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy(model_class=Base)