from mongoengine import Document, StringField, IntField, ListField, ReferenceField

class Artist(Document):
    artist_name = StringField(required=True)
    country_of_origin = StringField()
    # songs_credited = ListField(ReferenceField('Song'), default=list)
    # albums_credited = ListField(ReferenceField('Album'), default=list)
    age = IntField(default=35)
    genre = StringField()
    label = StringField()
    meta = {
        'collection': 'artists'
    }