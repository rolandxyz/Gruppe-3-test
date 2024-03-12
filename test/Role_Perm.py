from .initialize_db import *

class Role_Perm(Base):
    __tablename__ = 'role_perm'

    role_id = Column(ForeignKey('role.id'), primary_key=True)
    permission_id = Column(ForeignKey('permission.id'), primary_key=True)