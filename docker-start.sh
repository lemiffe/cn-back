#!/bin/bash
# Note: This is only for local development (see .circleci/config.yml for production deploys)
# Note: This requires the cn-db container to be running already (and "cnetwork" setup, see start_mongo.sh in cn-db for more info)

docker stop cn-back
docker rm cn-back
docker rmi cn-back
docker build -t cn-back .
docker run -d -p 1338:8080 --network=cnetwork --restart always --name cn-back cn-back