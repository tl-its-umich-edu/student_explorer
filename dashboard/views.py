from django.views.generic import View, TemplateView

# Create your views here.

class Dashboard(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        return context

dashboard = Dashboard.as_view()

class StudentPage(TemplateView):
    template_name = "dashboard/studentPage.html"

    def get_context_data(self, **kwargs):
        context = super(StudentPage, self).get_context_data(**kwargs)
        return context

studentPage = StudentPage.as_view()

class AdvisorDashboard(TemplateView):
    template_name = "dashboard/advisorDashboard.html"

    def get_context_data(self, **kwargs):
        context = super(AdvisorDashboard, self).get_context_data(**kwargs)
        return context

advisorDashboard = AdvisorDashboard.as_view()