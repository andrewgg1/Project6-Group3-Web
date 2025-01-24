from flask import Blueprint, request, jsonify
from models import Artist
from bson import ObjectId, errors as bson_errors
from mongoengine.errors import ValidationError, DoesNotExist
import json

artist_bp = Blueprint('artist', __name__)

@artist_bp.route("/artists", methods=["GET"])
def get_artists():
    """ Endpoint for getting all artists """
    try:
        all_artists = Artist.objects
        artists_output = [{
            "artist_name": artist.artist_name,
            "country_of_origin": artist.country_of_origin,
            "age": artist.age,
            "genres": artist.genres,
            "label": artist.label,
            "id": str(artist.id)
        } for artist in all_artists]
        return jsonify(artists_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@artist_bp.route("/artists/<ID>", methods=["GET"])
def get_artist(ID):
    """ Endpoint for getting a single artist """
    try:
        artist = Artist.objects(id=ObjectId(ID)).first()
        if not artist:
            return jsonify({"error": "Artist not found"}), 404
        return jsonify({
            "artist_name": artist.artist_name,
            "country_of_origin": artist.country_of_origin,
            "age": artist.age,
            "genres": artist.genres,
            "label": artist.label,
            "id": str(artist.id)
        }), 200
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Artist not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@artist_bp.route("/artists", methods=["POST"])
def create_artist():
    """ Endpoint for creating artist """
    try:
        data = json.loads(request.data)
        artist = Artist(**data).save()
        return jsonify({
            "artist_name": artist.artist_name,
            "country_of_origin": artist.country_of_origin,
            "age": artist.age,
            "genres": artist.genres,
            "label": artist.label,
            "id": str(artist.id)
        }), 201
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@artist_bp.route("/artists/<id>", methods=["DELETE"])
def delete_artist(id):
    """ Endpoint for deleting an artist """
    try:
        artist = Artist.objects(id=ObjectId(id)).first()
        if not artist:
            return jsonify({"error": "Artist not found"}), 404
        artist.delete()
        return jsonify({"message": "Artist deleted successfully"}), 200
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except DoesNotExist:
        return jsonify({"error": "Artist not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@artist_bp.route("/artists/<id>", methods=["PATCH"])
def edit_artist(id):
    """ Endpoint for editing an artist """
    try:
        # reads the json from the request into a data collection obj
        data = json.loads(request.data)

        # Find the document that matches the id in that data collection obj
        artist = Artist.objects(id=ObjectId(id)).first()

        # Update it using the modify command call and pass it the json request object.
        artist.modify(**data)
        
        return jsonify({
            "artist_name": artist.artist_name,
            "country_of_origin": artist.country_of_origin,
            "age": artist.age,
            "genres": artist.genres,
            "label": artist.label,
            "id": str(artist.id)
        }), 201
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500