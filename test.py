#!/usr/bin/env python3.7
import unittest
import app
import xmlrunner

class TestHello(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_hello(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{"message": "Flask REST app for CRUD operations on PostgreSQL."}\n')

#    def test_hello_hello(self):
#        rv = self.app.get('/hello/today')
#        self.assertEqual(rv.status, '200 OK')
#        self.assertEqual(rv.data, b'{"message": "Hello, today! Happy birthday!"}\n')

#    def test_hello_name(self):
#        name = 'tomorrow'
#        rv = self.app.get(f'/hello/{name}')
#        self.assertEqual(rv.status, '200 OK')
#        self.assertIn(bytearray(f"{name}", 'utf-8'), rv.data)

if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
