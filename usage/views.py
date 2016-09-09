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


class StaffMemberRequiredMixin(object):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request,
                                                              *args,
                                                              **kwargs)


class ExtractWeek(Func):
    function = 'WEEK'
    template = '%(function)s(%(expressions)s, 3)'
    output_field = models.IntegerField()


class ExtractYear(Func):
    function = 'YEAR'
    output_field = models.IntegerField()


class UsageView(StaffMemberRequiredMixin, TemplateView):
    template_name = 'usage.html'

    def get_context_data(self, **kwargs):
        context = super(UsageView, self).get_context_data(**kwargs)
        usage_past_weeks = settings.USAGE_PAST_WEEKS
        startdate = timezone.now() - datetime.timedelta(weeks=usage_past_weeks)
        weeklydata = (Event.objects
                      .filter(
                          timestamp__gte=startdate
                      ).annotate(week=ExtractWeek('timestamp'),
                                 year=ExtractYear('timestamp'))
                      .values('week', 'year')
                      .annotate(usercount=Count('user', distinct=True),
                                idcount=Count('id'))
                      .order_by('week', 'year'))
        weekData = []
        weekData.append(
            {'key': 'Unique Users Count', 'values': list(
                weeklydata)}
        )
        context['weekData'] = weekData
        return context


class DownloadCsvView(View):

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def render_to_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="usernamelist.csv"')

        writer = csv.writer(response)
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
        pastAcadUsers = (Event.objects
                         .filter(
                             timestamp__lte=current_acad_year,
                             timestamp__gte=last_acad_year
                         )
                         .values_list('user__username', flat=True)
                         .distinct()
                         .order_by())
        writer.writerow(['UserName'])
        for user in pastAcadUsers:
            writer.writerow([user])
        return response

    def get(self, request, *args, **kwargs):
        return self.render_to_csv()
