# Music Library API

A Flask-based REST API for managing a music library with MongoDB/MongoEngine.

## Prerequisites

- [Python 3.13.1](https://www.python.org/downloads/release/python-3131/)
- pip (Python package manager, should already be included with Python)
- [MongoDB installed and running locally](https://www.mongodb.com/try/download/community)
- [Postman (for API testing)](https://www.postman.com/downloads/)

## Setup

1. Clone the repository
2. Create and activate a virtual environment either through the VS Code interface or via commands:

```sh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Add sample data to the database by running the following command:

```sh
python import_data.py
```

## Running the API

Run the app using the pre-made launch.json debugger.

Can aso be run in non-debug mode using the following command:

```sh
flask run
```

## Testing the API

Use Postman to test the API endpoints.

## Artists

### GET /artists

**URL**: `http://127.0.0.1:5000/artists`

Gets all artists in the library

### GET /artists/\<ID>

**URL**: `http://127.0.0.1:5000/artists/6792dcfa3479a3961150f9ff`

Gets a specific artist by ID

### POST /artists

**URL**: `http://127.0.0.1:5000/artists`

**Request Body**:
```json
{
    "artist_name": "Post Malone",
    "country_of_origin": "USA",
    "age": 28,
    "genres": ["Hip Hop", "Pop Rap", "Alternative Rock"],
    "label": "Republic Records"
}
```

### DELETE /artists/\<ID>

**URL**: `http://127.0.0.1:5000/artists/6792dcfa3479a3961150f9ff`

Deletes a specific artist by ID

## Albums

### GET /albums

**URL**: `http://127.0.0.1:5000/albums`

Gets all albums in the library

### GET /albums/\<ID>

**URL**: `http://127.0.0.1:5000/albums/6792dcfa3479a3961150f9ff`

Gets a specific album by ID

### POST /albums

**URL**: `http://127.0.0.1:5000/albums`

**Request Body**:
```json
{
    "album_name": "Hollywood's Bleeding",
    "release_year": 2019,
    "genre": "Hip Hop"
}
```

### DELETE /albums/\<ID>

**URL**: `http://127.0.0.1:5000/albums/6792dcfa3479a3961150f9ff`

Deletes a specific album by ID

## Songs

### GET /songs

**URL**: `http://127.0.0.1:5000/songs`

Gets all songs in the library

### GET /songs/\<ID>

**URL**: `http://127.0.0.1:5000/songs/6792dcfa3479a3961150f9ff`

Gets a specific song by ID

### POST /songs

**URL**: `http://127.0.0.1:5000/songs`

**Request Body**:
```json
{
    "song_name": "Circles",
    "song_length": 215
}
```

### DELETE /songs/\<ID>

**URL**: `http://127.0.0.1:5000/songs/6792dcfa3479a3961150f9ff`

Deletes a specific song by ID