#!/bin/bash

cd /root/apps/Academy && git pull \
  && docker-compose down \
  && docker volume rm academy_static_volume \
  && docker-compose build --no-cache \
  && docker-compose up -d