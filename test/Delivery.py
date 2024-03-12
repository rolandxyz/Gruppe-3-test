from .initialize_db import *

class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    departure_id = Column(ForeignKey('location.id'))
    status_id = Column(ForeignKey('status.id'))
    arrival_date = Column(Text)

    departure = relationship('Location')
    status = relationship('Status')
    projects = relationship('Project', secondary='project_delivery', back_populates='deliveries')