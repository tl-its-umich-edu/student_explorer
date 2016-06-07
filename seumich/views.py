from django.views import generic
from seumich.models import Student, Mentor, ClassSite, ClassSiteScore
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


def convert_to_pages(request, student_list, num_records, num_page_links):
    paginator = Paginator(student_list, num_records)
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    if not page:
        initial = 1
        final = 1 + num_page_links
    elif paginator.num_pages <= num_page_links:
        initial = 1
        final = 1 + paginator.num_pages
    else:
        current = int(page)
        initial = current - 2
        final = 1 + (current + 2)
        if current <= 2:
            initial = 1
            final = initial + num_page_links
        elif current + 2 >= paginator.num_pages:
            initial = paginator.num_pages - (num_page_links - 1)
            final = 1 + paginator.num_pages

    return students, range(initial, final)


class AdvisorsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'seumich/advisor_list.html'
    queryset = Mentor.objects.order_by('last_name')
    context_object_name = 'advisors'


class StudentsListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'seumich/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        query_user = self.request.GET.get('search', None)
        student_list = []
        context['studentListHeader'] = 'Search Students'

        if query_user:
            student_list = Student.objects.filter(
                Q(username__icontains=query_user) |
                Q(univ_id__icontains=query_user) |
                Q(first_name__icontains=query_user) |
                Q(last_name__icontains=query_user)
            ).order_by('last_name')

        # Pagination to break list into multiple pieces
        records = settings.PAGINATION_RECORDS_PER_PAGE
        links = settings.PAGINATION_NUM_PAGE_LINKS
        pages, ranges = convert_to_pages(
            self.request, student_list, records, links)
        context['students'] = pages
        context['loop_times'] = ranges
        context['query_user'] = query_user
        return context


class AdvisorView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'seumich/advisor_detail.html'

    def get_context_data(self, advisor, **kwargs):
        context = super(AdvisorView, self).get_context_data(**kwargs)

        mentor = get_object_or_404(Mentor, username=advisor)
        student_list = mentor.students.order_by('last_name')
        context['studentListHeader'] = mentor.first_name + \
            " " + mentor.last_name
        context['advisor'] = mentor

        # Pagination to break list into multiple pieces
        records = settings.PAGINATION_RECORDS_PER_PAGE
        links = settings.PAGINATION_NUM_PAGE_LINKS
        pages, ranges = convert_to_pages(
            self.request, student_list, records, links)
        context['students'] = pages
        context['loop_times'] = ranges
        return context


class StudentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'seumich/student_detail.html'

    def get_context_data(self, student, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        selected_student = get_object_or_404(Student, username=student)
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
                    class_site__code=class_site.code)
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
            {
                'key': 'Course Site Engagement',
                'values': activityData, 'color': '#a9bdab'
            })

        context['classSite'] = class_site
        context['scoreData'] = scoreData
        context['eventPercentileData'] = eventPercentileData
        context['assignments'] = student.studentclasssiteassignment_set.filter(
            class_site=class_site)
        return context
