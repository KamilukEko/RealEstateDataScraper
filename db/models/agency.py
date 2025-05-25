from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.models.base import Base

class Agency(Base):
    __tablename__ = 'agencies'
    id = Column(Integer, autoincrement=True, primary_key=True)

    source = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    agents = relationship("Offeror", back_populates="agency")

