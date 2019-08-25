#!/usr/bin/env python3.7

import postgresql
import flask
import json

app = flask.Flask(__name__)

def db_conn():
    return postgresql.open('pq://restuser:sql@localhost:5432/birthdays')

@app.route('/')
def root():
    return flask.Response(status=200, response="Hello world!")

if __name__ == '__main__':
    app.run()
