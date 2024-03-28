from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
  id: str | None = None
  name: dict
  description: dict
  logo: str
  url: str
  is_deployed: bool

class ProjectOptional(Project):
  name: dict | None = None
  description: dict | None = None
  logo: str | None = None
  url: str | None = None
  is_deployed: bool | None = None