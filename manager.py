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

# List all holiday requests filterable by any of the column names of the holiday table.
# Return whether request overlaps with other approved or pending requests 
@app.route('/holidays', methods=['GET'])
def get_holidays():
    args = request.args
    page = args.get('page', type=int, default=1)
    per_page = 5
    id = args.get('id')
    employee_id = args.get('employee_id')
    manager_id = args.get('manager_id')
    status = args.get('status')
    created_at_date = args.get('created_at_date')
    holiday_start_date = args.get('holiday_start_date')
    holiday_end_date = args.get('holiday_end_date')
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
    
    holiday_query = query.order_by(created_at_date).paginate(page, per_page, False)
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
            'vacation_end_date': req.holiday_end_date
        }
        filtered_holiday_list.append(filtered_holidays)

    return jsonify(result = filtered_holiday_list)

# Get a list of objects showing requests with overlapping dates
@app.route('/overlapping-requests', methods=['GET'])
def get_overlapping_requests():
    # Fetch all requests in database with pending or approved status
    query_approved_and_pending = Holiday.query.filter(Holiday.status != 'rejected').all() 
    overlapping_days_list = []
    for i in query_approved_and_pending:
        i_start_date = i.holiday_start_date
        i_end_date = i.holiday_end_date
        for j in query_approved_and_pending:
            if i != j:
                j_start_date = j.holiday_start_date
                j_end_date = j.holiday_end_date
                # Case: The processed holiday request has start date set before the start date of the item it gets compared to.
                if i_start_date < j_start_date:
                    # Case: The processed holiday request has end date set before the start date of the item it gets compared to. No overlap
                    if i_end_date < j_start_date:
                        overlapping_days = {
                            'holiday_id_one': i.id,
                            'holiday_id_two': j.id,
                            'overlap': False
                        }
                    # Case: The processed holiday request has end date set after the start date of the item it gets compared to. Overlap    
                    else:
                        overlapping_days = {
                            'holiday_id_one': i.id,
                            'holiday_id_two': j.id,
                            'overlap': True
                        }
                        overlapping_days_list.append(overlapping_days)
                # Case: The processed holiday request has start and end date set within the range of start and end date of the item it gets compared to.  
                if i_start_date >= j_start_date and i_start_date <= j_end_date:
                        overlapping_days = {
                            'holiday_id_one': i.id,
                            'holiday_id_two': j.id,
                            'overlap': True
                        }
                        overlapping_days_list.append(overlapping_days)
                # Case: The processed holiday request has start and end date set after the end date of the item it gets compared to.
                else:
                    overlapping_days = {
                        'holiday_id_one': i.id,
                        'holiday_id_two': j.id,
                        'overlap': False
                    }
    
    return jsonify(result = overlapping_days_list)    

# Update a particular holiday request
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