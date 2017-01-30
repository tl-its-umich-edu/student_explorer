from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseForbidden
from django.views.generic import TemplateView, ListView


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
    template_name = 'management/index.html'


class CohortListView(ListView, StaffRequiredMixin):
    template_name = 'management/index.html'
