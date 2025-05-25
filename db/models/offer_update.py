from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.models.base import Base


class OfferUpdate(Base):
    __tablename__ = 'offers_updates'
    id = Column(Integer, autoincrement=True, primary_key=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), nullable=False)

    update_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=True)

    offer = relationship("Offer", back_populates="updates")

