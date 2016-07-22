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
def get_student_score(qs, obj):
    if qs.filter(class_site=obj).exists():
        avg_score = qs.filter(class_site=obj)[0].current_score_average
        if avg_score is None:
            return 'N/A'
        else:
            return avg_score
    else:
        return 'N/A'


@register.filter
def get_class_score(qs):
    if qs.exists():
        avg_score = qs[0].current_score_average
        if avg_score is None:
            return 'N/A'
        else:
            return avg_score
    else:
        return 'N/A'


@register.filter
def get_student_class_status(qs, obj):
    return str(qs.filter(class_site=obj)[0].status)


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
        return value * arg
    except:
        return None


@register.filter
def get_student_cohort(qs, obj):
    if qs.filter(student=obj).exists():
        return qs.filter(student=obj)[0].cohort
    else:
        return ''


@register.filter
def status_to_text(value, arg=None):
    result = ''
    value = str(value)
    if arg:
        result = str(arg) + ': ' + result
    if value == 'Green':
        return result + 'Encourage'
    elif value == 'Yellow':
        return result + 'Explore'
    elif value == 'Red':
        return result + 'Engage'
    elif value == 'Not Applicable':
        return result + 'No data'
    else:
        return result + ''


@register.simple_tag
def get_bar_widths(student_score, class_score):
    widths_dict = {}
    if student_score == 'N/A':
        student_score = 0
    if class_score == 'N/A':
        class_score = 0
    if class_score > 100.0 and student_score < class_score:
        widths_dict['student_score'] = student_score*100.0/class_score
        widths_dict['class_score'] = 100
    elif student_score > 100.0 and class_score < student_score:
        widths_dict['student_score'] = 100
        widths_dict['class_score'] = class_score*100.0/student_score
    else:
        widths_dict['student_score'] = student_score
        widths_dict['class_score'] = class_score
    return widths_dict
