from .initialize_db import *

class Ressource(Base):
    __tablename__ = 'ressource'

    guid = Column(Integer, primary_key=True)
    unit_id = Column(ForeignKey('unit.id'))
    status_id = Column(ForeignKey('status.id'))
    description = Column(Text)
    material = Column(Text)
    color = Column(Text)
    size = Column(Text)
    expiry_date = Column(Text)
    gtin = Column(Integer)
    amount = Column(Integer)
    position = Column(Text)

    status = relationship('Status')
    unit = relationship('Unit')