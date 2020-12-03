import os
import unittest
from unittest import mock
from settings import get_config, ProdConfig, DevConfig, TestConfig


class TestSetting(unittest.TestCase):

    @mock.patch.dict(os.environ, {"PROFILE": "prod"})
    def test_settings_prod(self):
        self.assertEqual(get_config(), ProdConfig)

    @mock.patch.dict(os.environ, {"PROFILE": "dev"})
    def test_settings_dev(self):
        self.assertEqual(get_config(), DevConfig)

    @mock.patch.dict(os.environ, {"PROFILE": "test"})
    def test_settings_test(self):
        self.assertEqual(get_config(), TestConfig)
