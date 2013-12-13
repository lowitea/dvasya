# coding: utf-8

# $Id: $
from dvasya import defaults


__all__ = ['settings']
import os


def _load_settings():
    """ Lazy Dvasya settings configurator.

    Defaults are in dvasya.defaults module,
    all of them can be overridden in module, specified in
    DVASYA_SETTINGS_MODULE (by default, it is 'settings')
    """
    module_name = os.environ.get("DVASYA_SETTINGS_MODULE", 'settings')
    module = __import__(module_name, fromlist='*')
    for attr in dir(defaults):
        if not hasattr(module, attr):
            setattr(module, attr, getattr(defaults, attr))
    return module

settings = _load_settings()
