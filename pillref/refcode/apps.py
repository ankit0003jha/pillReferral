from django.apps import AppConfig


class RefcodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'refcode'

    def ready(self):
        import refcode.signals