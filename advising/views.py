from advising.models import (Advisor, Student, ClassSite,
                             StudentClassSiteStatus,
                             StudentClassSiteAssignment)
from advising.serializers import (AdvisorSerializer, StudentSummarySerializer,
                                  StudentFullSerializer,
                                  StudentClassSiteSerializer,
                                  StudentClassSiteAssignmentSerializer,
                                  StudentAdvisorsSerializer)
from advising.mixins import MultipleFieldLookupMixin
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings

import logging

logger = logging.getLogger(__name__)


@api_view(('GET',))
def api_root(request, format=None):
    if hasattr(settings, 'CUSTOM_LOGIN_URL'):
        login_url = settings.CUSTOM_LOGIN_URL
    else:
        login_url = reverse('rest_framework:login',
                            request=request, format=format)

    if hasattr(settings, 'CUSTOM_LOGOUT_URL'):
        logout_url = settings.CUSTOM_LOGOUT_URL
    else:
        logout_url = reverse('rest_framework:logout',
                             request=request, format=format)

    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = None

    return Response({
        'advisors': reverse('advisor-list', request=request, format=format),
        'students': reverse('student-list', request=request, format=format),
        'username': username,
        'debug': settings.DEBUG,
        'login': login_url,
        'logout': logout_url,
    })


@api_view(('GET',))
def config(request, format=None):
    '''
    Config values for the client-side application.
    '''
    return Response({
        'static_url': request.build_absolute_uri(settings.STATIC_URL),
        'api_url': reverse('api_url', request=request),
        'username': request.user.username,
        'debug': settings.DEBUG,
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
        if (('username' in self.kwargs.keys() and
             self.kwargs['username'] == 'me')):
            self.kwargs['username'] = request.user.username
            kwargs['username'] = request.user.username
        resp = self.retrieve(request, *args, **kwargs)
        return resp


class AdvisorStudentsList(generics.ListAPIView):
    '''
    API endpoint that lists an advisor's students.
    '''
    queryset = Advisor.objects.all()
    serializer_class = StudentSummarySerializer
    # lookup_field = 'username'

    def get_queryset(self):
        return (
            Advisor.objects
            .get(username=self.kwargs['username'])
            .students.all()
        )


class StudentList(generics.ListAPIView):
    '''
    API endpoint that lists students.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSummarySerializer
    lookup_field = 'username'
    search_fields = ('username', 'univ_id', 'first_name', 'last_name')


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


class StudentClassSiteList(MultipleFieldLookupMixin, generics.ListAPIView):
    '''
    API endpoint that lists a student's class sites.
    '''
    serializer_class = StudentClassSiteSerializer
    queryset = StudentClassSiteStatus.objects.all()
    lookup_params = {
        'student__username': 'username',
    }


class StudentClassSiteDetail(MultipleFieldLookupMixin,
                             generics.RetrieveAPIView):
    '''
    API endpoint that lists a student's class site detail.
    '''
    serializer_class = StudentClassSiteSerializer
    queryset = StudentClassSiteStatus.objects.all()
    lookup_params = {
        'student__username': 'username',
        'class_site__code': 'code',
    }


class StudentClassSiteAssignmentList(MultipleFieldLookupMixin,
                                     generics.ListAPIView):
    '''
    API endpoint that lists a student's class sites.
    '''
    serializer_class = StudentClassSiteAssignmentSerializer
    queryset = StudentClassSiteAssignment.objects.all()
    lookup_params = {
        'student__username': 'username',
        'class_site__code': 'code',
    }
