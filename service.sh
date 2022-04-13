#!/bin/bash

gunicorn -w 1 -b 0.0.0.0:9000 --capture-output --log-level debug --access-logfile /var/logs/gunicorn/deployer/access.log --error-logfile /var/logs/gunicorn/deployer/errors.log app:app
