# CN Backend API

Python 3 flask-based API for CN-APP

## Running locally

**Docker:**
- Run docker-start.sh (will stop, remove, build, and start a new container)
- Should be accessible via port 1338 (e.g. http://localhost:1338)
- If you are going to be doing local development, use compose-start.sh instead
- Make sure you ran mongo_setup.sh in cn-db first (which creates a local docker network)