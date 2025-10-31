from config import Config
from pymongo import MongoClient


client = MongoClient(Config.MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True)
DB = client['RecordRose']
record_collection = DB['RecordRose']
