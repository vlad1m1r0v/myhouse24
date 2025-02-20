from django import template

register = template.Library()


@register.inclusion_tag("master_call_requests/adminlte/_partials/status_label.html")
def master_call_request_status(obj):
    return {'object': obj}