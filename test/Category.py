from .initialize_db import *

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category = Column(Text)