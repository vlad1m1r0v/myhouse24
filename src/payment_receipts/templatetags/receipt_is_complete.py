from django import template

register = template.Library()


@register.inclusion_tag("payment_receipts/adminlte/_partials/is_complete.html")
def receipt_is_complete(obj):
    return {'object': obj}