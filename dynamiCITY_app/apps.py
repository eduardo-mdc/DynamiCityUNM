from django.apps import AppConfig


class DynamicityAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dynamiCITY_app'

    def ready(self):
        import dynamiCITY_app.signals