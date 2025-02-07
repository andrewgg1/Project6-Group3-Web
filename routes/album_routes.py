from flask import Blueprint, request, jsonify
from models import Album
from bson import ObjectId, errors as bson_errors
from mongoengine.errors import ValidationError, DoesNotExist
import json

album_bp = Blueprint('album', __name__)

@album_bp.route("/albums", methods=["GET"])
def get_albums():
    """ Endpoint for getting all albums """
    try:
        all_albums = Album.objects
        albums_output = [{
            "album_name": album.album_name,
            "release_year": album.release_year,
            "genre": album.genre,
            "id": str(album.id)
        } for album in all_albums]
        return jsonify(albums_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@album_bp.route("/albums/<ID>", methods=["GET"])
def get_album(ID):
    """ Endpoint for getting a single album """
    try:
        album = Album.objects(id=ObjectId(ID)).first()
        if not album:
            return jsonify({"error": "Album not found"}), 404
        return jsonify({
            "album_name": album.album_name,
            "release_year": album.release_year,
            "genre": album.genre,
            "id": str(album.id)
        }), 200
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Album not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@album_bp.route("/albums", methods=["POST"])
def create_album():
    """ Endpoint for creating album """
    try:
        data = json.loads(request.data)
        album = Album(**data).save()
        return jsonify({
            "album_name": album.album_name,
            "release_year": album.release_year,
            "genre": album.genre,
            "id": str(album.id)
        }), 201
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@album_bp.route("/albums/<id>", methods=["DELETE"])
def delete_album(id):
    """ Endpoint for deleting an album """
    from models.song import Song

    try:
        album = Album.objects(id=ObjectId(id)).first()
        if not album:
            return jsonify({"error": "Album not found"}), 404
        
        #remove album from any songs that reference it
        songs_with_album = Song.objects(albums=album)
        for song in songs_with_album:
            #pull album out of the song's albums list
            song.update(pull__albums=album)
            #fetch song, to see updated list
            updated_song = Song.objects(id=song.id).first()
            #if no more albums in that song's list, delete the song
            if not updated_song.albums:
                updated_song.delete()

        #delete the album
        album.delete()
        return jsonify({"message": f"Album '{album.album_name}' deleted. Songs with no remaining albums also removed."}), 200

    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Album not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@album_bp.route("/albums/<id>", methods=["PATCH"])
def edit_album(id):
    """ Endpoint for editing an album """
    try:
        # reads the json from the request into a data collection obj
        data = json.loads(request.data)

        # Find the document that matches the id in that data collection obj
        album = Album.objects(id=ObjectId(id)).first()

        # Update it using the modify command call and pass it the json request object.
        album.modify(**data)

        return jsonify({
            "album_name": album.album_name,
            "release_year": album.release_year,
            "genre": album.genre,
            "id": str(album.id)
        }), 201
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For put need to use modify instead of update