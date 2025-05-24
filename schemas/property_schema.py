from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

class PropertySchema(BaseModel):
    id: Optional[int] = None
    inner_id: str
    url: str
    source: str
    contact: Optional[str] = None
    upload_date: Optional[datetime] = datetime.now()
    modification_date: Optional[datetime] = datetime.now()
    city: Optional[str] = None
    address: Optional[str] = None
    price: Optional[float] = None
    area: float
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)