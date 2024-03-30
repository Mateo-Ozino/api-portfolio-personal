import os
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from db.models.user import User
from db.schemas.user import user_schema, userdb_schema
from passlib.context import CryptContext
from db.client import db_client

load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SEED = os.getenv("SEED")
AUTH_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciales de autenticación inválidas",headers={"WWW-Authenticate": "Bearer"})

crypt = CryptContext(schemes=["bcrypt"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
  print(form.username)
  user = user_schema(db_client.users.find_one({"username": form.username}))
  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
  
  user_db = search_user_db("username", form.username)
  if not crypt.verify(form.password, user_db["password"]):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
  
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
  
  access_token = {"username": user["username"], "exp": expire}
  
  return {"access_token": jwt.encode(access_token, SEED, algorithm=ALGORITHM), "token_type":"bearer"}

async def auth_user(token: str = Depends(oauth2)):  
  try:
    username = jwt.decode(token, SEED, algorithms=[ALGORITHM]).get("username")
    if username is None:
      raise AUTH_EXCEPTION
    return search_user("username", username)
  except JWTError:
    raise AUTH_EXCEPTION

@router.get("/me")
async def get_user(user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  return user

def search_user(field: str, key):
  try:
    user = db_client.users.find_one({field: key})
    return user_schema(user)
  except:
    return "Usuario no encontrado"

def search_user_db(field: str, key):
  try:
    user = db_client.users.find_one({field: key})
    return userdb_schema(user)
  except:
    return "Usuario no encontrado"