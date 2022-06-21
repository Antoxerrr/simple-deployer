#!/bin/bash

pipenv run gunicorn -w 1 -b 0.0.0.0:9000 --capture-output deployer.app:app
