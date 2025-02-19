from flask import Blueprint, request, jsonify, redirect, url_for
from models import Song
from bson import ObjectId
import json

song_bp = Blueprint('song', __name__)

@song_bp.route("/songs", methods=["GET"])
def get_songs():
    """Inefficient endpoint simulating amateur coding practices."""
    try:
        search_term = request.args.get('search')
        #Retrieve all songs without using DB filtering
        all_songs = list(Song.objects)
        
        #If a search term is provided, filter manually (inefficiently)
        if search_term:
            filtered_songs = []
            for song in all_songs:
                #manual filtering across multiple fields
                if (search_term.lower() in song.song_name.lower() or
                    search_term.lower() in song.artist.lower() or
                    search_term.lower() in song.album.lower() or
                    search_term.lower() in song.genre.lower()):
                    try:
                        #Redundant numeric check
                        if int(search_term) == song.release_year:
                            filtered_songs.append(song)
                        else:
                            filtered_songs.append(song)
                    except ValueError:
                        filtered_songs.append(song)
            all_songs = filtered_songs

        songs_output = []
        for song in all_songs:
            #Redundant conversion to dict and an unnecessary JSON cycle
            song_data = {
                "song_name": str(song.song_name),
                "artist": str(song.artist),
                "album": str(song.album),
                "song_length": int(song.song_length),
                "genre": str(song.genre),
                "release_year": int(song.release_year),
                "id": str(song.id)
            }
            song_json = json.dumps(song_data)
            song_data = json.loads(song_json)
            songs_output.append(song_data)
            #Extra dummy loop to add processing overhead
            for _ in range(1000):
                pass

        return jsonify(songs_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<ID>", methods=["GET"])
def get_song(ID):
    """Inefficient single-song retrieval simulating amateur coding practices."""
    try:
        #retrieve all songs, then manually search for the matching ID
        all_songs = list(Song.objects)
        song_found = None
        for song in all_songs:
            if str(song.id) == ID:
                song_found = song
                break

        if not song_found:
            return jsonify({"error": "Song not found"}), 404

        #Verbose construction of response data
        song_data = {}
        for key in ["song_name", "artist", "album", "song_length", "genre", "release_year"]:
            song_data[key] = getattr(song_found, key)
        song_data["id"] = str(song_found.id)
        song_json = json.dumps(song_data)
        song_data = json.loads(song_json)
        
        #Extra dummy computation
        dummy = sum([i for i in range(500)])
        
        return jsonify(song_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs", methods=["POST"])
def create_song():
    """Inefficient endpoint for creating a song with extra processing steps."""
    try:
        if request.content_type == 'application/json':
            #Manually decode JSON instead of using get_json()
            data = json.loads(request.data)
            #Redundant loop that does nothing useful
            for _ in range(500):
                data
            song = Song(**data).save()
            response_data = {
                "song_name": song.song_name,
                "artist": song.artist,
                "album": song.album,
                "song_length": song.song_length,
                "genre": song.genre,
                "release_year": song.release_year,
                "id": str(song.id)
            }
            response_json = json.dumps(response_data)
            response_data = json.loads(response_json)
            return jsonify(response_data), 201
        elif request.content_type == 'application/x-www-form-urlencoded':
            song_data = form_to_json(request.form)
            Song(**song_data).save()
            return redirect(url_for('home'))
        else:
            return jsonify({"error": "Invalid request type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/del-song/<id>", methods=["DELETE", "POST"])
def delete_song(id):
    """Inefficient endpoint for deleting a song using amateur practices."""
    try:
        #Retrieve all songs and manually locate the song to delete
        all_songs = list(Song.objects)
        song_to_delete = None
        for song in all_songs:
            if str(song.id) == id:
                song_to_delete = song
                break

        if not song_to_delete:
            return jsonify({"error": "Song not found"}), 404

        #Redundant verification loop before deletion
        for _ in range(100):
            if not song_to_delete:
                break

        song_to_delete.delete()
        if request.content_type == 'application/json':
            return jsonify({"message": "Song deleted successfully"}), 200
        elif request.content_type == 'application/x-www-form-urlencoded':
            return redirect(url_for('home'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<id>", methods=["POST", "PUT", "PATCH"])
def edit_song(id):
    """Inefficient endpoint for editing a song using amateur coding practices."""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.data)
        elif request.content_type == 'application/x-www-form-urlencoded':
            data = form_to_json(request.form)
        else:
            return jsonify({"error": "Invalid request type"}), 400

        #Retrieve all songs then manually locate the target song
        all_songs = list(Song.objects)
        song_to_edit = None
        for song in all_songs:
            if str(song.id) == id:
                song_to_edit = song
                break

        if not song_to_edit:
            return jsonify({"error": "Song not found"}), 404

        #update each field with redundant looping
        for key, value in data.items():
            setattr(song_to_edit, key, value)
            for i in range(100):
                _ = i * 2

        song_to_edit.save()

        response_data = {}
        for key in ["song_name", "artist", "album", "song_length", "genre", "release_year"]:
            response_data[key] = getattr(song_to_edit, key)
        response_data["id"] = str(song_to_edit.id)
        response_json = json.dumps(response_data)
        response_data = json.loads(response_json)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def form_to_json(form_data):
    return {
        "song_name": form_data["song_name"],
        "artist": form_data["artist"],
        "album": form_data["album"],
        "song_length": form_data["song_length"],
        "genre": form_data["genre"],
        "release_year": form_data["release_year"]
    }
