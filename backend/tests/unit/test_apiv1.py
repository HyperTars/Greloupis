import unittest
from apiv1 import api
from utils.util_tests import util_tests_python_version

class TestApiV1(unittest.TestCase):

    def test_api(self):
        util_tests_python_version()
        self.assertIsNotNone(api,
                             "Flask API with blueprint initialization check")
        self.assertEqual(api.namespaces[0].name, "default",
                         "Blueprint default namespace check")
        self.assertEqual(api.namespaces[1].name, "user",
                         "Blueprint user namespace check")
        self.assertEqual(api.namespaces[2].name, "video",
                         "Blueprint video namespace check")
        self.assertEqual(api.namespaces[3].name, "search",
                         "Blueprint search namespace check")
