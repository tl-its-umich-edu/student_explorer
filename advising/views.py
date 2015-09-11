from advising import models
from django.http import HttpResponse
from django.views.generic import View
import json


def advisor_list(request):
    data = models.Advisor.objects.all()
    return HttpResponse(json.dumps(data), content_type="application/json")


class Courses(View):

    def get(self, request):
        data = models.Course.objects.values_list('course', flat=True)
        return HttpResponse(json.dumps(map(unicode, data)),
                            content_type="application/json")

courses = Courses.as_view()
