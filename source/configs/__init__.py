"""
from os import environ

PROFILE = environ.get("PROFILE", "dev")

if PROFILE == "dev":
    from .config_dev import *
elif PROFILE == "prod":
    from .config_prod import *
else:
    from .config_test import *


def get(name, default=None):
    import source.settings as this_module
    return getattr(this_module, name, default)
"""
