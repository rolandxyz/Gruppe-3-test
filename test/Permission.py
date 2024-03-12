from .initialize_db import *

class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)

    roles = relationship('Role', secondary='role_perm', back_populates='permissions')