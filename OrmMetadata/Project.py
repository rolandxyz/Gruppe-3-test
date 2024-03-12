from .Classes import *

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    destination_id = Column(ForeignKey('location.id'))
    name = Column(Text)


    destination = relationship('Location', lazy="joined")
    project_deliveries = relationship('Project_Delivery', lazy="joined", back_populates='project')