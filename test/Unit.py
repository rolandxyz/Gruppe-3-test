from .initialize_db import *

class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    unit = Column(Text)