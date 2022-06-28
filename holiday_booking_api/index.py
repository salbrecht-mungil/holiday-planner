import sqlite3
from flask import Flask, request, jsonify, abort

import json
import datetime as dt

def connect_to_db():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE holidays (
                id INTEGER PRIMARY KEY NOT NULL,
                author TEXT NOT NULL,
                status TEXT NOT NULL,
                resolved_by TEXT NOT NULL,
                request_created_at DATETIME NOT NULL,
                vacation_start_date DATETIME NOT NULL,
                vacation_end_date DATETIME NOT NULL
            );
        ''')
app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/holidays", methods=["POST"])
def make_holiday_request():
    data = json.loads(request.get_data())
    worker_id = data['author']
    created_at = dt.datetime.now()
    vacation_start = data['vacation_start_date']
    vacation_end = data['vacation_end_date']

    if worker_id != '' and vacation_start != '' and vacation_end != '':
        if vacation_end < vacation_start:
            abort (422, 'End date has to be later than start date!')
        else:

            return 
