from .Classes import *

class Ressource(Base):
    __tablename__ = 'ressource'

    id = Column(Integer, primary_key=True)
    box_id = Column(Integer, ForeignKey('box.id'))
    guid = Column(GUID, default=uuid.uuid4)
    description = Column(Text)
    material = Column(Text)
    color = Column(Text)
    size = Column(Text)
    gtin = Column(Integer)
    amount_unit = Column(Float)
    unit_id = Column(Integer, ForeignKey('unit.id'))
    amount = Column(Integer)
    expiry_date = Column(Date)
    position = Column(Text)
    status_id = Column(Integer, ForeignKey('status.id'))

    status = relationship('Status', lazy="joined")
    unit = relationship('Unit', lazy="joined")
    box = relationship('Box', lazy="joined", back_populates='ressources')