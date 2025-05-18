from pydantic import BaseModel, ConfigDict
from typing import Optional

class PropertySchema(BaseModel):
    id: int
    address: Optional[str] = None
    city: str
    price: Optional[float] = None
    area: float
    url: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)