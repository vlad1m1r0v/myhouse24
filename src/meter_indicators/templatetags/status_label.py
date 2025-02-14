from django import template

register = template.Library()


@register.inclusion_tag("meter_indicators/adminlte/_partials/status_label.html")
def status_label(obj):
    return {'object': obj}
