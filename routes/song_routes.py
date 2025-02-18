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
        song = Song(
            song_name = request.form['song_name'],
            song_length = request.form['song_length']
        ).save()

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

# I changed the app.route from "/songs/<ID>" because it caused conflicts 
# with the edit_song(id) app.route
# I also added a POST method bc that was the only way i could think of to
# directly call the delete_song(id) function without making a new html page & 
# ultimately a new function in app.py
@song_bp.route("/del-song/<id>", methods=["DELETE", "POST"])
def delete_song(id):
    """ Endpoint for deleting a song """
    try:
        if request.method == "POST": #checks for POST method
            song = Song.objects(id=ObjectId(id)).first()
        elif request.method == "DELETE": #relevant mostly for jmeter tests, which means to trigger this function, you can call the DELETE method directly
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

# I added a POST method bc the html <form> tag from editSong.html only works with POST and GET methods
@song_bp.route("/songs/<id>", methods=["POST", "PATCH"])
def edit_song(id):
    """ Endpoint for editing a song """
    try:
        # reads the json from the request into a data collection obj
        if request.method == 'POST': #checks for POST method
            data = form_to_json(request.form) #turns <form> data to json
        elif request.method == 'PATCH': #relevant mostly for jmeter tests, which means to trigger this function, you can call the PATCH method directly
            data = json.loads(request.data)

        # Find the document that matches the id in that data collection obj
        song = Song.objects(id=ObjectId(id)).first()

        if not song:
            return jsonify({"error": "Song not found"}), 404
        
        # Update it using the modify command call and pass it the json request object.
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

#turns <form> data to json dictionary
def form_to_json(form_data):
    return {
        "song_name": form_data["song_name"],
        # "artist": form_data["artist"],
        # "album": form_data["album"],
        "song_length": form_data["song_length"]
        # "genre": form_data["genre"],
        # "release_year": form_data["release_year"]
    }