from django.apps import AppConfig

class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'

    def ready(self):
        import apps.cart.signals  # Signalni import qilish