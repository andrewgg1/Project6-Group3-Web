from mongoengine import Document, StringField, IntField, ReferenceField, ListField, PULL

class Album(Document):
    album_name = StringField(required=True)
    release_year = IntField(default=2020)
    genre = StringField(default='rock')
    song_listing = ListField(ReferenceField('Song'), required=True, default=list, reverse_delete_rule=PULL)
    artists = ListField(ReferenceField('Artist'), default=list, reverse_delete_rule=PULL)
    meta = {
        'collection': 'albums'
    }

# For many to many ListFields checkout 2.3.3.5:
# https://docs.mongoengine.org/guide/defining-documents.html#fields

# To make faster queries we can include an index in the meta dictionary
# https://docs.mongoengine.org/guide/defining-documents.html#indexes