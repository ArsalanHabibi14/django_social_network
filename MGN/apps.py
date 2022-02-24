from django.apps import AppConfig


class MgnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MGN'

    def ready(self):
        from . import signals
