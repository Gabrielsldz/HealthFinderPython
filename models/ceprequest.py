from pydantic import BaseModel
from typing import Optional

class CepRequest(BaseModel):
    cep: str
    distance: int
    tipo_estabelecimento: Optional[int]