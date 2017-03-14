from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseForbidden
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import FormView
from django.http import StreamingHttpResponse

from management.forms import CohortForm

from .models import Student, Mentor, Cohort, StudentCohortMentor

import csv


from django.contrib.auth import get_user_model
User = get_user_model()


class Echo(object):

    def write(self, value):
        return value


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
    paginate_by = 50


class CohortListView(ListView, StaffRequiredMixin):
    template_name = 'management/cohort_list.html'
    model = Cohort
    paginate_by = 50


class CohortDetailView(ListView, StaffRequiredMixin):
    template_name = 'management/cohort_detail.html'
    model = StudentCohortMentor
    paginate_by = 50

    def get_queryset(self):
        return (self.model.objects
                .filter(cohort__code=self.kwargs['code'])
                .prefetch_related('student',
                                  'cohort',
                                  'mentor'))


class BaseCohortView(FormView, StaffRequiredMixin):
    template_name = 'management/add_cohort.html'
    form_class = CohortForm
    success_url = '/manage/cohorts/'

    def process_form(self, form):
        members = form.cleaned_data['members']
        sniffer = csv.Sniffer()
        members = members.split('\r\n')
        dialect = sniffer.sniff(members[0])
        delimiter = dialect.delimiter
        for member in members:
            record = member.split(delimiter)
            student, created = Student.objects.get_or_create(
                username=record[0].strip())
            mentor, created = Mentor.objects.get_or_create(
                username=record[1].strip())
            cohort = form.save()
            (StudentCohortMentor
             .objects
             .get_or_create(student=student,
                            cohort=cohort,
                            mentor=mentor
                            ))


class AddCohortView(BaseCohortView):

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.process_form(form)
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(**kwargs))


class EditCohortView(BaseCohortView):

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Cohort, code=self.kwargs['code'])
        form = self.form_class(instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Cohort, code=self.kwargs['code'])
        form = self.form_class(request.POST or None, instance=instance)
        if form.is_valid():
            self.process_form(form)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class CohortListDownloadView(View, StaffRequiredMixin):

    def iter_csv(self, rows, header, file_obj):
        writer = csv.writer(file_obj, delimiter='\t')
        yield writer.writerow(header)
        for row in rows:
            yield writer.writerow(row)

    def render_to_csv(self, header, rows, fname):
        response = (StreamingHttpResponse(
            self.iter_csv(rows,
                          header,
                          Echo()),
            content_type="text/tab-separated-values"))
        response['Content-Disposition'] = 'attachment; filename="%s"' % fname
        return response

    def get(self, request, *args, **kwargs):
        headers = ('CohortCode', 'CohortDescription', 'CohortGroup')
        rows = (Cohort.objects
                .values_list('code',
                             'description',
                             'group'))
        return self.render_to_csv(headers,
                                  rows,
                                  'TLA_Cohort_USELAB.dat')


class CohortDetailDownloadView(CohortListDownloadView):

    def get(self, request, *args, **kwargs):
        headers = ('StudentUniqname', 'CohortCode', 'MentorUniqname')
        rows = (StudentCohortMentor.objects
                .values_list('student__username',
                             'cohort__code',
                             'mentor__username'))
        return self.render_to_csv(headers,
                                  rows,
                                  'TLA_StudentCohortMentor_USELAB.dat')
