from .initialize_db import *

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    destination_id = Column(ForeignKey('location.id'))
    name = Column(Text)

    destination = relationship('Location')
    deliveries = relationship('Delivery', secondary='project_delivery', back_populates='peojects')