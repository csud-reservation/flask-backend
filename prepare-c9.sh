#!/bin/bash

rm -rf *
virtualenv -p python3 venv
source venv/bin/activate
git init
git remote add origin https://github.com/csud-reservation/flask-backend.git
git fetch
git checkout -t origin/dev