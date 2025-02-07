from flask import Flask, jsonify
import database
from routes.artist_routes import artist_bp
from routes.song_routes import song_bp
from routes.album_routes import album_bp
#for my html pages
from flask import Flask, render_template
from models import Artist

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(artist_bp)
app.register_blueprint(song_bp)
app.register_blueprint(album_bp)

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
    artists = Artist.objects() #reads from database
    return render_template('home.html', artists=artists) #sends list of artists to home.html

#these are the 'add' routes that return a html page with a form for the user to fill
#idk if these should be moved to the routes folder to their appropriate files
@app.route('/add-artist', methods=['GET'])
def Add_Artist(): #only this one has a button to trigger it on home.html
    return render_template('artist.html')

@app.route('/add-album', methods=['GET'])
def Add_Album(): #trigger in profile.html
    return render_template('album.html')

@app.route('/add-song', methods=['GET'])
def Add_Song(): #trigger in profile.html
    return render_template('song.html')

#To be deleted - for testing purposes
@app.route('/profile', methods=['GET'])
def Get_profile():
    return render_template('profile.html') #place this in route/artist_route.py instead (/artists/<ID> GET aka get_artist(ID))

if __name__ == "__main__":
    app.run()
