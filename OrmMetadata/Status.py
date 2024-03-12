from .Classes import *

class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    status = Column(Text)