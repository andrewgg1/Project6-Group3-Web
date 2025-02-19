# Music Library API

A Flask-based REST API for managing a music library with MongoDB/MongoEngine.

## Prerequisites

- [Python 3.13.1](https://www.python.org/downloads/release/python-3131/)
- pip (Python package manager, should already be included with Python)
- [MongoDB installed and running locally](https://www.mongodb.com/try/download/community)
- [Postman (for manual API testing)](https://www.postman.com/downloads/)

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

Can also be run in non-debug mode using the following command:

```sh
flask run
```

## Testing the API

Use Postman to test the API endpoints.

## Songs

### GET /songs

**URL**: `http://127.0.0.1:5000/songs`

Gets all songs in the library. Supports a `search` query parameter for filtering.

### GET /songs/\<ID>

**URL**: `http://127.0.0.1:5000/songs/<ID>`

Gets a specific song by ID.

### POST /songs

**URL**: `http://127.0.0.1:5000/songs`

**Request Body (JSON)**:
```json
{
    "song_name": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name",
    "song_length": 300,
    "genre": "Genre",
    "release_year": 2024
}
```
**Request Body (Form Data)**:

- `song_name`: Song Title
- `artist`: Artist Name
- `album`: Album Name
- `song_length`: Song Length (seconds)
- `genre`: Genre
- `release_year`: Release Year

Creates a new song. Supports both JSON and form data request types. On success, redirects to the home page.

### DELETE /del-song/\<ID>

**URL**: `http://127.0.0.1:5000/del-song/<ID>`

Deletes a specific song by ID. This endpoint is called with a POST request from the home page.

### POST/PUT/PATCH /songs/\<ID>

**URL**: `http://127.0.0.1:5000/songs/<ID>`

**Request Body (JSON for PUT/PATCH)**:
```json
{
    "song_name": "Updated Song Title",
    "artist": "Updated Artist Name",
    "album": "Updated Album Name",
    "song_length": 315,
    "genre": "Updated Genre",
    "release_year": 2023
}
```

**Request Body (Form Data for POST)**:

- `song_name`: Updated Song Title
- `artist`: Updated Artist Name
- `album`: Updated Album Name
- `song_length`: Updated Song Length (seconds)
- `genre`: Updated Genre
- `release_year`: Updated Release Year

Edits a specific song by ID. Supports both JSON (for PUT/PATCH) and form data (for POST) request types. On success, redirects to the home page.