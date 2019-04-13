from django.conf import settings
from django.utils.module_loading import import_string


def apiplexer(cls):
    return import_string(getattr(settings, cls.api_settings))
