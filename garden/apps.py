from django.apps import AppConfig


class GardenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garden'

    def ready(self):
        import garden.signals  # Import the signals module where your signal handlers are defined
