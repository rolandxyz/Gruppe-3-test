from sqlalchemy import create_engine, ForeignKey, Column, Table, Date, Text, Integer, Float, Boolean, func, exists
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_guid import GUID

from flask_login import UserMixin

import uuid

engine = create_engine('sqlite:///database/reliefgoodslogistics.db', pool_size=100, max_overflow=125)
Base = declarative_base()
Session = sessionmaker(bind=engine)
dbsession = Session()
metadata = Base.metadata