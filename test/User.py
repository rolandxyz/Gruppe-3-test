from .initialize_db import *

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('role.id'))
    username = Column(Text)
    surname = Column(Text)
    name = Column(Text)
    password = Column(Text)

    role = relationship('Role')
