import hashlib
import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response

#SAMPLE REST API PUBLISHED ON AWS LAMBDA
# https://cwrvx8v6xj.execute-api.us-east-2.amazonaws.com/default/apitest

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

# basic http authentication, prompts username and password upon contacting the endpoint
# 'password' as plaintext should not be used to verify authorization to access. the password should be hashed and the hash should be compared to the stored password hash in the database
@app.route('/authenticatedroute', methods=['GET'])
def auth_example():
    if request.authorization:
        encoded=request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == 'username'and hashedResult.hexdigest() == masterPassword:
            return '<h1> WE ARE ALLOWED TO BE HERE </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

#2FA token submission as part of the url, similar to how personal tokens were part of the url in superheroAPI endpoints (e.g. SMS code)
@app.route('/api/token/<token>', methods = ['GET'])
def auth_token(token):
    if token == "100": #check if token is valid, ideally compare against a set of valid tokens in a database table (here valid token is 100)
        return '<h1>Congratulations, Authentication successful!</h1>'
    return 'INVALID ACCESS TOKEN'

# token submission that has expiration date and authorization is given only if token is not expired yet
# for instance, time token valid until Jan 1 2020 (no longer valid): 1577836800
# for instance, time token valid until Jan 1 2022 (still valid): 1640995200
# we can create time ticks easily with:
# date = datetime.datetime(2022, 1, 1)
# dateInSeconds = date.timestamp() #returns time in seconds since Jan 1 1970
@app.route('/api/timetoken/<timetoken>', methods=['GET']) #token is part of the url -> must be retrieved from somewhere first
def auth_timetoken(timetoken):
    if float(timetoken) > time.time(): #check if the token we have is valid still valid beyond right now (in practice you wouldn't use clearview raw time stamp, you would hash it together with a private key)
        return '<h1> Your time token is still valid! Wonderful! </h1>'
    return 'Your time token has expired!'




app.run() #always needed at the end 
