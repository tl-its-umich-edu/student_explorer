from django.views import generic
from django.shortcuts import render
from seumich.models import Student, Mentor, StudentCohortMentor


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class AdvisorsListView(generic.ListView):
    template_name = 'seumich/advisor_list.html'
    model = Mentor
    context_object_name = 'advisors'


def getStudents(mentor):
    students = []
    for row in mentor.studentcohortmentor_set.all():
        students.append(row.student)
    students.sort(key=lambda x: x.last_name.lower())
    return students


class AdvisorView(generic.TemplateView):
    template_name = 'seumich/advisor_detail.html'

    def get_context_data(self, advisor, **kwargs):
        context = super(AdvisorView, self).get_context_data(**kwargs)
        mentor = Mentor.objects.get(username=advisor)
        context['students'] = getStudents(mentor)
        context['studentListHeader'] = mentor.first_name + " " + mentor.last_name
        context['advisor'] = mentor
        return context


class StudentsListView(generic.TemplateView):
    template_name = 'seumich/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        mentor = Mentor.objects.get(username=self.request.user)
        context['students'] = getStudents(mentor)
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
