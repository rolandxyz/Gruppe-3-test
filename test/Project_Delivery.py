from .initialize_db import *

class Project_Delivery(Base):
    __tablename__ = 'project_delivery'

    project_id = Column(ForeignKey('project.id'), primary_key=True)
    delivery_id = Column(ForeignKey('delivery.id'), primary_key=True)
