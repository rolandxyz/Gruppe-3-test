from .Classes import *

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    is_warehouse = Column(Boolean)