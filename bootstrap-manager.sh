#!/bin/sh
export FLASK_APP=manager.py
source $(pipenv --venv)/bin/activate
flask run --host 0.0.0.0 --port=5000