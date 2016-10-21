from django.views.generic import View, TemplateView
from django.db import models
from django.db.models import Count, Func
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from tracking.models import Event
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse


import datetime
import csv


class ExtractUnixTimestamp(Func):
    function = 'UNIX_TIMESTAMP'
    template = '%(function)s(%(expressions)s)'
    output_field = models.IntegerField()


class ExtractDate(Func):
    function = 'DATE'
    template = '%(function)s(%(expressions)s)'
    output_field = models.DateField()


class ExtractSubString(Func):
    function = 'SUBSTRING'
    template = '%(function)s(%(expressions)s, 11)'
    output_field = models.CharField()


class ExtractStudent(Func):
    function = 'SUBSTRING_INDEX'
    template = '%(function)s(%(expressions)s, "/", 1)'
    output_field = models.CharField()


class StaffMemberRequiredMixin(object):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request,
                                                              *args,
                                                              **kwargs)


class PastDataMixin(object):

    def __init__(self):
        self.current = None
        self.last = None

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def get_past_acad_year(self):

        sept_current = datetime.datetime(timezone.now().year,
                                         month=9,
                                         day=1)
        sept_current = self.next_weekday(sept_current, 0)
        sept_last = datetime.datetime(timezone.now().year - 1,
                                      month=9,
                                      day=1)
        sept_last = self.next_weekday(sept_last, 0)
        current_acad_year = timezone.make_aware(
            sept_current,
            timezone.get_current_timezone())
        last_acad_year = timezone.make_aware(
            sept_last,
            timezone.get_current_timezone())

        self.current = current_acad_year
        self.last = last_acad_year

    def get_past_users(self):
        self.get_past_acad_year()
        pastUsers = (Event.objects
                     .filter(
                         timestamp__lte=self.current,
                         timestamp__gte=self.last
                     )
                     .values_list('user__username', flat=True)
                     .distinct()
                     .order_by())
        return pastUsers

    def get_past_students(self):
        self.get_past_acad_year()
        pastStudents = (Event.objects
                        .filter(
                            note__regex=r'^/students/[a-zA-Z]+/',
                            timestamp__lte=self.current,
                            timestamp__gte=self.last
                        )
                        .annotate(student=ExtractStudent(
                            ExtractSubString('note')))
                        .values_list('student', flat=True)
                        .distinct()
                        .order_by())
        return pastStudents


class UsageView(StaffMemberRequiredMixin, PastDataMixin, TemplateView):
    template_name = 'usage.html'

    def get_daily_user_data(self, startdate):
        dailydata = (Event.objects
                     .filter(
                         timestamp__gte=startdate
                     )
                     .annotate(
                         date=ExtractUnixTimestamp(
                             ExtractDate('timestamp')))
                     .values('date')
                     .annotate(count=Count('user', distinct=True))
                     .order_by())
        return dailydata

    def get_daily_student_data(self, startdate):
        dailydata = (Event.objects
                     .filter(
                         note__regex=r'^/students/[a-zA-Z]+/',
                         timestamp__gte=startdate
                     )
                     .annotate(
                         date=ExtractUnixTimestamp(
                             ExtractDate('timestamp')))
                     .values('date')
                     .annotate(
                         count=Count(
                             ExtractStudent(
                                 ExtractSubString('note')),
                             distinct=True))
                     .order_by())
        return dailydata

    def get_context_data(self, **kwargs):
        context = super(UsageView, self).get_context_data(**kwargs)
        usage_past_weeks = settings.USAGE_PAST_WEEKS
        startdate = timezone.now() - datetime.timedelta(weeks=usage_past_weeks)
        # get next monday and set time to zero
        startdate = startdate + datetime.timedelta(
            days=(7 - startdate.weekday())
        )
        startdate = startdate.replace(hour=0, minute=0, second=0)

        dailyuserdata = {'key': 'Unique Users Count', 'values': list(
            self.get_daily_user_data(startdate)), 'color': '#7777ff',
            'area': 'true'}
        dailystudentdata = {'key': 'Unique Students Viewed', 'values': list(
            self.get_daily_student_data(startdate)), 'color': '#ff7f0e'}

        dailyData = []
        dailyData.append(dailystudentdata)
        dailyData.append(dailyuserdata)

        context['dailyData'] = dailyData
        context['usersCount'] = self.get_past_users().count()
        context['studentsCount'] = self.get_past_students().count()
        return context


class DownloadCsvView(View, PastDataMixin):

    def render_to_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="usernamelist.csv"')

        writer = csv.writer(response)
        writer.writerow(['UserName'])
        for user in self.get_past_users():
            writer.writerow([user])
        return response

    def get(self, request, *args, **kwargs):
        return self.render_to_csv()
