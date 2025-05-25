from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

class OfferDataSchema(BaseModel):
    id: Optional[int] = None
    inner_id: str
    url: str
    source: str
    offeror_name: Optional[str] = None
    offeror_id: Optional[str] = None
    offeror_phone: Optional[str] = None
    agency_name: Optional[str] = None
    agency_email: Optional[str] = None
    agency_phone: Optional[str] = None
    upload_date: Optional[datetime] = datetime.now()
    modification_date: Optional[datetime] = datetime.now()
    city: Optional[str] = None
    address: Optional[str] = None
    price: Optional[float] = None
    area: float
    floor: Optional[float] = None
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)