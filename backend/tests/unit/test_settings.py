import os
import unittest
from unittest import mock
from settings import get_config, ProdConfig


class TestSettingTest(unittest.TestCase):

    @mock.patch.dict(os.environ, {"PROFILE": "prod"})
    def test_settings(self):
        self.assertEqual(get_config(), ProdConfig)
