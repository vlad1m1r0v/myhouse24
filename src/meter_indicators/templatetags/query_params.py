from django.template import Library
from urllib.parse import urlencode

register = Library()


@register.simple_tag
def add_query_params(**params):
    query_string = urlencode({k: v for k, v in params.items() if v})
    return f"?{query_string}"
