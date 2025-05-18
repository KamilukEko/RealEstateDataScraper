from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.base import Base

engine = create_engine('sqlite:///real_estate.db')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    import db.models.property
    Base.metadata.create_all(bind=engine)
