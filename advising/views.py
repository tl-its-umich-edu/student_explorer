from advising.models import Advisor, Student
from advising.serializers import (AdvisorSerializer, StudentSerializer,
                                  AdvisorFullSerializer,
                                  StudentFullSerializer)
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'advisors': reverse('advisor-list', request=request, format=format),
        'students': reverse('student-list', request=request, format=format),
    })


class AdvisorList(generics.ListAPIView):
    '''
    API endpoint that allows advisors to be viewed.
    '''
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    lookup_field = 'username'


class AdvisorDetail(generics.RetrieveAPIView):
    '''
    API endpoint that allows advisors to be viewed.
    '''
    queryset = Advisor.objects.all()
    serializer_class = AdvisorFullSerializer
    lookup_field = 'username'


class StudentList(generics.ListAPIView):
    '''
    API endpoint that allows advisors to be viewed.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'username'


class StudentDetail(generics.RetrieveAPIView):
    '''
    API endpoint that allows advisors to be viewed.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentFullSerializer
    lookup_field = 'username'
