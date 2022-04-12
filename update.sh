#!/bin/bash

docker-compose down
# Удаляем volume со статикой, чтобы собрать её заново
docker volume rm academy_static_volume
docker-compose build --no-cache
docker-compose up -d