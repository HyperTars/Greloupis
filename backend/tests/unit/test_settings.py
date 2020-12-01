import os
from unittest import TestCase, mock
from settings import get_config, TestConfig, ProdConfig, DevConfig


class SettingsTests(TestCase):

    @mock.patch.dict(os.environ, {"PROFILE": "test"})
    def test_settings(self):
        self.assertEqual(get_config(), TestConfig)

    @mock.patch.dict(os.environ, {"PROFILE": "prod"})
    def prod_settings(self):
        self.assertEqual(get_config(), ProdConfig)

    @mock.patch.dict(os.environ, {"PROFILE": "dev"})
    def dev_settings(self):
        self.assertEqual(get_config(), DevConfig)
