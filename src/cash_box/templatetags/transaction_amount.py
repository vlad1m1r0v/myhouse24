from django import template

register = template.Library()


@register.inclusion_tag("cash_box/adminlte/_partials/amount.html")
def transaction_amount(obj):
    return {'object': obj}