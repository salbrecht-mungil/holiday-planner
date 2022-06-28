Endpoints:  
    1.  http://localhost:5000/holidays?status=pending
        method: GET
        description: list all entries with "pending" status
    2.  http://localhost:5000/holidays/<hol_id>
        method: GET
        description: read a particular holiday request
    3.  http://localhost:5000/holidays/add
        method: POST
        description: create new holiday request
    4.  http://localhost:5000/holidays/update
        method: PUT
        description: update a particular holiday request
    
    
     
Technologies used:
Python, pip, pipenv, Flask, SQLite