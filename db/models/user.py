from pydantic import BaseModel

# Entidad User
class User(BaseModel):
  id: str | None = None
  username: str
  email: str
  is_disabled: bool

class UserDB(User):
  password: str