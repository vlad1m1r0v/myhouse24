from datetime import datetime

from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from src.meter_indicators.models import StatusChoices, MeterIndicator
from src.payment_receipts.models import ReceiptService


@receiver(pre_delete, sender=ReceiptService)
def receipt_service_pre_delete(sender, instance, **kwargs):
    """
    before deleting ReceiptService return status of meter indicator to 'NEW'.
    """
    if instance.meter_indicator:
        MeterIndicator.objects.filter(pk=instance.meter_indicator.pk).update(status=StatusChoices.NEW)


@receiver(pre_save, sender=ReceiptService)
def receipt_service_pre_save(sender, instance, **kwargs):
    """
    Automatically create or update MeterIndicator when creating/updating ReceiptService
    """
    if not instance.meter_indicator:
        meter_indicators = [
            MeterIndicator(
                no=int(datetime.now().timestamp() * 1000),
                date=instance.receipt.date,
                status=StatusChoices.ACCOUNTED,
                house=instance.receipt.house,
                section=instance.receipt.section,
                flat=instance.receipt.flat,
                service=instance.service,
                value=instance.value
            )
        ]
        created_indicators = MeterIndicator.objects.bulk_create(meter_indicators)
        instance.meter_indicator = created_indicators[0]
    else:
        MeterIndicator.objects.filter(pk=instance.meter_indicator.pk).update(
            value=instance.value,
            status=StatusChoices.ACCOUNTED
        )


@receiver(post_save, sender=MeterIndicator)
def meter_indicator_post_save(sender, instance, **kwargs):
    """
    If value of MeterIndicator has changed, we update value in ReceiptService.
    """
    ReceiptService.objects.filter(meter_indicator=instance).update(value=instance.value)
