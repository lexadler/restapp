#!/usr/bin/env python3.7

import postgresql
import flask
import json

app = flask.Flask(__name__)

def db_conn():
    return postgresql.open('pq://restuser:sql@localhost:5432/birthdays')

def to_json(data):
    return json.dumps(data) + "\n"

def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )

@app.route('/')
def root():
    return flask.Response(status=200, response="Hello world!")

@app.route('/users', methods=['GET'])
def get_users():
    with db_conn() as db:
        tuples = db.query("SELECT username, \"dateOfBirth\" FROM dates")
        dates = []
        for (username, dateOfBirth) in tuples:
            dates.append({"username": username, "dateOfBirth": dateOfBirth})
        return resp(200, {"users": dates})

@app.route('/hello/<string:username>', methods=['GET'])
def get_user(username):
    with db_conn() as db:
        select = db.prepare("SELECT \"dateOfBirth\" FROM dates WHERE username = $1")
        [(birthdate,)] = select(username)
        print(birthdate)
        return resp(200, {"dateOfBirth": birthdate})

@app.route('/hello/<string:username>', methods=['POST'])
def post_user(username):
    with db_conn() as db:
        insert = db.prepare(
            "INSERT INTO dates (username, \"dateOfBirth\") VALUES ($1, $2)")
        json = flask.request.get_json()
        insert (username, json['dateOfBirth'])
        return flask.Response(status=200, response="New user \'" + username + "\' was added successfully!")

if __name__ == '__main__':
    app.run()
