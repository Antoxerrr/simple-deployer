#!/bin/bash

if ! cd "$1" ; then
    echo "Failed to enter folder $1"
    exit 1
fi

git pull origin $2
docker-compose rm -sf app
docker-compose build --no-cache app
docker-compose up -d app
docker system prune -af