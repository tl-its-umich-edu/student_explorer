from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import FormView, CreateView
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings

from management.forms import CohortForm, UserCreateForm

from .models import Student, Mentor, Cohort, StudentCohortMentor

import csv
import xlrd
import xlwt


from django.contrib.auth import get_user_model
User = get_user_model()


class StaffRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(StaffRequiredMixin, self).dispatch(request,
                                                        *args, **kwargs)


class StaffOrTokenRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        token = request.GET.get('token', None)
        if not token or token != settings.DOWNLOAD_TOKEN:
            if not request.user.is_staff:
                raise PermissionDenied
        return super(StaffOrTokenRequiredMixin, self).dispatch(request,
                                                               *args, **kwargs)


class IndexView(StaffRequiredMixin, TemplateView):
    template_name = 'management/index.html'


class CohortListView(StaffRequiredMixin, ListView):
    template_name = 'management/cohort_list.html'
    model = Cohort
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(CohortListView, self).get_context_data(**kwargs)
        context['query_term'] = self.all_cohorts
        context['show'] = 'all' if self.all_cohorts == 'all' else 'active'
        return context

    def get(self, request, *args, **kwargs):
        return super(CohortListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        self.all_cohorts = self.request.GET.get('show', None)
        if self.all_cohorts and self.all_cohorts == 'all':
            cohort_list = self.model.objects.all()
        else:
            cohort_list = self.model.objects.filter(active=True)
        return cohort_list

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code', None)
        action = request.POST.get('action', None)
        if code and action:
            if action == 'activate':
                instance = get_object_or_404(Cohort, code=code)
                instance.active = True
                instance.save()
            if action == 'deactivate':
                instance = get_object_or_404(Cohort, code=code)
                instance.active = False
                instance.save()
            if action == 'delete':
                instance = get_object_or_404(Cohort, code=code)
                instance.delete(request = request)
        return self.get(request, *args, **kwargs)


class UserListView(StaffRequiredMixin, ListView):
    template_name = 'management/user_list.html'
    model = User
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['query_term'] = self.all_users
        context['show'] = 'all' if self.all_users == 'all' else 'active'
        return context

    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        self.all_users = self.request.GET.get('show', None)
        if self.all_users and self.all_users == 'all':
            user_list = self.model.objects.all()
        else:
            user_list = self.model.objects.filter(is_active=True)
        return user_list

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        action = request.POST.get('action', None)
        if username and action:
            if action == 'activate':
                instance = get_object_or_404(User, username=username)
                instance.is_active = True
                instance.save()
            if action == 'deactivate':
                instance = get_object_or_404(User, username=username)
                instance.is_active = False
                instance.save()
        return self.get(request, *args, **kwargs)


class CohortMembersView(StaffRequiredMixin, ListView):
    template_name = 'management/cohort_members.html'
    model = StudentCohortMentor
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(CohortMembersView, self).get_context_data(**kwargs)
        context['cohort_code'] = self.kwargs['code']
        return context

    def get_queryset(self):
        return (self.model.objects
                .filter(cohort__code=self.kwargs['code'])
                .prefetch_related('student',
                                  'cohort',
                                  'mentor'))


class AddCohortView(StaffRequiredMixin, FormView):
    template_name = 'management/cohort_add.html'
    form_class = CohortForm
    success_url = '/manage/cohorts/'

    def process_form_members(self, form, members):
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

    def handle_uploaded_file(self, form, fname):
        xl_workbook = xlrd.open_workbook(file_contents=fname.read())
        xl_sheet = xl_workbook.sheet_by_index(0)
        for row_idx in range(0, xl_sheet.nrows):
            student, created = Student.objects.get_or_create(
                username=xl_sheet.cell(row_idx, 0).value.strip())
            mentor, created = Mentor.objects.get_or_create(
                username=xl_sheet.cell(row_idx, 1).value.strip())
            cohort = form.save()
            (StudentCohortMentor
             .objects
             .get_or_create(student=student,
                            cohort=cohort,
                            mentor=mentor
                            ))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            members = form.cleaned_data['members']
            if members:
                self.process_form_members(form, members)
            if len(request.FILES) != 0:
                self.handle_uploaded_file(form, request.FILES['excel_file'])
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(**kwargs))


class AddUserView(StaffRequiredMixin, CreateView):
    template_name = 'management/user_add.html'
    form_class = UserCreateForm
    success_url = '/manage/users/'


class CohortListDownloadView(StaffOrTokenRequiredMixin, View):

    class Echo(object):

        def write(self, value):
            return value

    def iter_qs(self, rows, header, file_obj):
        writer = csv.writer(file_obj, delimiter='\t')
        yield writer.writerow(header)
        for row in rows:
            yield writer.writerow(row)

    def render_to_csv(self, header, rows, fname):
        """A function that streams a large CSV file."""
        response = (StreamingHttpResponse(
            self.iter_qs(rows,
                         header,
                         self.Echo()),
            content_type="text/tab-separated-values"))
        response['Content-Disposition'] = 'attachment; filename="%s"' % fname
        return response

    def get(self, request, *args, **kwargs):
        headers = ('CohortCode', 'CohortDescription', 'CohortGroup')
        rows = (Cohort.objects
                .filter(active=True)
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
                .filter(cohort__active=True)
                .values_list('student__username',
                             'cohort__code',
                             'mentor__username').order_by('id'))
        return self.render_to_csv(headers,
                                  rows,
                                  'TLA_StudentCohortMentor_USELAB.dat')


class CohortMembersDownloadView(CohortListDownloadView):

    def render_to_excel(self, rows, fname):
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename="%s"' % fname

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Students')

        for idx, row in enumerate(rows):
            ws.write(idx, 0, row[0])
            ws.write(idx, 1, row[1])

        wb.save(response)
        return response

    def get(self, request, *args, **kwargs):
        rows = (StudentCohortMentor.objects
                .filter(cohort__code=self.kwargs['code'])
                .values_list('student__username',
                             'mentor__username').order_by('id'))
        return self.render_to_excel(
            rows,
            'StudentCohortMentor_' + self.kwargs['code'] + '.xls'
        )
