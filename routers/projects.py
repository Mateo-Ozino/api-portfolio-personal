from fastapi import APIRouter, HTTPException, status
from db.models.projects import Project
from db.schemas.projects import project_schema, projects_schema

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", status_code=status.HTTP_200_OK)
async def read_projects():
  pass