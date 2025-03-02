from datetime import datetime

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from src.meter_indicators.models import StatusChoices, MeterIndicator
from src.payment_receipts.models import ReceiptService


@receiver(pre_delete, sender=ReceiptService)
def receipt_service_pre_delete(sender, instance, **kwargs):
    """
    before deleting ReceiptService return status of meter indicator to 'NEW'.
    """
    if instance.meter_indicator:
        instance.meter_indicator.status = StatusChoices.NEW
        instance.meter_indicator.save()


@receiver(post_save, sender=ReceiptService)
def receipt_service_post_save(sender, instance, created, **kwargs):
    """
    Automatically create or update MeterIndicator when creating/updating ReceiptService
    """
    if not instance.meter_indicator:
        meter_indicator = MeterIndicator.objects.create(
            no=int(datetime.now().timestamp() * 1000),
            date=instance.receipt.date,
            status=StatusChoices.ACCOUNTED,
            house=instance.receipt.house,
            section=instance.receipt.section,
            flat=instance.receipt.flat,
            service=instance.service,
            value=instance.value
        )
        instance.meter_indicator = meter_indicator
        instance.save()
    else:
        instance.meter_indicator.value = instance.value
        instance.meter_indicator.status = StatusChoices.ACCOUNTED
        instance.meter_indicator.save()
