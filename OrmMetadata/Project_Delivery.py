from .Classes import *


class Project_Delivery(Base):
    __tablename__ = 'project_delivery'
    __table_args__ = {'extend_existing': True}

    project_id = Column(ForeignKey('project.id'), primary_key=True)
    delivery_id = Column(ForeignKey('delivery.id'), primary_key=True)

    project = relationship('Project', lazy="joined", back_populates='project_deliveries')
    delivery = relationship('Delivery', lazy="joined", back_populates='delivery_projects')
