from mongoengine import Document, StringField, IntField, ReferenceField, ListField, PULL, CASCADE

class Song(Document):
    pass
class Album(Document):
    pass

class Artist(Document):
    artist_name = StringField(required=True)
    country_of_origin = StringField()
    age = IntField(default=35)
    genres = ListField(StringField(), default=list)
    label = StringField()
    songs_credited = ListField(ReferenceField(Song), 
                               default=list, 
                               reverse_delete_rule=CASCADE)
    albums_credited = ListField(ReferenceField(Album), 
                                default=list, 
                                reverse_delete_rule=CASCADE)
    meta = {
        'collection': 'artists'
    }

class Album(Document):
    album_name = StringField(required=True)
    release_year = IntField(default=2020)
    genre = StringField(default='rock') 
    song_listing = ListField(ReferenceField(Song), 
                             required=True, 
                             default=list, 
                             reverse_delete_rule=PULL)
    artists = ListField(ReferenceField(Artist), 
                        default=list, 
                        reverse_delete_rule=PULL)
    meta = {
        'collection': 'albums'
    }

class Song(Document):
    song_name = StringField(required=True)
    song_length = IntField(default=0)
    artists = ListField(ReferenceField(Artist), 
                        required= True, 
                        default=list, 
                        reverse_delete_rule=PULL)
    albums = ListField(ReferenceField(Album), 
                       default=list, 
                       reverse_delete_rule=PULL)
    meta = {
        'collection': 'songs'
    }
