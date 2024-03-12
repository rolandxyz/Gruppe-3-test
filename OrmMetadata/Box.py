from .Classes import *

class Box(Base):
    __tablename__ = 'box'

    id = Column(Integer, primary_key=True)
    guid = Column(GUID, default=uuid.uuid4)
    category_id = Column(Integer, ForeignKey('category.id'))
    status_id = Column(Integer, ForeignKey('status.id'))
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    description = Column(Text)

    category = relationship('Category', lazy="joined")
    delivery = relationship('Delivery', lazy="joined")
    status = relationship('Status', lazy="joined")
    ressources = relationship('Ressource', lazy="joined", back_populates='box')
