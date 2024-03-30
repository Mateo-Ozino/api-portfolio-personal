def user_schema(user) -> dict:
  return {"id": str(user["_id"]),
          "username": user["username"],
          "email": user["email"],
          "is_disabled": user["is_disabled"]}

def userdb_schema(user) -> dict:
  return {"id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "is_disabled": user["is_disabled"]}

def users_schema(users) -> list:
  return [user_schema(user) for user in users]