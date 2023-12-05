#!/bin/bash

# Go to John Coltrane repository
cd $HOME/Documents/code/JohnColtraneBot

# install dependencies
pipenv install

# run gunicorn
RUN_SCHEDULER=true LOGGING_VERBOSE=false pipenv run gunicorn -w 1 "app:app" -b :8001
