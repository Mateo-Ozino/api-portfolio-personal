from pydantic import BaseModel

class Tech(BaseModel):
  id: str | None = None
  name: str
