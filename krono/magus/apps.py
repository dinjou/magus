from django.apps import AppConfig

class MagusConfig(AppConfig):
    name = 'magus'

    def ready(self):
        import magus.signals  # noqa: F401
