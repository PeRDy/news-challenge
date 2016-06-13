#!/usr/bin/env bash

# Get docker-machine env
eval `docker-machine env default`

# Run server
echo "Connect to:"
env | grep DOCKER_HOST | awk 'match($0, /tcp:\/\/([0-9.]+)/, a) { printf "http://%s:8000/news\n", a[1] }'
docker-compose run --service-ports news runserver > /dev/null

