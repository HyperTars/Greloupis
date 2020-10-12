import unittest
from source.app import *

class TestApp(unittest.TestCase):

    def test_app(self):
        self.assertIsNotNone(app, msg="Flask app initialization check")
        self.assertEqual(app.name, 'source.app', msg="Flask app name check")


if __name__ == '__main__':
    unittest.main()