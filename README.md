# Available Endpoints

Employees: 
    - GET localhost:5000/holiday-requests
    - POST localhost:5000/holiday-requests

Managers:
    - GET localhost:5000/holidays
    - GET localhost:5000/overlapping-requests
    - PATCH localhost:5000/holidays/{holiday_id}
    
# Pre-existing knowledge

At the beginning I wasn't familiar with Python beyond a couple of Udemy courses and some small practice tasks in Jupyter Notebook. 

I had no knowledge in dependency handling in Python or which framework to use. I chose Flask since Flask applications are known for being lightweight and it has plenty of documentation in case you run into issues. 

Also, my previous experience with creating and deploying APIs were limited to Mulesoft and working within very confined requirements (most things were set up with matured tooling and configured CICDs). 

I never had to worry about how to package an application and deploy it. So this was a useful exercise for me to learn how to containerise an API using Docker.

I wanted to understand SpaCy a lot more but I tried to stick close to the 1.5 hour mark as suggested in the specification.

This all took considerably longer than I anticipated, but I had to upskill to achieve this and I'm grateful for this opportunity.
Endpoints:  
    1.  http://localhost:5000/holidays?status=pending
        method: GET
        description: list all entries with "pending" status
    2.  http://localhost:5000/holidays/hol_id/
        method: GET
        description: read a particular holiday request
    3.  http://localhost:5000/holidays/
        method: POST
        description: create new holiday request
    4.  http://localhost:5000/holidays/hol_id/
        method: PUT
        description: update a particular holiday request
    
    
     
Technologies used:
Python, pip, pipenv, Flask, SQLAlchemy

Testing:

As an employee:
Test Case 1: Get holiday request of existing employee - returns list of holiday requests of a particular employee ordered by created_at_date. Each item shows the remaining holidays at the time when the holiday request was made. Employee_id should be derived through logging in data from UI. 
Test Case 2: Get holiday request of non-existing employee - returns 401 unauthorized error. 
Test Case 3: Get holiday request of existing employee, filtered by status - returns list of holiday requests of a particular employee with applied filter ordered by created_at_date. Each item shows the remaining holidays at the time when the holiday request was submitted. 
Test Case 4: Get holiday without employee specified - returns 401 unauthorized error.
Test Case 5: Make holiday request with sufficient days left - returns 201 and "Request has been added to the database". Status is automatically set as "pending" and created_at_date is set as "now". (Bug: no check for end_date > start_date)
Test Case 6: Make holiday request with insufficient days left - returns 401 and "Not enough holidays left. Change your holiday_end_date" or "No holidays left"

As a manager:
Test Case 7: Get all holiday requests available in database - returns list of holiday requests, 5 per page.
Test Case 8: Get all holiday requests available in database filtered by status - returns list of holiday requests with applied filter, 5 per page. (multiple filters possible, all database fields are filterable)
Test Case 9: Get all holiday requests for an existing employee - returns list of holiday requests for an existing employee, 5 per page.
Test Case 10: Get all holiday requests for a non-existing employee - returns 404 error.
Test Case 11: Get a list of overlapping requests - returns list of objects showing which holiday requests overlap. (Bug: currently they appear as duplicates, hol_req_one + holiday_req_two and hol_req_two + hol_req_one)
Test Case 12: Make request to change status for particular employee


