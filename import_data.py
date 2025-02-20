import os
import json
from database import *
from models import Song 

def import_data():
    try:
        print('------------ BEGIN TEST DATA IMPORT ------------')
        Song.drop_collection()  # Clears old data

        data_dir = 'test_data'
        processed = 0

        if not os.path.exists(data_dir):
            print(f"Creating {data_dir} directory...")
            os.makedirs(data_dir)
            return

        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                print(f"\nProcessing {filename}...")

                with open(file_path, 'r') as file:
                    data = json.load(file)

                    if 'songs' in data:
                        for song_data in data['songs']:
                            # Remove '_id' field if present
                            song_data.pop('_id', None)
                            song = Song(**song_data)
                            song.save()
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