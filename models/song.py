from mongoengine import Document, StringField, IntField, ReferenceField

class Song(Document):
    song_name = StringField(required=True)
    # artists = ListField(ReferenceField('Artist'), default=list)
    # albums = ListField(ReferenceField('Album'), default=list)
    song_length = IntField(default=0)
    meta = {
        'collection': 'songs'
    }