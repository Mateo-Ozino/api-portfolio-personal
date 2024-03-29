def skill_schema(skill) -> dict:
  return {"id": str(skill["_id"]),
          "name": skill["name"],
          "level": skill["level"]}

def skills_schema(skills) -> list:
  return [skill_schema(skill) for skill in skills]