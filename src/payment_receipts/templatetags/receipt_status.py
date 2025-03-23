from django import template

register = template.Library()


@register.inclusion_tag("payment_receipts/adminlte/_partials/status.html")
def receipt_status(obj):
    return {'object': obj}