from django import template
from ..models import List

register = template.Library()

@register.filter
def permission_description(value):
    return List.permission_descriptions.get(value, "")

@register.filter
def requires_invite(value):
    try:
        return List.Permission(value).requires_invite
    except ValueError:
        return False
