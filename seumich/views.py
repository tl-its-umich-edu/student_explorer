from django.views import generic
from seumich.models import Student, Mentor, ClassSite
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class AdvisorsListView(generic.ListView):
    template_name = 'seumich/advisor_list.html'
    queryset = Mentor.objects.order_by('last_name')
    context_object_name = 'advisors'


class AdvisorView(generic.TemplateView):
    template_name = 'seumich/advisor_detail.html'

    def get_context_data(self, advisor, **kwargs):
        context = super(AdvisorView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            mentor = Mentor.objects.get(username=advisor)
            context['students'] = mentor.students.order_by('last_name')
            context['studentListHeader'] = mentor.first_name + \
                " " + mentor.last_name
            context['advisor'] = mentor
        return context


class StudentsListView(generic.TemplateView):
    template_name = 'seumich/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        user = self.request.user
        query_user = self.request.GET.get('search', None)
        if user.is_authenticated():
            mentor = Mentor.objects.get(username=user)
            context['students'] = mentor.students.order_by('last_name')
            context['studentListHeader'] = mentor.first_name + \
                " " + mentor.last_name
        if query_user:
            context['students'] = Student.objects.filter(Q(username__icontains=query_user) | Q(univ_id__icontains=query_user) | Q(
                first_name__icontains=query_user) | Q(last_name__icontains=query_user)).order_by('last_name')
            context['studentListHeader'] = None
        return context


class StudentView(generic.TemplateView):
    template_name = 'seumich/student.html'

    def get_context_data(self, student, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        selected_student = Student.objects.get(username=student)
        context['student'] = selected_student
        context['advisors'] = selected_student.mentors.all()
        context['classSites'] = selected_student.class_sites.all()
        return context


class StudentClassSiteView(StudentView):
    template_name = 'seumich/student_class_site_detail.html'

    def get_class_history(self, student, class_site, format=None):

        studentData = []
        classData = []
        activityData = []

        try:
            term = class_site.terms.get()
        except:
            return studentData, classData, activityData

        events = class_site.weeklystudentclasssiteevent_set.filter(
            student=student)
        student_scores = class_site.weeklystudentclasssitescore_set.filter(
            student=student)
        class_scores = class_site.weeklyclasssitescore_set.all()
        todays_week_end_date = term.todays_week_end_date()

        week_number = 0

        for week_end_date in term.week_end_dates():
            tempStudentData = []
            tempClassData = []
            tempActivityData = []
            week_number += 1

            tempStudentData.append(week_number)
            tempClassData.append(week_number)
            tempActivityData.append(week_number)

            try:
                event = events.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                pass
            else:
                tempActivityData.append(round(event.percentile_rank * 100))

            try:
                score = student_scores.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                pass
            else:
                tempStudentData.append(score.score)

            try:
                score = class_scores.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                pass
            else:
                tempClassData.append(score.score)

            if week_end_date == todays_week_end_date:
                tempStudentData.append(student.studentclasssitescore_set
                                       .get(class_site=class_site)
                                       .current_score_average)

                class_site_score = ClassSiteScore.objects.get(
                    class_site__code=code)
                tempClassData.append(class_site_score.current_score_average)

            studentData.append(tempStudentData)
            classData.append(tempClassData)
            activityData.append(tempActivityData)

        return studentData, classData, activityData

    def get_context_data(self, student, classcode, **kwargs):
        context = super(StudentClassSiteView, self).get_context_data(
            student, **kwargs)
        student = get_object_or_404(Student, username=student)
        class_site = get_object_or_404(ClassSite, code=classcode)
        studentData, classData, activityData = self.get_class_history(
            student, class_site)

        scoreData = []
        eventPercentileData = []
        scoreData.append(
            {'key': 'Student', 'values': studentData, 'color': '#255c91'})
        scoreData.append(
            {'key': 'Class', 'values': classData, 'color': '#F0D654'})
        eventPercentileData.append(
            {'key': 'Course Site Engagement', 'values': activityData, 'color': '#a9bdab'})

        context['classSite'] = class_site
        context['scoreData'] = scoreData
        context['eventPercentileData'] = eventPercentileData
        context['assignments'] = student.studentclasssiteassignment_set.filter(
            class_site=class_site)
        return context
