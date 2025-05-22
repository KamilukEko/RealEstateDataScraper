from sqlalchemy import Column, Integer, String, Float, DateTime
from db.models.base import Base

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, autoincrement=True, primary_key=True)
    inner_id = Column(String, nullable=True)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    modification_date = Column(DateTime, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    area = Column(Float, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

