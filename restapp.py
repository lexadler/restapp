#!/usr/bin/env python3.7

from postgresql import open
from flask import Flask, request, Response
from json import dumps
from datetime import date, datetime
from calendar import isleap

app = Flask(__name__)

# Opens database for CRUD
def db_conn():
    return open('pq://restuser:sql@localhost:5432/birthdays')

# Sending response in JSON
def to_json(data):
    return dumps(data) + "\n"

def resp(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )

# Handles leap days
def handle_leap(year, month, day):
    if day == 29 and month == 2 and not isleap(year):
        return date(year, month, day-1)
    else:
        return date(year, month, day)

# How many days are left before the birthday
def days_left(birthday, today):
    next = handle_leap(today.year, birthday.month, birthday.day)
    if today > next:
        next = handle_leap(today.year+1, birthday.month, birthday.day)
    days = (next - today).days
    return days

# Checks if username exists in database
def user_exist(username):
    with db_conn() as db:
        check = db.prepare("SELECT COUNT(1) FROM dates WHERE username = $1;")
        [(exists,)] = check(username)
        return (bool(exists))

# Validates username in URI
def user_validate(username, method):
    if not username.isalpha():
        (code, error) = (400, 'Username must be a string containing only letters.')
        return (code, error)
    elif method in ['GET', 'DELETE'] and not user_exist(username):
        (code, error) = (404, 'User with username \'' + username + '\' does not exist.')
        return (code, error)
    elif method == 'POST' and user_exist(username):
        (code, error) = (409, 'User already exists. Use \'PUT\' method for updating the date of birth.')
        return (code, error)
    (code, error) = (200, False)
    return (code, error)

# Validates date of birth in JSON
def validate_birthdate(date_of_birth):
    try:
        datetime.strptime(date_of_birth['dateOfBirth'], "%Y-%m-%d")
        return True
    except (ValueError, KeyError):
        return False

def check_birthdate(date_of_birth):
    birthday = datetime.strptime(date_of_birth['dateOfBirth'], "%Y-%m-%d").date()
    if birthday < date.today():
        return True
    else:
        return False

# Validates JSON in request body
def json_validate(json, method):
    if method in ['POST', 'PUT']:
        if json is None:
            (code, error) = (400, 'No JSON was found in the request body. Did you forget to set Content-Type header to application/json?')
            return (code, error)
        elif not validate_birthdate(json):
            (code, error) = (400, 'JSON field \'dateOfBirth\' is missing or value not in \'YYYY-MM-DD\' format.')
            return (code, error)
        elif not check_birthdate(json):
            (code, error) = (422, 'Date of birth must be a date before the today date.')
            return (code, error)
    (code, error) = (200, False)
    return (code, error)

# Validates REST request
def req_validate(username, json):
    method = request.method
    (code, error) = user_validate(username, method)
    if error:
        return (code, error)
    (code, error) = json_validate(json, method)
    return (code, error)

# Returns info message
@app.route('/')
def root():
    msg = 'Flask REST app for CRUD operations on PostgreSQL.'
    return resp(200, {"message": msg})

# Returns all users from the database (for testing)
@app.route('/users', methods=['GET'])
def get_users():
    with db_conn() as db:
        tuples = db.query("SELECT username, \"dateOfBirth\" FROM dates")
        dates = []
        for (username, dateOfBirth) in tuples:
            dates.append({"username": username, "dateOfBirth": dateOfBirth})
        return resp(200, {"users": dates})

# Returns hello birthday message for the given user 
@app.route('/hello/<string:username>', methods=['GET'])
def get_user(username):
    (code, error) = req_validate(username, None)
    if error:
        return resp(code, {"error": error})
    with db_conn() as db:
        select = db.prepare("SELECT \"dateOfBirth\" FROM dates WHERE username = $1")
        [(birthdate,)] = select(username)
        birthday = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()
        left = days_left(birthday, today)
        if left == 0:
            msg = 'Hello, ' + username + '! Happy birthday!'
        else:
            msg = 'Hello, ' + username + '! Your birthday is in ' + str(left) + ' day(s).'
        return resp(200, {"message": msg})

# Saves/updates the given username and date of birth in the database
@app.route('/hello/<string:username>', methods=['POST', 'PUT'])
def update_user(username):
    json = request.get_json()
    (code, error) = req_validate(username, json)
    if error:
        return resp(code, {"error": error})
    if request.method == 'POST' or request.method == 'PUT' and not user_exist(username):
        with db_conn() as db:
            insert = db.prepare("INSERT INTO dates (username, \"dateOfBirth\") VALUES ($1, $2)")
            insert (username, json['dateOfBirth'])
            msg = 'New user \'' + username + '\' was added successfully.'
            return resp(201, {"message": msg})
    elif request.method == 'PUT':
        with db_conn() as db:
            update = db.prepare("UPDATE dates SET \"dateOfBirth\" = $2 WHERE username = $1")
            update (username, json['dateOfBirth'])
            msg = 'Date of birth for user \'' + username + '\' was updated successfully.'
            return resp(204, {})

# Deletes the given user from the database
@app.route('/hello/<string:username>', methods=['DELETE'])
def delete_user(username):
    (code, error) = req_validate(username, None)
    if error:
        return resp(code, {"error": error})
    with db_conn() as db:
        delete = db.prepare("DELETE FROM dates WHERE username = $1")
        delete (username)
        msg = 'User \'' + username + '\' was deleted successfully.'
        return resp(200, {"message": msg})

if __name__ == '__main__':
    app.debug = True
    app.run()
