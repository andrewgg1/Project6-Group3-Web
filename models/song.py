from mongoengine import Document, StringField, IntField, ListField, ReferenceField
import yt_dlp

class Song(Document):
    song_name = StringField(required=True)
    artist = StringField()
    album = StringField()
    song_length = IntField()
    genre = StringField()
    release_year = IntField()
    youtube_url = StringField(default='')
    youtube_audio_url = StringField(default='')
    youtube_thumbnail = StringField(default='')
    meta = {
        'collection': 'songs'
    }

    # def get_youtube_url(self):
    #     try:
    #         videos = list(scrapetube.get_search(query=f'{self.song_name} by {self.artist}', limit=1, sort_by='relevance'))
    #         if videos:
    #             videoId = videos[0]['videoId']
    #             self.youtube_url = f'https://www.youtube.com/watch?v={videoId}'
    #             self.youtube_thumbnail = f'http://img.youtube.com/vi/{videoId}/maxresdefault.jpg'
    #             return self.youtube_url
    #         else:
    #             return None  # Or handle the case where no video is found
    #     except Exception as e:
    #         print(f"Error fetching YouTube URL: {e}")
    #         return None

    # def save(self, *args, **kwargs):
    #     # Call get_youtube_url to fetch and save the YouTube URL
    #     if not self.youtube_url:
    #         self.get_youtube_url()
    #     super(Song, self).save(*args, **kwargs) # Call the "real" save method


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
                    return
                else:
                    return None
            except Exception as e:
                print(f"Error: {e}")
                return None

    # Example usage:
    # search_query = 'Red Hot Chili Peppers Californication'
    # audio_url, webpage_url, thumbnail_url = get_youtube_info_from_search(search_query)

    def save(self, *args, **kwargs):
        # Call get_youtube_url to fetch and save the YouTube URL
        if not self.youtube_url:
            self.get_youtube_info_from_search()
        super(Song, self).save(*args, **kwargs) # Call the "real" save method