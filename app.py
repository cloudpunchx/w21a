from flask import Flask, request
import json
from dbhelpers import run_statement
from helpers import check_data

app = Flask(__name__)

# ITEM SECTION:

# GET items
# Included: bonus 1. Optional Limit Parameter, Bonus 2. returns the limited items based on highest quantity
@app.get('/api/item')
def get_items():
    item_limit = request.args.get('item_limit')
    result = run_statement("CALL get_items(?)", [item_limit])
    if (type(result) == list):
        return json.dumps(result, default=str)
    else: 
        return "Sorry, something went wrong."

# POST items
@app.post('/api/item')
def post_item():
    """
    Expects the fields:
    name, description, quantity
    """
    required_data = ['name', 'description', 'quantity']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    description = request.json.get('description')
    quantity = request.json.get('quantity')
    result = run_statement("CALL post_item(?,?,?)", [name, description, quantity])
    if (type(result) == list):
        if result[0][0] == 1:
            return "Successfully created item."
        else:
            return "Creation unsuccessful for item."

# PATCH items
# Included: bonus 3. change patch item to accept optional data for name, description
@app.patch('/api/item')
def patch_item():
    """
    Expected field:
    item id, quantity
    """
    required_data = ['id', 'quantity']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    id = request.json.get('id')
    name = request.json.get('name')
    description = request.json.get('description')
    quantity = request.json.get('quantity')
    result = run_statement("CALL update_quantity(?,?,?,?)", [id, name, description, quantity])
    if (type(result) == list):
        if result[0][0] == 1:
            return f"Successfully updated item {id}."
        else:
            return f"Update unsuccessful for item {id}, check Item ID."

# DELETE items
@app.delete('/api/item')
def delete_item():
    """
    Expected field:
    Item Id
    """
    check_result = check_data(request.json, ['itemId'])
    if check_result != None:
        return check_result
    item_id = request.json.get('itemId')
    if item_id == None:
        return "You have to specify an Item ID."
    result = run_statement("CALL delete_item(?)", [item_id])
    if (type(result) == list):
        if result[0][0] == 1:
            return f"Successfully deleted item {item_id}."
        else:
            return f"Delete unsuccessful for item {item_id}, check Item ID."

# EMPLOYEE SECTION :

# GET employee by ID
@app.get('/api/employee')
def get_employees():
    """
    Expected field:
    employee id
    """
    check_result = check_data(request.json, ['id'])
    if check_result != None:
        return check_result
    employee_id = request.json.get('id')
    result = run_statement("CALL get_employees(?)", [employee_id])
    if (type(result) == list):
            return json.dumps(result, default=str)
    else: 
        return "An error has occurred."

# POST employees
@app.post('/api/employee')
def post_employee():
    """
    Expects the fields:
    name, hourly wage
    """
    required_data = ['name', 'hourlyWage']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    hourly_wage = request.json.get('hourlyWage')
    result = run_statement("CALL post_employee(?,?)", [name, hourly_wage])
    if (type(result) == list):
        if result[0][0] == 1:
            return "Successfully added Employee."
        else:
            return "An error has occurred, Employee not added."

# PATCH employees
@app.patch('/api/employee')
def patch_employee():
    """
    Expected field:
    employee id, hourly wage
    """
    required_data = ['id', 'hourlyWage']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    id = request.json.get('id')
    hourly_wage = request.json.get('hourlyWage')
    result = run_statement("CALL patch_employee(?,?)", [id, hourly_wage])
    if (type(result) == list):
        if result[0][0] == 1:
            return f"Successfully updated Employee {id}."
        else:
            return f"Update unsuccessful for Employee {id}, check ID."

# DELETE employees
@app.delete('/api/employee')
def delete_employee():
    """
    Expected field:
    Item Id
    """
    check_result = check_data(request.json, ['id'])
    if check_result != None:
        return check_result
    id = request.json.get('id')
    if id == None:
        return "You have to specify an Employee ID."
    result = run_statement("CALL delete_employee(?)", [id])
    if (type(result) == list):
        if result[0][0] == 1:
            return f"Successfully deleted Employee {id}."
        else:
            return f"Delete unsuccessful for Employee {id}, check ID."


app.run(debug = True)