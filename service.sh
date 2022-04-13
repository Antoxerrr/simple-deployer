#!/bin/bash

pipenv run gunicorn -w 1 -b 0.0.0.0:9000 --capture-output --log-level debug --access-logfile /root/apps/simple-deployer/access.log --error-logfile /root/apps/simple-deployer/errors.log app:app
