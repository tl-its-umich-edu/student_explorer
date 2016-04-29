from django.views import generic
from django.shortcuts import render
from seumich.models import Student, Mentor, StudentCohortMentor


class IndexView(generic.View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AdvisorsListView(generic.ListView):
    template_name = 'seumich/advisor_list.html'
    model = Mentor
    context_object_name = 'advisors'


class AdvisorView(generic.ListView):
    template_name = 'seumich/advisor_detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class StudentsListView(generic.ListView):
    template_name = 'seumich/student_list.html'
    queryset = Student.objects.filter(mentor=2)
    context_object_name = 'students'
