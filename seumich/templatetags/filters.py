from django import template
from django.utils.safestring import mark_safe
import json


register = template.Library()


@register.filter
def get_student_score(qs, obj):
    if qs.filter(class_site=obj).exists():
        return qs.filter(class_site=obj)[0].current_score_average
    else:
        return 'N/A'


@register.filter
def get_class_score(qs):
    if qs.exists():
        return qs[0].current_score_average
    else:
        return 'N/A'


@register.filter
def get_student_class_status(qs, obj):
    return qs.filter(class_site=obj)[0].status


@register.filter
def jsonify(list):
    return mark_safe(json.dumps(list))


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except:
        return None
