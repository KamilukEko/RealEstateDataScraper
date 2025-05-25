from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, autoincrement=True, primary_key=True)
    updates = relationship("OfferUpdate", back_populates="offer")
    inner_id = Column(String, nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    property = relationship("Property", back_populates="offers")
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    offer_date = Column(DateTime, nullable=False)
    offeror_id = Column(Integer, ForeignKey('offerors.id'), nullable=False)
    offeror = relationship("Offeror", back_populates="offers")
