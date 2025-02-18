from flask import Flask, jsonify
import database
# from routes.artist_routes import artist_bp, get_artist
from routes.song_routes import song_bp, get_songs, get_song
# from routes.album_routes import album_bp
#for my html pages
from flask import Flask, render_template
from models import Artist

app = Flask(__name__)
app.url_map.strict_slashes = False
# app.register_blueprint(artist_bp)
app.register_blueprint(song_bp)
# app.register_blueprint(album_bp)

#do something about options
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

#root route to homepage
@app.route('/', methods=['GET'])
def home():
    song_list = get_songs()[0].json
    return render_template('home.html', song_list=song_list) #sends list of songs to home.html

#edit song
@app.route('/edit/<ID>', methods=['GET'])
def Edit_Song(ID): 
    song = get_song(ID)[0].json #get specific song and send to editSong.html
    return render_template('editSong.html', song=song)

#add/create a song
@app.route('/add-song', methods=['GET'])
def Add_Song():
    return render_template('addSong.html')


if __name__ == "__main__":
    app.run()
