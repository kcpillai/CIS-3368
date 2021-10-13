import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

cars = [
    {'id': 0,
     'make': 'Jeep',
     'model': 'Grand Cherokee',
     'year': '2000',
     'color': 'black'},
    {'id': 1,
     'make': 'Ford',
     'model': 'Mustang',
     'year': '1970',
     'color': 'white'},
    {'id': 2,
     'make': 'Dodge',
     'model': 'Challenger',
     'year': '2020',
     'color': 'red'}
]

@app.route('/', methods=['GET']) # default url without any routing as GET request
def home():
    return "<h1> WELCOME TO OUR FIRST API! </h1>"

@app.route('/api/cars/all', methods=['GET']) #endpoint to get all the cars
def api_all():
    return jsonify(cars)

@app.route('/api/cars', methods=['GET']) #endppoint to get a single car by id: http://127.0.0.1:5000/api/cars?id=1
def api_id():
    if 'id' in request.args: #only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    
    results = [] #resulting car(s) to return
    for car in cars: 
        if car['id'] == id:
            results.append(car)
    return jsonify(results)

@app.route('/api/users', methods=['GET']) #API to get a user from the db table in AWS by id as a JSON response: http://127.0.0.1:5000/api/users?id=1
def api_users_id():
    if 'id' in request.args: #only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    conn = create_connection("cis3368fall21.ckt6dnygzu82.us-east-2.rds.amazonaws.com", "admin", "chase234", "cis3368fall21")
    sql = "SELECT * FROM users"
    users = execute_read_query(conn, sql)
    results = []

    for user in users:
        if user['id'] == id:
            results.append(user)
    return jsonify(results)

# Example to use POST as your method type, sending parameters as payload from POSTMAN (raw, JSON)
@app.route('/api/addcar', methods=['POST'])
def post_example():
    request_data = request.get_json()
    newmake = request_data['make']
    newmodel = request_data['model']
    newyear = request_data['year']
    newcolor = request_data['color']
    cars.append({ 'make': newmake, 'model': newmodel, 'year': newyear, 'color': newcolor}) #adding a new car to my car collection on the server.
    #IF I go check the /api/cars/all route in the browser now, I should see this car added to the returned JSON list of cars
    return 'POST REQUEST WORKED'

app.run()