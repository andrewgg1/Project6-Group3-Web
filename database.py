import os
from mongoengine import connect

print("DEBUG: database.py is being executed...")

environment = os.environ.get('ENVIRONMENT', 'local')  # Default to 'local' if not set
mongo_host =  'mongo' if environment == 'docker' else 'localhost'

print(f'ENVIRONMENT IS {environment}')
db = connect(db='music-library', host=mongo_host, port=27017, alias='default')

print("DEBUG: Default connection created!")