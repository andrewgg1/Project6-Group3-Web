from mongoengine import Document, StringField, IntField, ListField, ReferenceField, CASCADE

class Artist(Document):
    artist_name = StringField(required=True)
    country_of_origin = StringField()
    age = IntField(default=35)
    genres = ListField(StringField(), default=list)
    label = StringField()
    songs_credited = ListField(ReferenceField('Song'), 
                               default=list, 
                               reverse_delete_rule=CASCADE)
    albums_credited = ListField(ReferenceField('Album'), 
                                default=list, 
                                reverse_delete_rule=CASCADE)
    meta = {
        'collection': 'artists'
    }