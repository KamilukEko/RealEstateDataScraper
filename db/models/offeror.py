from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.models.base import Base

class Offeror(Base):
    __tablename__ = 'offerors'
    id = Column(Integer, autoincrement=True, primary_key=True)

    source = Column(String, nullable=False)
    inner_id = Column(String, nullable=True)
    name = Column(String, nullable=False)

    type = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    offers = relationship("Offer", back_populates="offeror")



