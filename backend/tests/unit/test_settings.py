import os
import unittest
from unittest import mock
from settings import get_config, TestConfig, ProdConfig, DevConfig


class TestSettingTest(unittest.TestCase):

    @mock.patch.dict(os.environ, {"PROFILE": "test"})
    def test_settings(self):
        self.assertEqual(get_config(), TestConfig)


class TestSettingProd(unittest.TestCase):

    @mock.patch.dict(os.environ, {"PROFILE": "prod"})
    def prod_settings(self):
        self.assertEqual(get_config(), ProdConfig)


class TestSettingDev(unittest.TestCase):

    @mock.patch.dict(os.environ, {"PROFILE": "dev"})
    def dev_settings(self):
        self.assertEqual(get_config(), DevConfig)
