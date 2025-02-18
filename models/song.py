from mongoengine import Document, StringField, IntField, ListField, ReferenceField

class Song(Document):
    song_name = StringField(required=True)
    artist = StringField()
    album = StringField()
    song_length = IntField()
    genre = StringField()
    release_year = IntField()
    meta = {
        'collection': 'songs'
    }