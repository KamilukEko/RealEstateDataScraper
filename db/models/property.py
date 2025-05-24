from sqlalchemy import Column, Integer, String, Float, DateTime
from db.models.base import Base

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, autoincrement=True, primary_key=True)
    inner_id = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    contact = Column(String, nullable=True)
    upload_date = Column(DateTime, nullable=False)
    modification_date = Column(DateTime, nullable=False)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    area = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

