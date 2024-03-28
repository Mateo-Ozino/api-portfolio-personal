from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from pymongo import ReturnDocument
from db.client import db_client
from db.models.projects import Project, ProjectOptional
from db.schemas.projects import project_schema, projects_schema

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Project])
async def read_projects():
  projects = db_client.projects.find()
  return projects_schema(projects)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Project)
async def read_project(id: str):
  project = search_project("_id", ObjectId(id))
  if not project:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El proyecto no existe")
  
  return project

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(project: Project):
  if type(search_project("name", project.name)) == Project:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El proyecto ya existe")
  
  project_dict : dict = dict(project)
  del project_dict["id"]
  
  project_id = db_client.projects.insert_one(project_dict).inserted_id
  
  new_project = project_schema(db_client.projects.find_one({"_id": project_id}))
  
  return Project(**new_project)

@router.put("/", response_model=Project, status_code=status.HTTP_200_OK)
async def total_project_update(project: Project):
  project_dict = dict(project)
  del project_dict["id"]
  
  try:
    db_client.projects.find_one_and_replace({"_id": ObjectId(project.id)}, project_dict)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proyecto no actualizado correctamente")
  
  return search_project("_id", ObjectId(project.id))

@router.patch("/{id}", response_model=Project, status_code=status.HTTP_200_OK)
async def partial_project_update(id: str, modifications: ProjectOptional):
  try:
    db_client.projects.find_one_and_update({"_id": ObjectId(id)}, {'$set': modifications.model_dump(exclude_unset=True)}, return_document=ReturnDocument.AFTER)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proyecto no actualizado correctamente")
  
  return search_project("_id", ObjectId(id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: str):
  try:
    found = db_client.projects.find_one_and_delete({"_id": ObjectId(id)})
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proyecto no eliminado correctamente")

def search_project(field: str, key) -> dict:
  try:
    project = db_client.projects.find_one({field: key})
    return Project(**project_schema(project))
  except:
    return None