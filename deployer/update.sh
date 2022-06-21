#!/bin/bash

if ! cd "$1" ; then
    echo "Failed to enter folder $1"
    exit 1
fi


git pull origin $2 \
  && docker-compose down \
  && docker volume rm $3 \
  && docker-compose build --no-cache \
  && docker-compose up -d