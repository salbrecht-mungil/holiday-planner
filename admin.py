from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
# from holiday_planner.holiday_database.base import Session, engine, Base

# from holiday_database.holiday import Holiday
# , base, employee, manager

from .config import postgresConn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgresConn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# # Generate database schema
# Base.metadata.create_all(engine)
# # Create new session
# session = Session()

class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    manager = db.relationship(Manager, backref='employees')

class Holiday(db.Model):
    __tablename__ = 'holidays'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    employee = db.relationship(Employee, backref='holidays')
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    manager = db.relationship(Manager, backref='holidays')
    status = db.Column(db.String)
    created_at_date = db.Column(db.DateTime)
    holiday_start_date = db.Column(db.DateTime)
    holiday_end_date = db.Column(db.DateTime)
    number_of_holidays = db.Column(db.Numeric)

@app.route('/holidays')
def get_holidays_by_status():
        try:
                pending_requests = Holiday.query.filter_by(status='pending').order_by(Holiday.created_at_date).all()
                pending_requests_text = '<ul>'
                for req in pending_requests:
                        pending_requests_text += '<li>' + str(req.employee_id) + ', ' + str(req.holiday_start_date) + ', ' + str(req.holiday_end_date) + '</li>'
                pending_requests_text += '</ul>'
                return pending_requests_text
        except Exception as e:
                # e holds description of the error
                error_text = "<p>The error:<br>" + str(e) + "</p>"
                hed = '<h1>Something is broken.</h1>'
                return hed + error_text
                # holiday_list = session.query(Holiday.status).filter(Holiday.status=='pending')
                # return Holiday.dump(holiday_list)

if __name__ == '__main__':
    app.run()