#!/bin/bash

cd /root/apps/Academy && /usr/libexec/git-core/git pull \
  && /usr/local/bin/docker-compose down \
  && /usr/local/bin/docker-compose volume rm academy_static_volume \
  && /usr/local/bin/docker-compose build --no-cache \
  && /usr/local/bin/docker-compose up -d