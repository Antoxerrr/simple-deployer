#!/bin/bash

mkdir /var/log/gunicorn/deployer
gunicorn -w 1 -b 0.0.0.0:9000 --capture-output --log-level debug app:app
