from django import template
from ..models import List

register = template.Library()

@register.filter
def permission_description(value):
    return List.permission_descriptions.get(value, "")
