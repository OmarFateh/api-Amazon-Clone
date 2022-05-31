from django.apps import AppConfig


class BrandConfig(AppConfig):
    name = 'brand'

    def ready(self):
        import brand.signals