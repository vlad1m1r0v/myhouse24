from django.apps import AppConfig


class PaymentReceiptsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.payment_receipts'

    def ready(self):
        import src.payment_receipts.signals
