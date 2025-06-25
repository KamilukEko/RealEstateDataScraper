from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.models.base import Base

class Offeror(Base):
    __tablename__ = 'offerors'
    id = Column(Integer, autoincrement=True, primary_key=True)

    source = Column(String, nullable=False)
    inner_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_agency = Column(Boolean, nullable=False)

    offers = relationship("Offer", back_populates="offeror")




