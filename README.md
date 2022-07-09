# Pre-existing knowledge

My previous experience with creating and deploying APIs were limited to Mulesoft and working within very confined requirements (most things were set up with matured tooling and configured CICDs). 

Also, this is only my second project I have written from scratch. Since I had little or no experience with the tools being used there was a steep learning curve. But I enjoyed every bit of it.

# Assumptions

- Once the API is connected to a UI certain variables, e.g. employee_id would be retrieved from there.
- vacation_start_date <= vacation_end_date will be handled through the UI.
- Annual leave is assigned per calendar year (if this is not the case the calculations would have to be amended)

# Steps to build the APIs

1. Create a database with examples to be able to test code whilst writing.
    - Create three tables: employees, managers, holidays
    - Connect tables through relationships: 
        - employees -> managers = Many_To_One
        - employees -> holidays = One_To_Many
        - managers -> holidays = One-To-Many
2. Create the model(s) for the database - this will be used by both APIs
3. Create one API for employees and one for managers

# Tech stack:

- Python3.9
- pipenv for dependencies
- Flask for the API using gunicorn
- Docker for containerisation

# Instructions for running the API

First you need to navigate to the main folder: `cd holiday_planner`
You will need to have Python3.9 installed along with pip. 
Run the following:
- Install pipenv for dependencies: `pip install pipenv`
- Install the required dependencies: `pipenv install`
- Navigate to the database folder: `cd holiday_database/`
- Create and populate tables in PostgreSQL database: `pipenv shell` and then `python inserts.py`
- Navigate back to the main folder: `cd ..`
- Run the Employee API: `./bootstrap-worker.sh` (Ctrl+C to quit)
- Run the Manager API: `./bootstrap-manager.sh` (Ctrl+C to quit)

Both APIs currently share port 5000, so you can only run one API at the time - This will have to be addressed.

## Endpoints
- Employees: 
    GET localhost:5000/holiday-requests
    POST localhost:5000/holiday-requests
- Managers:
    GET localhost:5000/holidays
    GET localhost:5000/overlapping-requests
    PATCH localhost:5000/holidays/{holiday_id}

## Testing
I am very well aware that testing is a very important of developing new software and if I had much more time I would certainly look into upskilling in this area. However, since I haven't got much experience in writing proper unit, integration etc tests I decided to only create example requests in Postman representing different test cases for this code test.

## Postman file for example requests
I have added a Postman collection with example requests representing the following test cases (hopefully it all works without issues for you as well).

Test cases:
1. As an employee:
- Test Case 1: Get holiday request of existing employee - returns list of holiday requests of a particular employee ordered by created_at_date. Each item shows the remaining holidays at the time when the holiday request was made. Employee_id should be derived through logging in data from UI. 
- Test Case 2: Get holiday request of non-existing employee or employee not specified - This error should be handled at the UI level and is not included in this collection.
-  Test Case 3: Get holiday request of existing employee, filtered by status - returns list of holiday requests of a particular employee with applied filter ordered by created_at_date. Each item shows the remaining holidays at the time when the holiday request was submitted.
- Test Case 4: Make holiday request with sufficient days left - returns 201 and "Request has been added to the database". Status is automatically set as "pending" and created_at_date is set as "now". (Bug: no check for end_date > start_date)
- Test Case 5: Make holiday request with insufficient days left - returns 401 and "Not enough holidays left. Change your holiday_end_date" or "No holidays left"

2. As a manager:
- Test Case 6: Get all holiday requests available in database - returns list of holiday requests, 5 per page.
- Test Case 7: Get all holiday requests available in database filtered by status - returns list of holiday requests with applied filter, 5 per page. (multiple filters possible, all database fields are filterable)
- Test Case 8: Get all holiday requests for an existing employee - returns list of holiday requests for an existing employee, 5 per page.
- Test Case 9: Get all holiday requests for a non-existing employee - returns 404 error. This is also the case for all other filters.
- Test Case 10: Get a list of overlapping requests - returns list of objects showing which holiday requests overlap. (Bug: currently they appear as duplicates, hol_req_one + holiday_req_two and hol_req_two + hol_req_one)
- Test Case 11: Make request to change status for particular employee - returns 200 and "Holiday status has been updated"

## Ideas for improvements
- Add unit tests and e2e tests to ensure the API can cope with possible scenarios.
- Add authorization (Auth0) from which employee_id and manager_id can be retrieved.
- Deploy API to cloud and allow for both APIs to run at the same time