from django import template


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
