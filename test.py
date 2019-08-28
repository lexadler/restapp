#!/usr/bin/env python3.7
import unittest
import app
import xmlrunner
from json import dumps
from datetime import date

today = date.today()
tomorrow = date(today.year-1,today.month,today.day+1)
yesterday = date(today.year,today.month,today.day-1)

class TestHello(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "Flask REST app for CRUD operations on PostgreSQL."}\n')

    def test_today(self):
        route = '/hello/today'
        rv = self.app.put(route, json={'dateOfBirth': str(today)})
        self.assertTrue(rv.status == '204 NO CONTENT' or rv.status == '201 CREATED')
        rv = self.app.get(route)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "Hello, today! Happy birthday!"}\n')
        rv = self.app.delete(route)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "User \'today\' was deleted successfully."}\n')

    def test_tomorrow(self):
        route = '/hello/tomorrow'
        rv = self.app.put(route, json={'dateOfBirth': str(tomorrow)})
        self.assertTrue(rv.status == '204 NO CONTENT' or rv.status == '201 CREATED')
        rv = self.app.get(route)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "Hello, tomorrow! Your birthday is in 1 day(s)."}\n')
        rv = self.app.delete(route)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "User \'tomorrow\' was deleted successfully."}\n')

    def test_today(self):
        route = '/hello/yesterday'
        rv = self.app.put(route, json={'dateOfBirth': str(yesterday)})
        self.assertTrue(rv.status == '204 NO CONTENT' or rv.status == '201 CREATED')
        rv = self.app.get(route)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "Hello, yesterday! Your birthday is in 365 day(s)."}\n')
        rv = self.app.delete(route)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "User \'yesterday\' was deleted successfully."}\n')

if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
