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

# Returns info message
@app.route('/')
def root():
    msg_value = 'Flask REST app for CRUD operations on PostgreSQL.'
    return resp(200, {"message": msg_value})

# Returns all users from database (for testing)
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
    with db_conn() as db:
        select = db.prepare("SELECT \"dateOfBirth\" FROM dates WHERE username = $1")
        [(birthdate,)] = select(username)
        birthday = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()
        left = days_left(birthday, today)
        if left == 0:
            msg_value = 'Hello, ' + username + '! Happy birthday!'
        else:
            msg_value = 'Hello, ' + username + '! Your birthday is in ' + str(left) + ' day(s).'
        return resp(200, {"message": msg_value})

# Saves the given user's name and date of birth in the database
@app.route('/hello/<string:username>', methods=['POST'])
def post_user(username):
    with db_conn() as db:
        insert = db.prepare(
            "INSERT INTO dates (username, \"dateOfBirth\") VALUES ($1, $2)")
        json = request.get_json()
        insert (username, json['dateOfBirth'])
        msg_value = 'New user \'' + username + '\' was added successfully!'
        return resp(201, {"message": msg_value})

if __name__ == '__main__':
    app.run()
