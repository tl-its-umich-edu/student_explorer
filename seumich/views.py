from django.views import generic
from seumich.models import Student, Mentor, ClassSite
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


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
        mentor = Mentor.objects.get(username=advisor)
        context['students'] = mentor.students.order_by('last_name')
        context['studentListHeader'] = mentor.first_name + " " + mentor.last_name
        context['advisor'] = mentor
        return context


class StudentsListView(generic.TemplateView):
    template_name = 'seumich/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            mentor = Mentor.objects.get(username=user)
            context['students'] = mentor.students.order_by('last_name')
            context['studentListHeader'] = mentor.first_name + " " + mentor.last_name
        return context


class StudentView(generic.TemplateView):
    template_name = 'seumich/student.html'

    def get_context_data(self, student, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        selected_student =  Student.objects.get(username=student)
        context['student'] = selected_student
        context['advisors'] = selected_student.mentors.all()
        context['classSites'] = selected_student.class_sites.all()
        return context


class StudentClassSiteView(StudentView):
    template_name = 'seumich/student_class_site_detail.html'

    def get_class_history(self, student, classcode, format=None):
        student = get_object_or_404(Student, username=student)
        class_site = get_object_or_404(ClassSite, code=classcode)

        try:
            term = class_site.terms.get()
        except ObjectDoesNotExist:
            raise Http404()

        events = class_site.weeklystudentclasssiteevent_set.filter(
                student=student)

        student_scores = class_site.weeklystudentclasssitescore_set.filter(
                student=student)
        student_statuses = class_site.weeklystudentclasssitestatus_set.filter(
                student=student)

        class_scores = class_site.weeklyclasssitescore_set.all()

        todays_week_end_date = term.todays_week_end_date()

        history = []
        week_number = 0
        for week_end_date in term.week_end_dates():
            entry = {}
            entry['week_end_date'] = str(week_end_date)

            week_number += 1
            entry['week_number'] = week_number

            try:
                event = events.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                # entry['event_count'] = None
                # entry['event_percentile_rank'] = None
                pass
            else:
                entry['event_count'] = event.event_count
                entry['event_percentile_rank'] = event.percentile_rank

            try:
                score = student_scores.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                # entry['score'] = None
                pass
            else:
                entry['score'] = score.score

            try:
                status = student_statuses.get(
                        week_end_date=week_end_date)
            except ObjectDoesNotExist:
                    # entry['status'] = None
                pass
            else:
                entry['status'] = str(status.status.description)
                entry['status_order'] = status.status.order

            try:
                score = class_scores.get(week_end_date=week_end_date)
            except ObjectDoesNotExist:
                    # entry['class_score'] = None
                pass
            else:
                entry['class_score'] = score.score

            if week_end_date == todays_week_end_date:
                entry['this_week'] = True
                entry['score'] = (student.studentclasssitescore_set
                                      .get(class_site=class_site)
                                      .current_score_average)

                todaysStatus = student.studentclasssitestatus_set.get(class_site=class_site)
                entry['status'] = str(todaysStatus.status.description)
                entry['status_order'] = todaysStatus.status.order

                class_site_score = ClassSiteScore.objects.get(class_site__code=code)
                entry['class_score'] = class_site_score.current_score_average
            history.append(entry)
        return history

    def get_context_data(self, student, classcode, **kwargs):
        context = super(StudentClassSiteView, self).get_context_data(student, **kwargs)
        context['classSite'] = ClassSite.objects.get(code=classcode)
        classSiteHistory = self.get_class_history(student, classcode)
        studentData = []
        classData = []
        for item in classSiteHistory:
            if 'week_number' in item and 'score' in item:
                studentData.append([item['week_number'], item['score']])
            if 'week_number' in item and 'class_score' in item:
                classData.append([item['week_number'], item['class_score']])
        scoreData = []
        scoreData.append({'key': 'Student', 'values': studentData, 'color': '#255c91'})
        scoreData.append({'key': 'Class', 'values': classData, 'color': '#F0D654'})
        context['scoreData'] = scoreData
        return context
