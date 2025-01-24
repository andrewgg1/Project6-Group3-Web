from mongoengine import Document, StringField, IntField

class Artist(Document):
    name = StringField(required=True)
    age = IntField(default=20)
    genre = StringField(default='Unknown')

class Album(Document):
    name = StringField(required=True)
    artist = StringField(required=True)
    year = IntField(default=2020)

class Song(Document):
    name = StringField(required=True)
    artist = StringField(required=True)
    album = StringField(required=True)
    genre = StringField(default='Unknown')
    year = IntField(default=2020)

