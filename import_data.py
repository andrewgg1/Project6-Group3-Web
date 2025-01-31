import os
import json
from database import connect
from models import Artist, Album, Song

def import_data():
    try:
        data_dir = 'test_data'
        processed = 0
        
        # Ensure directory exists
        if not os.path.exists(data_dir):
            print(f"Creating {data_dir} directory...")
            os.makedirs(data_dir)
            return
        
        # Process each JSON file
        for filename in os.listdir(data_dir):
            # if filename.endswith('.json'):
            if filename.find('album_data.json') is not -1:
                file_path = os.path.join(data_dir, filename)
                print(f"\nProcessing {filename}...")
                
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Handle artists data
                    if 'artists' in data:
                        for artist_data in data['artists']:
                            artist = Artist(**artist_data)
                            if artist.save(cascade=True):
                                print(f"Added artist: {artist.artist_name}")
                                processed += 1
                            
                    # Handle albums data
                    if 'albums' in data:
                        for album_data in data['albums']:
                            album = Album(**album_data)
                            if album.save(cascade=True):
                                print(f"Added album: {album.album_name}")
                                processed += 1
                            
                    # Handle songs data
                    if 'songs' in data:
                        for song_data in data['songs']:
                            song = Song(**song_data)
                            if song.save(cascade=True):
                                print(f"Added song: {song.song_name}")
                                processed += 1
                            
        print(f"\nImport completed successfully! Processed {processed} items.")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {filename} - {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    import_data()