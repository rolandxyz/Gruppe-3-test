from .Classes import *

class Content(Base):
    __tablename__ = 'content'

    box_guid = Column(ForeignKey('box.guid'), primary_key=True)
    ressource_guid = Column(ForeignKey('ressource.guid'), primary_key=True)
    current_amount = Column(Integer)
    sent_amount = Column(Integer)

    box = relationship('Box', lazy="joined")
    ressource = relationship('Ressource', lazy="joined")