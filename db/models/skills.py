from pydantic import BaseModel

class Skill(BaseModel):
  id: str | None = None
  name: str
  level: int

class SkillOptional(Skill):
  name: str | None = None
  level: int | None = None