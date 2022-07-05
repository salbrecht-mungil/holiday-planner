from flask import Flask, jsonify, request, abort
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

@app.route('/holiday-requests', methods=['GET'])
def get_holiday_request():
    args = request.args
    page = args.get('page')
    per_page = 5
    status = args.get('status')
    employee_id = args.get('employee_id')
    query = Holiday.query

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
    for req in filtered_query:
        filtered_requests = {
            'id': req.id,
            'author': req.employee_id, 
            'status': req.status, 
            'resolved_by': req.manager_id, 
            'request_created_at': req.created_at_date, 
            'vacation_start_date': req.holiday_start_date, 
            'vacation_end_date': req.holiday_end_date,
            'number_of_days_requested': req.number_of_holidays
        }
        filtered_query_list.append(filtered_requests)

    return jsonify(result = filtered_query_list)

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