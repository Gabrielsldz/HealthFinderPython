from pydantic import BaseModel
from typing import Optional

class nameRequest(BaseModel):
    name: Optional[str] = None