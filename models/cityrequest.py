from pydantic import BaseModel
from typing import Optional

class CityRequest(BaseModel):
    city: str
    tipo_estabelecimento: Optional[int]