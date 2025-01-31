from mongoengine import Document, StringField, IntField, ReferenceField, ListField, PULL

class Song(Document):
    song_name = StringField(required=True)
    song_length = IntField(default=0)
    artists = ListField(ReferenceField('Artist'), required= True, default=list, reverse_delete_rule=PULL)
    albums = ListField(ReferenceField('Album'), default=list, reverse_delete_rule=PULL)
    meta = {
        'collection': 'songs'
    }