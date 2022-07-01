from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey, Column, Integer, Numeric, String
from sqlalchemy.orm import relationship
from flask_restful import Api, Resource
from base import Session, engine, Base

# from holiday_database.holiday import Holiday
# , base, employee, manager

from .config import postgresConn
from holiday_planner.holiday_database.holiday import Holiday

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgresConn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# Generate database schema
Base.metadata.create_all(engine)
# Create new session
session = Session()

@app.route('/holidays')
def get_holidays_by_status():
        holidays = session.query(Holiday).filter(Holiday.status.in_('pending')).all()
        return Holiday.dump(holidays)

if __name__ == '__main__':
    app.run()