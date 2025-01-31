from flask import Flask, jsonify
import database
from routes.artist_routes import artist_bp
from routes.song_routes import song_bp
from routes.album_routes import album_bp
#for my html pages
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(artist_bp)
app.register_blueprint(song_bp)
app.register_blueprint(album_bp)

#@app.route('/', methods=['GET', 'OPTIONS'])
def options():
    return jsonify({
        "endpoints": {
            "/": {
                "GET": "Welcome message",
                "OPTIONS": "Get API documentation"
            },
            "/artists": {
                "GET": "Get all artists",
                "POST": {
                    "description": "Create a new artist",
                    "required_fields": ["artist_name"],
                    "optional_fields": ["country_of_origin", "age", "genres", "label"]
                }
            },
            "/artists/<id>": {
                "GET": "Get artist by ID",
                "DELETE": "Delete artist by ID"
            },
            "/albums": {
                "GET": "Get all albums",
                "POST": {
                    "description": "Create a new album",
                    "required_fields": ["album_name"],
                    "optional_fields": ["release_year", "genre"]
                }
            },
            "/albums/<id>": {
                "GET": "Get album by ID",
                "DELETE": "Delete album by ID"
            },
            "/songs": {
                "GET": "Get all songs",
                "POST": {
                    "description": "Create a new song",
                    "required_fields": ["song_name"],
                    "optional_fields": ["song_length"]
                }
            },
            "/songs/<id>": {
                "GET": "Get song by ID",
                "DELETE": "Delete song by ID"
            }
        },
        "status_codes": {
            "200": "Success",
            "201": "Created",
            "400": "Bad Request",
            "404": "Not Found",
            "500": "Server Error"
        }
    }), 200

#just testing my html pages opening
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
if __name__ == "__main__":
    app.run()
