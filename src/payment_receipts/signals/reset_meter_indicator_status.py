from django.db.models.signals import pre_delete
from django.dispatch import receiver

from src.meter_indicators.models import StatusChoices
from src.payment_receipts.models import ReceiptService


@receiver(pre_delete, sender=ReceiptService)
def reset_meter_indicator_status(sender, instance, **kwargs):
    """
    before deleting ReceiptService return status of meter indicator to 'NEW'.
    """
    if instance.meter_indicator:
        instance.meter_indicator.status = StatusChoices.NEW
        instance.meter_indicator.save()