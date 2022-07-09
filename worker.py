from flask import jsonify, request, abort
from werkzeug.exceptions import HTTPException
from .model import Holiday, Employee
from datetime import datetime
from .config import app, db

import json

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

# List all the holiday requests for a particular employee_id - this would normally be retrieved from the logging in page
# Return the number of holidays left if the request was approved
# Constraints: 
#   - annual leave is calculated per calendar year
#   - holidays can not be taken over into new year
@app.route('/holiday-requests', methods=['GET'])
def get_holiday_request():
    args = request.args
    page = args.get('page', type=int, default=1)
    per_page = 5
    status = args.get('status')
    # The employee_id should be retrieved from the UI
    employee_id = args.get('employee_id')

    if status:
        if employee_id:
            query = Holiday.query.filter(Holiday.status == status, Holiday.employee_id == employee_id)
        else:
            abort(401)            
    elif employee_id:
        query = Holiday.query.filter(Holiday.employee_id == employee_id)
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

# Creating a new holiday request in case there are enough days left to take  
@app.route('/holiday-requests', methods=["POST"])
def post_holiday_request():
    data = json.loads(request.get_data())
    # The employee_id should be retrieved from the UI
    employee_id = data['author']

    # Calculating the holidays remaining for the year
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

    status = 'pending' 
    # Get manager_id from Employee table 
    manager_id_list = Employee.query.filter(Employee.id == employee_id).all()
    manager_id_object = manager_id_list[0]
    manager_id = manager_id_object.manager_id
    # Set created_at_date to time of making the request
    created_at_date = datetime.now()
    holiday_start_date_req = data['vacation_start_date']
    holiday_end_date_req = data['vacation_end_date']
    number_of_hol_requested = abs((datetime.strptime(holiday_end_date_req, "%Y-%m-%d")  - datetime.strptime(holiday_start_date_req, "%Y-%m-%d")).days)

    # Creating a request if requested amount of days is < or = remaining holidays     
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