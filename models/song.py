from mongoengine import Document, StringField, IntField, ListField, ReferenceField
import yt_dlp

class Song(Document):
    song_name = StringField(required=True)
    artist = StringField()
    album = StringField()
    song_length = IntField(default=60)
    genre = StringField()
    release_year = IntField(default=2015)
    youtube_url = StringField(default='')
    youtube_audio_url = StringField(default='')
    youtube_thumbnail = StringField(default='static/images/music-note-96.png')
    meta = {
        'collection': 'songs'
    }

    def get_youtube_info_from_search(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'default_search': 'ytsearch'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(f'ytsearch:{self.artist} {self.song_name}', download=False)
                if info_dict and 'entries' in info_dict and len(info_dict['entries']) > 0:
                    first_entry = info_dict['entries'][0]
                    self.youtube_audio_url = first_entry.get('url')
                    self.youtube_url = first_entry.get('webpage_url') or f"https://www.youtube.com/watch?v={first_entry.get('id')}" # Construct URL if missing
                    self.youtube_thumbnail = first_entry.get('thumbnail')
                    self.save()
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Error: {e}")
                return False

    def save(self, *args, **kwargs):
        return super(Song, self).save(*args, **kwargs)