import flask
from flask import jsonify
from flask import request, make_response
from flask import json
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#Creating connection to database
conn = create_connection("cis3368fall21.ckt6dnygzu82.us-east-2.rds.amazonaws.com", "admin", "chase234", "cis3368fall21")

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow show errors in browser

# Creating the api to add a celestial object to the table
@app.route('/api/addcelestialobject', methods=['POST'])
def post_object():
    request_data = request.get_json() #requesting the data from postman
    co_name = request_data['name']
    co_distance = request_data['distance']
    co_description = request_data['description']
    co_ddate = request_data['discoverydate']
    # Inserting the data into the sql query
    query = "INSERT INTO planets(name, distance, description, discoverydate) VALUES ('%s', '%s', '%s', '%s')" % (co_name, co_distance, co_description,co_ddate)
    execute_query(conn, query) #executing the query 
    conn.commit()
    return "Celestial Object Added"

# Creating the api to delete a celestial object to the table
@app.route('/api/deletecelestialobject/<token>', methods=['DELETE'])
def auth_token(token): #creating a token
    if token == "880e0d76": #check if token is valid and the token is set to 880e0d76
        if 'id' in request.args:
            id = int(request.args['id'])
        else:
            return 'ERROR: No ID provided!'
        #created a sql query to delete an object if the ids matches
        sql = "DELETE FROM planets Where id = %s" % (id)
        execute_read_query(conn, sql) #executing the query 
        conn.commit()
        return "Celestial Object has been deleted"
    else:
        return 'INVALID ACCESS TOKEN'

# Creating the api to get the furthest object from Earth
@app.route('/api/getfurthestcelestialobject', methods=['GET'])
def api_furthest_object():
    #creating sql query to get the largest distance
    sql = "SELECT MAX(distance) FROM planets"
    furthest = execute_read_query(conn,sql) #executes the query
    return jsonify(furthest) #returns the furthest planet in json format


@app.route('/api/getmostrecentthree', methods=['GET'])
def api_furthest_three():
    sql ="SELECT * FROM planets order by discoverydate DESC LIMIT 3"
    recent_three = execute_read_query(conn, sql) #executing the query
    return jsonify (recent_three) #returns the furthest planet in json format

app.run() #always needed at the end 
