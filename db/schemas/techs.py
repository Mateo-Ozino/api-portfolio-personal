def tech_schema(tech) -> dict:
  return {"id": str(tech["_id"]),
          "name": tech["name"]}

def techs_schema(techs) -> list:
  return [tech_schema(tech) for tech in techs]