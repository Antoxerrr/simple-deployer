#!/bin/bash

if ! cd "$1" ; then
    echo "Failed to enter folder $1"
    exit 1
fi

git pull origin $2
docker-compose rm -sf celery_worker celery_beat app
docker-compose build --no-cache celery_worker celery_beat app
docker-compose up -d celery_worker celery_beat app
docker system prune -af