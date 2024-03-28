def project_schema(project) -> dict:
  return {"id": str(project["_id"]),
          "name": project["name"],
          "description": project["description"],
          "logo": project["logo"],
          "url": project["url"],
          "is_deployed": project["is_deployed"]}

def projects_schema(projects) -> list:
  return [project_schema(project) for project in projects]