from .Classes import *

class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    departure_id = Column(ForeignKey('location.id'))
    status_id = Column(ForeignKey('status.id'))
    arrival_date = Column(Date)

    departure = relationship('Location', lazy="joined")
    status = relationship('Status', lazy="joined")
    delivery_projects = relationship('Project_Delivery', lazy="joined", back_populates='delivery')