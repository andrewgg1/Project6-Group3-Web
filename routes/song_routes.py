from flask import Blueprint, request, jsonify, redirect, url_for
from models import Song
from bson import ObjectId, errors as bson_errors
from mongoengine.errors import ValidationError, DoesNotExist
import json

song_bp = Blueprint('song', __name__)

@song_bp.route("/songs", methods=["GET"])
def get_songs():
    """Endpoint for getting all songs with optimized DB calls."""
    try:
        search_term = request.args.get('search')
        # Limit to only needed fields
        fields = ('song_name', 'artist', 'album', 'song_length', 'genre', 'release_year')
        if search_term:
            year_search = int(search_term) if search_term.isdigit() else None
            songs_qs = Song.objects.filter(
                __raw__={
                    "$or": [
                        {"song_name": {"$regex": search_term, "$options": "i"}},
                        {"artist": {"$regex": search_term, "$options": "i"}},
                        {"album": {"$regex": search_term, "$options": "i"}},
                        {"genre": {"$regex": search_term, "$options": "i"}},
                        {"release_year": year_search}
                    ]
                }
            ).only(*fields)
        else:
            songs_qs = Song.objects.only(*fields)

        songs_output = [{
            "song_name": song.song_name,
            "artist": song.artist,
            "album": song.album,
            "song_length": song.song_length,
            "genre": song.genre,
            "release_year": song.release_year,
            "id": str(song.id)
        } for song in songs_qs]

        return jsonify(songs_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<ID>", methods=["GET"])
def get_song(ID):
    """Endpoint for getting a single song with optimized DB call."""
    try:
        fields = ('song_name', 'artist', 'album', 'song_length', 'genre', 'release_year')
        song = Song.objects.only(*fields).get(id=ObjectId(ID))
        return jsonify({
            "song_name": song.song_name,
            "artist": song.artist,
            "album": song.album,
            "song_length": song.song_length,
            "genre": song.genre,
            "release_year": song.release_year,
            "id": str(song.id)
        }), 200
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Song not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs", methods=["POST"])
def create_song():
    """Endpoint for creating a song with efficient JSON handling."""
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
            song = Song(**data).save()
            return jsonify({
                "song_name": song.song_name,
                "artist": song.artist,
                "album": song.album,
                "song_length": song.song_length,
                "genre": song.genre,
                "release_year": song.release_year,
                "id": str(song.id)
            }), 201
        elif request.content_type == 'application/x-www-form-urlencoded':
            song_data = form_to_json(request.form)
            Song(**song_data).save()
            return redirect(url_for('home'))
        else:
            return jsonify({"error": "Invalid request type"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/del-song/<id>", methods=["DELETE", "POST"])
def delete_song(id):
    """Endpoint for deleting a song with efficient retrieval."""
    try:
        song = Song.objects.get(id=ObjectId(id))
        song.delete()
        if request.content_type == 'application/json':
            return jsonify({"message": "Song deleted successfully"}), 200
        elif request.content_type == 'application/x-www-form-urlencoded':
            return redirect(url_for('home'))
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Song not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<id>", methods=["POST", "PUT", "PATCH"])
def edit_song(id):
    """Endpoint for editing a song with efficient JSON handling."""
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type == 'application/x-www-form-urlencoded':
            data = form_to_json(request.form)
        else:
            return jsonify({"error": "Invalid request type"}), 400

        song = Song.objects.get(id=ObjectId(id))
        song.modify(**data)
        return jsonify({
            "song_name": song.song_name,
            "artist": song.artist,
            "album": song.album,
            "song_length": song.song_length,
            "genre": song.genre,
            "release_year": song.release_year,
            "id": str(song.id)
        }), 201
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Song not found"}), 404
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
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
