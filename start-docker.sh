#!/bin/bash
docker stop cn-back
docker rm cn-back
docker rmi cn-back
docker build -t cn-back .
docker run -d -p 1338:8080 --restart always --name cn-back cn-back