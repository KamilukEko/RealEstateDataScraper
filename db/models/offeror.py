from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.models.base import Base

class Offeror(Base):
    __tablename__ = 'offerors'
    id = Column(Integer, autoincrement=True, primary_key=True)
    offers = relationship("Offer", back_populates="offeror")
    inner_id = Column(String, nullable=True)
    url = Column(String, nullable=True)
    source = Column(String, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    type = Column(String, nullable=True)