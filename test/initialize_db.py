from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship,aliased
from sqlalchemy.dialects.postgresql import UUID

engine = create_engine('sqlite:///database/hilfsgüterlogistik.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
dbsession = Session()