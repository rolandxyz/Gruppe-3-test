from .initialize_db import *

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    permissions = relationship('Permission', secondary='role_perm', back_populates='roles')