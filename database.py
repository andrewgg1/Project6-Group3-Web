from mongoengine import connect

print("DEBUG: database.py is being executed...")

connect(db='music-library', host='mongo', port=27017, alias='default')
print("DEBUG: Default connection created!")