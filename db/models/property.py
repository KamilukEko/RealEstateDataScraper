from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.models.base import Base

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, autoincrement=True, primary_key=True)

    area = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)

    offers = relationship("Offer", back_populates="property")

