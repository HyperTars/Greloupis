import unittest
from app import app


class TestApp(unittest.TestCase):

    def test_app(self):
        self.assertIsNotNone(app, msg="Flask app initialization check")
        self.assertEqual(app.name, 'app', msg="Flask app name check")


if __name__ == '__main__':
    unittest.main()
