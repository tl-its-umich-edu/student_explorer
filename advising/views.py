from advising.models import Advisor, Student
from advising.serializers import (AdvisorSerializer, StudentSummarySerializer,
                                  StudentFullSerializer,
                                  StudentAdvisorsSerializer,
                                  AdvisorStudentsSerializer)
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
    API endpoint that lists advisors.
    '''
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    lookup_field = 'username'


class AdvisorDetail(generics.RetrieveAPIView):
    '''
    API endpoint that shows advisor details.
    '''
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        resp = self.retrieve(request, *args, **kwargs)
        resp.data['students_url'] = reverse('advisor-students-list',
                                            request=request, kwargs=kwargs)
        return resp


class AdvisorStudentsList(generics.ListAPIView):
    '''
    API endpoint that lists an advisor's students.
    '''
    queryset = Advisor.objects.all()
    serializer_class = StudentSummarySerializer
    # lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        self.queryset = (
            Advisor.objects
            .get(username=kwargs['username'])
            .studentadvisorrole_set.all()
        )
        return self.list(request, *args, **kwargs)


class StudentList(generics.ListAPIView):
    '''
    API endpoint that lists students.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSummarySerializer
    lookup_field = 'username'


class StudentDetail(generics.RetrieveAPIView):
    '''
    API endpoint that shows student details.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSummarySerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        resp = self.retrieve(request, *args, **kwargs)
        resp.data['advisors_url'] = reverse('student-advisors-list',
                                            request=request, kwargs=kwargs)
        resp.data['student_full_url'] = reverse('student-full-detail',
                                            request=request, kwargs=kwargs)
        return resp


class StudentFullDetail(generics.RetrieveAPIView):
    '''
    API endpoint that shows student details.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentFullSerializer
    lookup_field = 'username'


class StudentAdvisorsList(generics.ListAPIView):
    '''
    API endpoint that lists a student's advisors.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentAdvisorsSerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        self.queryset = (
            Student.objects
            .get(username=kwargs['username'])
            .studentadvisorrole_set.all()
        )
        return self.list(request, *args, **kwargs)
