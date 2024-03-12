from .Classes import *


class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)

    roles = relationship('Role', lazy="joined", secondary='role_perm', overlaps="permissions")