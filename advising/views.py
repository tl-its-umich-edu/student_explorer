from advising.models import Advisor, Student
from advising.serializers import AdvisorSerializer, StudentSerializer
from rest_framework import viewsets

# from django.http import HttpResponse
# import json
#
# def advisor_list(request):
#     data = models.Advisor.objects.all()
#     return HttpResponse(json.dumps(data), content_type="application/json")


class AdvisorViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows advisors to be viewed.
    '''
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows students to be viewed.
    '''
    queryset = Student.objects.all()
    serializer_class = AdvisorSerializer
