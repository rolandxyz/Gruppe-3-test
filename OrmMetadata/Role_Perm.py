from .Classes import *

class Role_Perm(Base):
    __tablename__ = 'role_perm'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('role.id'))
    permission_id = Column(ForeignKey('permission.id'))

    role = relationship('Role', lazy="joined", overlaps="roles, permissions")
    permission = relationship('Permission', lazy="joined", overlaps="roles, permissions")
