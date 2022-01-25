from importlib import import_module

from django.apps import AppConfig


class LibrariesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'libraries'

    def ready(self):
        import libraries.receivers
