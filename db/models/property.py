from sqlalchemy import Column, Integer, String, Float
from db.models.base import Base

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    area = Column(Float, nullable=False)
    url = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

