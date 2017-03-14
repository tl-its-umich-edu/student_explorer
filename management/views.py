from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseForbidden
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

from management.forms import CohortForm

from .models import Student, Advisor, Cohort, StudentAdvisorCohort

import csv


from django.contrib.auth import get_user_model
User = get_user_model()


class StaffRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden

        return super(StaffRequiredMixin, self).dispatch(request,
                                                        *args, **kwargs)


class IndexView(TemplateView, StaffRequiredMixin):
    template_name = 'management/index.html'


class UserListView(ListView, StaffRequiredMixin):
    template_name = 'management/user_list.html'
    model = User


class CohortListView(ListView, StaffRequiredMixin):
    template_name = 'management/cohort_list.html'
    model = Cohort


class AddCohortView(FormView, StaffRequiredMixin):
    template_name = 'management/add_cohort.html'
    form_class = CohortForm
    success_url = '/manage/cohorts/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            members = form.cleaned_data['members']
            sniffer = csv.Sniffer()
            members = members.split('\r\n')
            dialect = sniffer.sniff(members[0])
            delimiter = dialect.delimiter
            for member in members:
                record = member.split(delimiter)
                student, created = Student.objects.get_or_create(
                    username=record[0])
                advisor, created = Advisor.objects.get_or_create(
                    username=record[1])
                cohort = form.save()
                (StudentAdvisorCohort
                 .objects
                 .get_or_create(student=student,
                                advisor=advisor,
                                cohort=cohort))
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(**kwargs))
