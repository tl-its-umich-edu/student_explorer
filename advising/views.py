from advising.models import (Advisor, Student, Mentor, ClassSite,
                             StudentClassSiteStatus,
                             StudentClassSiteAssignment)
from advising.serializers import (AdvisorSerializer,
                                  MentorSerializer,
                                  StudentSerializer,
                                  StudentClassSiteSerializer,
                                  StudentClassSiteAssignmentSerializer,
                                  StudentAdvisorSerializer,
                                  StudentMentorSerializer)
from advising.mixins import MultipleFieldLookupMixin
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'apiRootUrl': reverse('advising-api-root',
                              request=request, format=format),
        'advisorsUrl': reverse('advisor-list',
                               request=request, format=format),
        'mentorsUrl': reverse('mentor-list',
                              request=request, format=format),
        'studentsUrl': reverse('student-list',
                               request=request, format=format),
        'userInfoUrl': reverse('current-user-detail',
                               request=request, format=format),
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


class AdvisorStudentList(generics.ListAPIView):
    '''
    API endpoint that lists an advisor's students.
    '''
    queryset = Advisor.objects.all()
    serializer_class = StudentSerializer
    # lookup_field = 'username'

    def get_queryset(self):
        return (
            get_object_or_404(Advisor, username=self.kwargs['username'])
            .students.all()
        )


class MentorList(generics.ListAPIView):
    '''
    API endpoint that lists Mentors.
    '''
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    lookup_field = 'username'


class MentorDetail(generics.RetrieveAPIView):
    '''
    API endpoint that shows advisor details.
    '''
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    lookup_field = 'username'


class MentorStudentList(generics.ListAPIView):
    '''
    API endpoint that lists an advisor's students.
    '''
    queryset = Mentor.objects.all()
    serializer_class = StudentSerializer
    # lookup_field = 'username'

    def get_queryset(self):
        return (
            get_object_or_404(Mentor, username=self.kwargs['username'])
            .students.all()
        )


class StudentList(generics.ListAPIView):
    '''
    API endpoint that lists students.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'username'
    search_fields = ('username', 'univ_id', 'first_name', 'last_name')


class StudentDetail(generics.RetrieveAPIView):
    '''
    API endpoint that shows student details.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'username'


class StudentAdvisorList(generics.ListAPIView):
    '''
    API endpoint that lists a student's advisors.
    '''
    serializer_class = StudentAdvisorSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return (
            get_object_or_404(Student, username=self.kwargs['username'])
            .advisors
        )


class StudentMentorList(generics.ListAPIView):
    '''
    API endpoint that lists a student's mentors.
    '''
    queryset = Student.objects.all()
    serializer_class = StudentMentorSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return (
            get_object_or_404(Student, username=self.kwargs['username'])
            .studentcohortmentor_set.all()
        )


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


class StudentClassSiteHistoryList(APIView):

    def get(self, request, username, code, format=None):
        student = Student.objects.get(username=username)
        class_site = ClassSite.objects.get(code=code)
        term = class_site.terms.get()  # FIXME

        events = class_site.weeklystudentclasssiteevent_set.filter(
            student=student)

        student_scores = class_site.weeklystudentclasssitescore_set.filter(
            student=student)
        student_statuses = class_site.weeklystudentclasssitestatus_set.filter(
            student=student)

        class_scores = class_site.weeklyclasssitescore_set.all()

        history = []
        week_number = 0
        for week_end_date in term.week_end_dates():
            entry = {}
            entry['week_end_date'] = str(week_end_date)

            week_number += 1
            entry['week_number'] = week_number

            try:
                event = events.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                # entry['event_count'] = None
                # entry['event_percentile_rank'] = None
                pass
            else:
                entry['event_count'] = event.event_count
                entry['event_percentile_rank'] = event.percentile_rank

            try:
                score = student_scores.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                # entry['score'] = None
                pass
            else:
                entry['score'] = score.score

            try:
                status = student_statuses.get(
                    week_end_date=week_end_date)
            except ObjectDoesNotExist:
                # entry['status'] = None
                pass
            else:
                entry['status'] = str(status.status)

            try:
                score = class_scores.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                # entry['class_score'] = None
                pass
            else:
                entry['class_score'] = score.score

            history.append(entry)
        return Response(history)
