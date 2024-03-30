from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from pymongo import ReturnDocument
from db.client import db_client
from db.models.user import User
from db.models.skills import Skill
from db.schemas.skills import skill_schema, skills_schema
from routers.login import auth_user

router = APIRouter(prefix="/skills", tags=["skills"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Skill])
async def read_skills():
  skills = db_client.skills.find()
  return skills_schema(skills)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Skill)
async def read_skill(id: str):
  skill = search_skill("_id", ObjectId(id))
  if not skill:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La skill ya existe")
  
  return skill

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_skill(skill: Skill, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  if type(search_skill("name", skill.name)) == Skill:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La skill ya existe")
  
  skill_dict : dict = dict(skill)
  del skill_dict["id"]
  
  skill_id = db_client.skills.insert_one(skill_dict).inserted_id
  
  new_skill = skill_schema(db_client.skills.find_one({"_id": skill_id}))
  
  return Skill(**new_skill)

@router.post("/many", status_code=status.HTTP_201_CREATED)
async def create_multiple_skills(skills: list[dict], user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  skills_list : list[dict] = []
  
  for skill in skills:
    if type(search_skill("name", skill["name"])) == Skill:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Una de las skills ya existe")
    skill_dict = dict(skill)
    del skill_dict["id"]
    skills_list.append(skill_dict)
  
  try:
    db_client.skills.insert_many(skills_list)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creando multiples skills")
  
  new_skills = db_client.skills.find()
  return skills_schema(new_skills)

@router.put("/", response_model=Skill, status_code=status.HTTP_200_OK)
async def total_skill_update(skill: Skill, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  
  skill_dict = dict(skill)
  del skill_dict["id"]
  
  try:
    db_client.skills.find_one_and_replace({"_id": ObjectId(skill.id)}, skill_dict)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill no actualizada correctamente")
  
  return search_skill("_id", ObjectId(skill.id))

@router.patch("/{id}", response_model=Skill, status_code=status.HTTP_200_OK)
async def partial_skill_update(id: str, modifications: Skill, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

  try:
    db_client.skills.find_one_and_update({"_id": ObjectId(id)}, {'$set': modifications.model_dump(exclude_unset=True)}, return_document=ReturnDocument.AFTER)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill no actualizada correctamente")
  
  return search_skill("_id", ObjectId(id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(id: str, user: User = Depends(auth_user)):
  if user["is_disabled"]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
  try:
    db_client.skills.find_one_and_delete({"_id": ObjectId(id)})
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill no eliminada correctamente")

def search_skill(field: str, key) -> dict:
  try:
    skill = db_client.skills.find_one({field: key})
    return Skill(**skill_schema(skill))
  except:
    return None