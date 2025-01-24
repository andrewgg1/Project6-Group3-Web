from flask import Flask
import database
from routes.artist_routes import artist_bp
from routes.song_routes import song_bp
from routes.album_routes import album_bp

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(artist_bp)
app.register_blueprint(song_bp)
app.register_blueprint(album_bp)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the Music Library!'

if __name__ == "__main__":
    app.run()
