#!/bin/bash
# filepath: init.sh
# Wait for MongoDB to be available
echo "Waiting for MongoDB to start..."
while ! nc -z mongo 27017; do
  sleep 1
done

echo "MongoDB is up, importing data..."
python import_data.py

echo "Data import complete."

echo "Starting Flask application..."
flask run