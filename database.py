from pymongo import MongoClient
from mongoengine import connect

client = MongoClient('mongodb://localhost:27017/')
db = client['music-library']
connect('music-library')
