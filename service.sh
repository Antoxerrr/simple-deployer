#!/bin/bash

gunicorn -w 1 -b 0.0.0.0:9000 --capture-output app:app
