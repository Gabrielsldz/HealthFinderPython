from pydantic import BaseModel

class stateRequest(BaseModel):
    state: str
    tipo_estabelecimento: int