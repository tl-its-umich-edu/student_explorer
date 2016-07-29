from django import template
from django.utils.safestring import mark_safe
import json
import decimal

register = template.Library()

# Source:
# http://stackoverflow.com/questions/16957275/python-to-json-serialization-fails-on-decimal


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


@register.filter
def get_score(qs):
    if qs.exists():
        avg_score = qs[0].current_score_average
        if avg_score is None:
            return 'N/A'
        else:
            return avg_score
    else:
        return 'N/A'


@register.filter
def jsonify(list):
    return mark_safe(json.dumps(list, default=decimal_default))


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except:
        return None


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except:
        return None


@register.filter
def get_bar_width(value, arg):
    width = value
    if arg != 'N/A' and value != 'N/A':
        arg = float(arg)
        value = float(value)
        if arg > 100.0 and value < arg:
            width = value * 100.0 / arg
    return width
