from email.policy import default
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import postgresConn
from werkzeug.exceptions import HTTPException
from .model import Holiday
from datetime import datetime

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

@app.route('/holiday-requests', methods=['GET'])
def get_holiday_request():
    args = request.args
    page = args.get('page', type=int, default=1)
    per_page = 5
    status = args.get('status')
    employee_id = args.get('employee_id')
    query = Holiday.query

    print(page)
    print(type(page))

    if status:
        if employee_id:
            query = query.filter(Holiday.status == status, Holiday.employee_id == employee_id)
        else:
            abort(401)            
    elif employee_id:
        query = query.filter(Holiday.employee_id == employee_id)
    else:
        abort(401)
    
    request_query = query.paginate(page, per_page, False)
    filtered_query = request_query.items
    filtered_query_list = []
    holidays_taken_list = []
    for req in filtered_query:
        year_start = datetime.now().date().replace(month=1, day=1)
        holiday_start_date = req.holiday_start_date.date()
        holiday_end_date = req.holiday_end_date.date()
        start_to_beginning_of_year = abs((holiday_start_date - year_start).days)
        end_to_beginning_of_year = abs((holiday_end_date - year_start).days)

        # Case: holiday starts within new calendar year
        if start_to_beginning_of_year >= 0:
            if req.status == 'approved' or req.status == 'pending':
                holidays_taken = abs((holiday_end_date - holiday_start_date).days)
                holidays_taken_list.append(holidays_taken)
                holiday_sum = sum(holidays_taken_list)
            else:
                holiday_sum = 0
            remaining_holidays = 30 - holiday_sum
        # Case: holiday starts in previous calendar year. Only the days in the current year will be deducted from the leave.
        elif start_to_beginning_of_year < 0 and end_to_beginning_of_year >= 0:
            if req.status == 'approved' or req.status == 'pending':
                holidays_taken = abs((holiday_end_date - year_start).days)
                holidays_taken_list.append(holidays_taken)
                holiday_sum = sum(holidays_taken_list)
            else:
                holiday_sum = 0
            remaining_holidays = 30 - holiday_sum
        # Case: holidays booked for previous year(s)
        else:
            remaining_holidays = 0

        filtered_requests = {
            'id': req.id,
            'author': req.employee_id, 
            'status': req.status, 
            'resolved_by': req.manager_id, 
            'request_created_at': req.created_at_date, 
            'vacation_start_date': req.holiday_start_date, 
            'vacation_end_date': req.holiday_end_date,
            'remaining_holidays': remaining_holidays
        }
        filtered_query_list.append(filtered_requests)
            
    return jsonify(result = filtered_query_list) 

@app.route('/holiday-requests', methods=["POST"])
def post_holiday_request():
    data = json.loads(request.get_data())
    employee_id = data['author']

    past_holiday_query = Holiday.query.filter(Holiday.employee_id == employee_id).order_by('created_at_date').all() 
    holidays_taken_list = []
    for item in past_holiday_query:
        year_start = datetime.now().date().replace(month=1, day=1)
        holiday_start_date = item.holiday_start_date.date()
        holiday_end_date = item.holiday_end_date.date()
        start_to_beginning_of_year = abs((holiday_start_date - year_start).days)
        end_to_beginning_of_year = abs((holiday_end_date - year_start).days)

        # Case: holiday starts within new calendar year
        if start_to_beginning_of_year >= 0:
            if item.status == 'approved' or item.status == 'pending':
                holidays_taken = abs((holiday_end_date - holiday_start_date).days)
                holidays_taken_list.append(holidays_taken)
                holiday_sum = sum(holidays_taken_list)
            else:
                holiday_sum = 0
            remaining_holidays = 30 - holiday_sum
        # Case: holiday starts in previous calendar year. Only the days in the current year will be deducted from the leave.
        elif start_to_beginning_of_year < 0 and end_to_beginning_of_year >= 0:
            if item.status == 'approved' or item.status == 'pending':
                holidays_taken = abs((holiday_end_date - year_start).days)
                holidays_taken_list.append(holidays_taken)
                holiday_sum = sum(holidays_taken_list)
            else:
                holiday_sum = 0
            remaining_holidays = 30 - holiday_sum
        # Case: holidays booked for previous year(s)
        else:
            remaining_holidays = 0

    status = data['status'] 
    manager_id = data['resolved_by']
    created_at_date = data['request_created_at']
    holiday_start_date_req = data['vacation_start_date']
    holiday_end_date_req = data['vacation_end_date']
    number_of_hol_requested = abs((datetime.strptime(holiday_end_date_req, "%Y-%m-%d")  - datetime.strptime(holiday_start_date_req, "%Y-%m-%d")).days)

    if remaining_holidays > 0:
        if number_of_hol_requested <= remaining_holidays:                        
            new_request = Holiday(employee_id=employee_id, status=status, manager_id=manager_id, created_at_date=created_at_date, holiday_start_date=holiday_start_date_req, holiday_end_date=holiday_end_date_req)
        else:
            abort(401, "Not enough holidays left. Change your holiday_end_date")
    else:
        abort(401, "No holidays left")

    db.session.add(new_request)
    db.session.commit()

    return "Request has been added to the database", 201    

if __name__ == '__main__':
    app.run()