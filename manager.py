from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import postgresConn
from werkzeug.exceptions import HTTPException
from .model import Holiday

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgresConn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

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

@app.route('/holidays/<int:page>', methods=['GET'])
def get_holidays(page=1):
    args = request.args
    page = args.get('page')
    per_page = 10
    id = args.get('id')
    employee_id = args.get('employee_id')
    manager_id = args.get('manager_id')
    status = args.get('status')
    created_at_date = args.get('created_at_date')
    holiday_start_date = args.get('holiday_start_date')
    holiday_end_date = args.get('holiday_end_date')
    number_of_holidays = args.get('number_of_holidays')
    query = Holiday.query

    if id:
        query = query.filter(Holiday.id == id)
    if employee_id:
        query = query.filter(Holiday.employee_id == employee_id)
    if manager_id:
        query = query.filter(Holiday.manager_id == manager_id)
    if status:
        query = query.filter(Holiday.status == status)
    if created_at_date:
        query = query.filter(Holiday.created_at_date == created_at_date)
    if holiday_start_date:
        query = query.filter(Holiday.holiday_start_date == holiday_start_date)
    if holiday_end_date:
        query = query.filter(Holiday.holiday_end_date == holiday_end_date)
    if number_of_holidays:
        query = query.filter(Holiday.number_of_holidays == number_of_holidays)
    
    holiday_query = query.order_by(created_at_date).paginate(page, per_page, error_out=False)
    filtered_holiday_request = holiday_query.items
    filtered_holiday_list = []
    for req in filtered_holiday_request:
        filtered_holidays = {
            'id': req.id,
            'author': req.employee_id, 
            'status': req.status, 
            'resolved_by': req.manager_id, 
            'request_created_at': req.created_at_date, 
            'vacation_start_date': req.holiday_start_date, 
            'vacation_end_date': req.holiday_end_date,
            'number_of_days_requested': req.number_of_holidays
        }
        filtered_holiday_list.append(filtered_holidays)

    return jsonify(result = filtered_holiday_list)

@app.route('/holidays/<int:holiday_id>', methods=['PATCH'])
def update_holiday(holiday_id):
    data = json.loads(request.get_data())
    status = data['status'] 
                                
    update_request = Holiday.query.get(holiday_id)
    update_request.status = status
        
    db.session.add(update_request)
    db.session.commit()

    return "Holiday status has been updated", 200

if __name__ == '__main__':
    app.run()