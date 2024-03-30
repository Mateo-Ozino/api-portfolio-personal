from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from pymongo import ReturnDocument
from db.client import db_client
from db.models.user import User
from db.models.techs import Tech
from db.schemas.techs import tech_schema, techs_schema
from routers.login import auth_user

router = APIRouter(prefix="/techs", tags=["techs"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Tech])
async def read_techs():
  techs = db_client.techs.find()
  return techs_schema(techs)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Tech)
async def read_tech(id: str):
  tech = search_tech("_id", ObjectId(id))
  if not tech:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El proyecto no existe")
  
  return tech

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tech(tech: Tech, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

  if type(search_tech("name", tech.name)) == Tech:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El proyecto ya existe")
  
  tech_dict : dict = dict(tech)
  del tech_dict["id"]
  
  tech_id = db_client.techs.insert_one(tech_dict).inserted_id
  
  new_tech = tech_schema(db_client.techs.find_one({"_id": tech_id}))
  
  return Tech(**new_tech)

@router.post("/many", status_code=status.HTTP_201_CREATED)
async def create_multiple_techs(techs: list[dict], user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  techs_list : list[dict] = []
  
  for tech in techs:
    if type(search_tech("name", tech["name"])) == Tech:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Una de las techs ya existe")
    tech_dict = dict(tech)
    del tech_dict["id"]
    techs_list.append(tech_dict)
  
  try:
    db_client.techs.insert_many(techs_list)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error")
  
  new_techs = db_client.techs.find()
  return techs_schema(new_techs)

@router.put("/", response_model=Tech, status_code=status.HTTP_200_OK)
async def total_tech_update(tech: Tech, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  tech_dict = dict(tech)
  del tech_dict["id"]
  
  try:
    db_client.techs.find_one_and_replace({"_id": ObjectId(tech.id)}, tech_dict)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tech no actualizada correctamente")
  
  return search_tech("_id", ObjectId(tech.id))

@router.patch("/{id}", response_model=Tech, status_code=status.HTTP_200_OK)
async def partial_tech_update(id: str, modifications: Tech, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  try:
    db_client.techs.find_one_and_update({"_id": ObjectId(id)}, {'$set': modifications.model_dump(exclude_unset=True)}, return_document=ReturnDocument.AFTER)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tech no actualizada correctamente")
  
  return search_tech("_id", ObjectId(id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tech(id: str, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  try:
    db_client.techs.find_one_and_delete({"_id": ObjectId(id)})
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tech no eliminada correctamente")

def search_tech(field: str, key) -> dict:
  try:
    tech = db_client.techs.find_one({field: key})
    return Tech(**tech_schema(tech))
  except:
    return None