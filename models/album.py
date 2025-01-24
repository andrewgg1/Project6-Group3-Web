from mongoengine import Document, StringField, IntField, ReferenceField, ListField

class Album(Document):
    album_name = StringField(required=True)
    # artists = ListField(ReferenceField('Artist'), default=list)
    release_year = IntField(default=2020)
    # song_listing = ListField(ReferenceField('Song'), default=list)
    genre = StringField(default='rock')
    meta = {
        'collection': 'albums'
    }