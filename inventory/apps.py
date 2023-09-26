from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
    verbose_name = 'Inventory'
    verbose_name_plural = 'Inventory'
    icon = '⏳'

    def ready(self):
        import inventory.signals
