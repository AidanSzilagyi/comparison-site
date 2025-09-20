from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def shortened_timesince(value, arg=None):
    # Return only the largest time unit from timesince.
    # Example: '20 hours, 11 minutes' -> '20 hours'
    if not value:
        return ""
    result = timesince(value, arg)
    return result.split(",")[0].strip()
