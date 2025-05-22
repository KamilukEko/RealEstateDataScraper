from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

class PropertySchema(BaseModel):
    id: Optional[int] = None
    inner_id: str
    url: str
    source: str
    upload_date: Optional[datetime] = datetime.now()
    modification_date: Optional[datetime] = datetime.now()
    city: str
    address: Optional[str] = None
    price: Optional[float] = None
    area: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)