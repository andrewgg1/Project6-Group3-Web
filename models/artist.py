from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentListField

class Song(EmbeddedDocument):
    song_name = StringField(required=True)
    song_length = IntField()
    genre = StringField()

class Album(EmbeddedDocument):
    album_name = StringField(required=True)
    release_year = IntField()
    genre = StringField()
    songs = EmbeddedDocumentListField(Song, default=list)

class Artist(Document):
    artist_name = StringField(required=True)
    country_of_origin = StringField()
    age = IntField()
    genres = ListField(StringField(), default=list)
    label = StringField()
    albums = EmbeddedDocumentListField(Album, default=list)
    meta = {
        'collection': 'artists'
    }