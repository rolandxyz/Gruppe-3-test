from .initialize_db import *

class Box(Base):
    __tablename__ = 'box'

    guid = Column(UUID(as_uuid=True), primary_key=True)
    category_id = Column(ForeignKey('category.id'))
    status_id = Column(ForeignKey('status.id'))
    delivery_id = Column(ForeignKey('delivery.id'))
    number = Column(Integer)
    description = Column(Text)

    category = relationship('Category')
    delivery = relationship('Delivery')
    status = relationship('Status')