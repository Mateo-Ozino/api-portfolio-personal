from pydantic import BaseModel

class Project(BaseModel):
  id: str | None = None
  name: dict
  description: dict
  logo: str
  url: str
  is_deployed: bool
  order: int

class ProjectOptional(Project):
  name: dict | None = None
  description: dict | None = None
  logo: str | None = None
  url: str | None = None
  is_deployed: bool | None = None
  order: int | None = None