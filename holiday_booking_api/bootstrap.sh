#!/bin/sh
export FLASK_APP=./holiday_booking_api/index.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0