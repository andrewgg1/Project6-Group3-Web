@REM Use this script to build the docker image from scratch and then launch it in detached mode.
@REM If you just want to start an existing container, use the Start docker container command below.

@REM Start Docker Desktop
docker desktop start

@REM Build docker image:
docker-compose build

@REM Comment above and uncomment below to build with no cache
@REM docker-compose build --no-cache

@REM Start docker container:
docker-compose up -d

echo Docker container running on http://127.0.0.1:5001
