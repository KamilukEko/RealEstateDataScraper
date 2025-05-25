from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, autoincrement=True, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    offeror_id = Column(Integer, ForeignKey('offerors.id'), nullable=False)
    inner_id = Column(String, nullable=False)

    source = Column(String, nullable=False)
    offer_date = Column(DateTime, nullable=False)
    url = Column(String, nullable=False)

    updates = relationship("OfferUpdate", back_populates="offer")
    property = relationship("Property", back_populates="offers")
    offeror = relationship("Offeror", back_populates="offers")
