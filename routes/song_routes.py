from flask import Blueprint, request, jsonify
from models import Song
from bson import ObjectId, errors as bson_errors
from mongoengine.errors import ValidationError, DoesNotExist
import json

song_bp = Blueprint('song', __name__)

@song_bp.route("/songs", methods=["GET"])
def get_songs():
    """ Endpoint for getting all songs """
    try:
        all_songs = Song.objects
        songs_output = [{
            "song_name": song.song_name,
            "song_length": song.song_length,
            "id": str(song.id)
        } for song in all_songs]
        return jsonify(songs_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<ID>", methods=["GET"])
def get_song(ID):
    """ Endpoint for getting a single song """
    try:
        song = Song.objects(id=ObjectId(ID)).first()
        if not song:
            return jsonify({"error": "Song not found"}), 404
        return jsonify({
            "song_name": song.song_name,
            "song_length": song.song_length,
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
    """ Endpoint for creating song """
    try:
        data = json.loads(request.data)
        song = Song(**data).save()
        return jsonify({
            "song_name": song.song_name,
            "song_length": song.song_length,
            "id": str(song.id)
        }), 201
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<id>", methods=["DELETE"])
def delete_song(id):
    """ Endpoint for deleting a song """
    try:
        song = Song.objects(id=ObjectId(id)).first()
        if not song:
            return jsonify({"error": "Song not found"}), 404
        song.delete()
        return jsonify({"message": "Song deleted successfully"}), 200
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Song not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@song_bp.route("/songs/<id>", methods=["PATCH"])
def edit_song(id):
    """ Endpoint for editing a song """
    try:
        # reads the json from the request into a data collection obj
        data = json.loads(request.data)

        # Find the document that matches the id in that data collection obj
        song = Song.objects(id=ObjectId(id)).first()

        # Modify it using the update command call and pass it the json request object.
        song.modify(**data)
        
        return jsonify({
            "song_name": song.song_name,
            "song_length": song.song_length,
            "id": str(song.id)
        }), 201
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500