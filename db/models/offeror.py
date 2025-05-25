from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base

class Offeror(Base):
    __tablename__ = 'offerors'
    id = Column(Integer, autoincrement=True, primary_key=True)

    source = Column(String, nullable=False)
    inner_id = Column(String, nullable=True)
    name = Column(String, nullable=True)

    agency_id = Column(Integer, ForeignKey('agencies.id'), nullable=True)
    phone = Column(String, nullable=True)

    offers = relationship("Offer", back_populates="offeror")
    agency = relationship("Agency", back_populates="agents")



