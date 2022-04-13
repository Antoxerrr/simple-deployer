#!/bin/bash

cd /root/apps/Academy && git pull \
  && docker-compose down \
  && docker-compose volume rm academy_static_volume \
  && docker-compose build --no-cache \
  && docker-compose up -d