from django.views import generic
from seumich.models import Student, Mentor


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
        mentor = Mentor.objects.get(username=advisor)
        context['students'] = mentor.students.all()
        context['studentListHeader'] = mentor.first_name + " " + mentor.last_name
        context['advisor'] = mentor
        return context


class StudentsListView(generic.TemplateView):
    template_name = 'seumich/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        mentor = Mentor.objects.get(username=self.request.user)
        context['students'] = mentor.students.all()
        context['studentListHeader'] = mentor.first_name + " " + mentor.last_name
        return context


class StudentView(generic.TemplateView):
    template_name = 'seumich/student.html'

    def get_context_data(self, student, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        classScores = {}
        studentScores = {}
        selected_student =  Student.objects.get(username=student)
        context['student'] = selected_student
        context['advisors'] = selected_student.mentors.all()
        context['classSites'] = selected_student.class_sites.all()
        for classSite in selected_student.class_sites.all():
            classScore = classSite.classsitescore_set.all()
            studentScore = selected_student.studentclasssitescore_set.filter(class_site=classSite)
            if classScore:
                classScores[classSite.id] = classScore[0].current_score_average
            else:
                classScores[classSite.id] = 'N/A'
            if studentScore:
                studentScores[classSite.id] = studentScore[0].current_score_average
            else:
                studentScores[classSite.id] = 'N/A'
        context['classScores'] = classScores
        context['studentScores'] = studentScores
        print context
        return context
