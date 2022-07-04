from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import postgresConn
from werkzeug.exceptions import HTTPException

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgresConn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

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

@app.errorhandler(HTTPException)
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

@app.route('/holidays', methods=['GET'])
def get_holidays():
    args = request.args()
    page = args.get('page')
    per_page = 5
    id = args.get('id')
    employee_id = args.get('employee_id')
    manager_id = args.get('manager_id')
    status = args.get('status')
    created_at_date = args.get('created_at_date')
    holiday_start_date = args.get('holiday_start_date')
    holiday_end_date = args.get('holiday_end_date')
    number_of_holidays = args.get('number_of_holidays')

    filtered_holidays = Holiday.query.order_by(Holiday.created_at_date).all().paginate(page,per_page,error_out=False)
    pending_holiday_list = []
    for req in pending_holiday_request:
        pending_holidays = {
            'id': req.id,
            'author': req.employee_id, 
            'status': req.status, 
            'resolved_by': req.manager_id, 
            'request_created_at': req.created_at_date, 
            'vacation_start_date': req.holiday_start_date, 
            'vacation_end_date': req.holiday_end_date,
            'number_of_days_requested': req.number_of_holidays
        }
        pending_holiday_list.append(pending_holidays)
    return jsonify(result = pending_holiday_list)

@app.route('/holiday-requests', methods=["POST"])
def post_holiday_request():
    data = json.loads(request.get_data())
    employee_id = data['author']
    status = data['status'] 
    manager_id = data['resolved_by']
    created_at_date = data['request_created_at']
    holiday_start_date = data['vacation_start_date']
    holiday_end_date = data['vacation_end_date']
    number_of_holidays = data['number_of_days_requested']
                                
    new_request = Holiday(employee_id=employee_id, status=status, manager_id=manager_id, created_at_date=created_at_date, holiday_start_date=holiday_start_date, holiday_end_date=holiday_end_date, number_of_holidays=number_of_holidays)
        
    db.session.add(new_request)
    db.session.commit()

    return "Request has been added to the database", 201


if __name__ == '__main__':
    app.run()