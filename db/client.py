# COMANDO PARA INICIAR UNA INSTANCIA DE MONGO EN LOCAL (CORRER EN CMD COMO ADMIN)
# "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="c:\data\db"
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

#DB LOCAL
#db_client = MongoClient().local

# DB REMOTA
URI = os.getenv("MONGO_URL")
db_client = MongoClient(URI, server_api=ServerApi('1')).portfolio
