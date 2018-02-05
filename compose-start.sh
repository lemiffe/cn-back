#!/bin/bash
docker stop cn-back
docker rm cn-back
docker rmi cn-back
docker-compose up --build -d