from .Classes import *

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    permissions = relationship('Permission', lazy="joined", secondary='role_perm', overlaps='roles')