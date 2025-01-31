import os
import json
from database import connect
from models import Artist, Album, Song

def import_artist(data):
    # Try to add this document to the collection.
    processed = 0
    for artist_data in data['artists']:
        artist = Artist(**artist_data)
        artist.cascade_save()
        print(f"Added artist: {artist.artist_name}")
        
        # Recursively add this document's id to any document that needs it.
        try:
            # Try to add this item to those reference lists.
            print("Something found")
        
        except Exception as e:
            print("Nothing found")
        
        processed +=1

    return processed

def import_album(data):
    # Try to add this document to the collection.
    processed = 0
    for album_data in data['albums']:
        album = Album(**album_data)
        album.cascade_save()
        print(f"Added album: {album.album_name}")
        
        # Recursively add this document's id to any document that needs this reference.
        try:
            # Try to add this item to those reference lists.
            print("Something found")
        
        except Exception as e:
            print("Nothing found")
        
        processed +=1

    return processed

def import_json_file(file_path):    
    # Counter of documents processed.
    processed = 0

    # Process JSON file
    print(f"\nProcessing {file_path}...")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        # Handle artists data
        if 'artists' in data:
            processed = import_artist(data)
                
        # Handle albums data
        if 'albums' in data:
            processed = import_album(data)
                
        # Handle songs data
        if 'songs' in data:
            for song_data in data['songs']:
                song = Song(**song_data)
                song.save()
                print(f"Added song: {song.song_name}")
                processed += 1
    file.close()
                        
    print(f"\nImport completed successfully! Processed {processed} items.")
