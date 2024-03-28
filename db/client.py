# COMANDO PARA INICIAR UNA INSTANCIA DE MONGO (CORRER EN CMD COMO ADMIN)
# "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="c:\data\db"
# fast_api_test pass
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

#DB LOCAL
db_client = MongoClient().local

# #DB REMOTA
# URI = os.getenv("MONGO_URL")
# # Create a new client and connect to the server
# db_client = MongoClient(URI, server_api=ServerApi('1')).test
