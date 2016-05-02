from django.views import generic
from django.shortcuts import render
from seumich.models import Student, Mentor, StudentCohortMentor


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class AdvisorsListView(generic.ListView):
    template_name = 'seumich/advisor_list.html'
    model = Mentor
    context_object_name = 'advisors'


class AdvisorView(generic.TemplateView):
    template_name = 'seumich/advisor_detail.html'

    def get_context_data(self, advisor, **kwargs):
        context = super(AdvisorView, self).get_context_data(**kwargs)
        context['advisor'] = Mentor.objects.get(username=advisor)
        return context


class StudentsListView(generic.TemplateView):
    template_name = 'seumich/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        students = []
        if 'advisor' in self.request.GET:
            user = self.request.GET['advisor']
        else:
            user = self.request.user
        mentor = Mentor.objects.get(username=user)
        for row in mentor.studentcohortmentor_set.all():
            students.append(row.student)
        context['students'] = students
        context['studentListHeader'] = mentor.first_name + " " + mentor.last_name
        return context


class StudentView(generic.TemplateView):
    template_name = 'seumich/student_detail.html'

    def get_context_data(self, student, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        advisors = []
        selected_student =  Student.objects.get(username=student)
        student_mentors = selected_student.studentcohortmentor_set.all()
        for row in student_mentors:
            advisors.append(row.mentor)
        context['advisors'] = advisors
        return context
