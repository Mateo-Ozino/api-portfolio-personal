from pydantic import BaseModel

class Project(BaseModel):
  id: str | None = None
  name: dict
  description: dict
  logo: str
  url: str
  is_deployed: bool