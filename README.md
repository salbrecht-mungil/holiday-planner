# Pre-existing knowledge

My previous experience with creating and deploying APIs were limited to Mulesoft and working within very confined requirements (most things were set up with matured tooling and configured CICDs). 

Also, this is only my second project I have written from scratch. Since I had little or no experience with the tools being used there was a steep learning curve. But I enjoyed every bit of it.

# Assumptions

- Eventually the API would retrieve certain variables such as the employee_id and manager_id from an authentication layer. For simplicity this is currently represented through query parameters.
- At present the vacation dates are handled as vacation_start_date <= vacation_end_date.
- Annual leave is assigned per calendar year (if this is not the case the calculations will have to be amended)

# Planning the assignment

First I was reading about and non-relational or relational databases such as MongoDB and SQL. I decided that an SQL relational database (I chose PostgreSQL) is the most suitable for the assignment since the data are well structured and relationships between tables can easily be formed.

My design for the database contains three tables which are connected through Foreign Keys to represent the following relationships:
        - employees -> managers = Many_To_One
        - employees -> holidays = One_To_Many
        - managers -> holidays = One-To-Many

To be able to represent my data models with objects and query those entities, I decided to connect the APIs with the database through an Object Relational Mapper. Since SQLAlchemy is well documented I thought this was a suitable tool for my task. 

To start with, I created the folder `holiday_database` containing all files necessary to create a new database containing the three tables with examples. 
Then I built the model(s) (see `model.py`) for the database which would eventually be used for both APIs.
Finally I built two APIs, one to be used by employees called `worker.py` and one by managers called `manager.py`.

# Tech stack:

- Python3.9
- pipenv for dependencies
- Flask for the API
- Docker to create PostgreSQL instance

# Instructions for running the API

First you need to navigate to the main folder: `cd holiday_planner`
You will need to have Python3.9 installed along with pip. 
Run the following:
- Install pipenv for dependencies: `pip install pipenv`
- Install the required dependencies: `pipenv install`
- Create a PostgreSQL instance on port 5432: `docker run --name sqlalchemy-orm-psql -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=usr -e POSTGRES_DB=sqlalchemy -p 5432:5432 -d postgres`
- Navigate to the database folder: `cd holiday_database/`
- Create and populate tables in PostgreSQL database: `pipenv shell` and then `python inserts.py`
- Navigate back to the main folder: `cd ..`
- Run the Employee API: `./bootstrap-worker.sh`
- Run the Manager API: `./bootstrap-manager.sh`

## Endpoints
- Employees: 
    - GET localhost:5050/holiday-requests
    - POST localhost:5050/holiday-requests
- Managers:
    - GET localhost:5000/holidays
    - GET localhost:5000/overlapping-requests
    - PATCH localhost:5000/holidays/{holiday_id}

## Testing
I am very well aware that testing is a crucial part of developing new software and if I had more time I would look into upskilling in this area and add all the required tests to the code. However, since I haven't got much experience in writing tests in a TDD fashion I decided to only create example requests in Postman representing different test cases for this assignment.

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
- Add unit tests and e2e tests to ensure the API can cope with all possible scenarios.
- Currently database connection is hard-coded. postgresConn would have to be dynamically managed through environment variables. Now that I've come across 12 factor apps during the assignment I would apply those principles which would include configuration of evironment variables.
- Add an authentication and an authorization layer to secure the API.
- Add payload validation, e.g. to validate vacation start and end dates.
- Add a repository pattern such as Docker to manage complexity (e.g. through the Dockerfile), take advantage of re-usability and not having to worry about setting up different environments.
- Looking into database migrations to handle the set up and maintanance of the database as opposed to how it's been handled in this assignment. 