from flask import Flask, request
import json
from dbhelpers import run_statement
from helpers import check_data

app = Flask(__name__)

# GET items
@app.get('/api/item')
def get_items():
    result = run_statement("CALL get_items()")
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
    if check_data == None:
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

@app.patch('/api/item')
def patch_item():
    """
    Expected field:
    item id, quantity
    """
    id = request.json.get('id')
    quantity = request.json.get('quantity')
    required_data = ['id', 'quantity']
    check_result = check_data(request.json, required_data)
    if check_data == None:
        return check_result
    result = run_statement("CALL update_quantity(?,?)", [id, quantity])
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
    if check_data == None:
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

app.run(debug = True)