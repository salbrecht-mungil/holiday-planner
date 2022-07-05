from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

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