from django.views.generic import View, ListView, TemplateView
from seumich.models import (Student, Mentor, Cohort, ClassSite,
                            ClassSiteScore,
                            StudentCohortMentor,
                            StudentClassSiteStatus,
                            StudentClassSiteScore)
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q, Prefetch, Value as V
from django.db.models.functions import Concat
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from tracking.utils import UserLogPageViewMixin

import operator
import logging

from decouple import config
from functools import reduce

User = get_user_model()
logger = logging.getLogger(__name__)

class AdvisorsListView(LoginRequiredMixin, UserLogPageViewMixin, ListView):
    template_name = 'seumich/advisor_list.html'
    # Filtering for id >= 0 eliminates "Bad Value"-type results.
    queryset = Mentor.objects.filter(id__gte=0).order_by('last_name')
    context_object_name = 'advisors'


class CohortsListView(LoginRequiredMixin, UserLogPageViewMixin, ListView):
    template_name = 'seumich/cohort_list.html'
    # Filtering for id >= 0 eliminates "Bad Value"-type results.
    queryset = Cohort.objects.filter(id__gte=0)
    context_object_name = 'cohorts'

class StudentsListView(LoginRequiredMixin, UserLogPageViewMixin, ListView):
    template_name = 'seumich/student_list.html'
    context_object_name = 'students'

    def get(self, request):
        univ_id = self.request.GET.get('univ_id', None)
        if univ_id:
            try:
                student = get_object_or_404(Student, univ_id=univ_id)
                return redirect('seumich:student', student.username)
            except MultipleObjectsReturned:
                logger.info('Multiple students with the same univ_id (%s)'
                            % univ_id)
        return super(StudentsListView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        context['studentListHeader'] = 'Search Students'
        context['query_user'] = self.query_user
        return context

    def get_queryset(self):
        self.query_user = self.request.GET.get('search', None)
        self.univ_id = self.request.GET.get('univ_id', None)
        student_list = []
        if self.query_user:
            # Filtering for id >= 0 eliminates "Bad Value"-type results.
            q_list = [Q(username__icontains=self.query_user)]
            q_list += [Q(univ_id__icontains=self.query_user)]
            q_list += [Q(first_name__icontains=self.query_user)]
            q_list += [Q(last_name__icontains=self.query_user)]
            q_list += [Q(full_name__icontains=self.query_user)]
            student_list = (Student.objects.filter(id__gte=0)
                            .annotate(full_name=(Concat('first_name', V(' '), 'last_name')))
                            .filter(reduce(operator.or_, q_list))
                            .order_by('last_name').distinct())
            student_list = student_list.prefetch_related(
                'studentclasssitestatus_set__status',
                'studentclasssitestatus_set__class_site',
                'cohorts')
        elif self.univ_id:
            student_list = Student.objects.filter(id__gte=0).filter(
                univ_id=self.univ_id)
            student_list = student_list.prefetch_related(
                'studentclasssitestatus_set__status',
                'studentclasssitestatus_set__class_site',
                'cohorts')
            messages.add_message(
                self.request,
                messages.WARNING,
                'Multiple students with the same univ_id (%s)' % self.univ_id)
        return student_list


class AdvisorView(LoginRequiredMixin, UserLogPageViewMixin, ListView):
    template_name = 'seumich/advisor_detail.html'
    context_object_name = 'students'

    def get_queryset(self):
        self.mentor = None
        try:
            self.mentor = Mentor.objects.get(username=self.kwargs['advisor'])
            student_list = self.mentor.students.order_by('last_name').distinct()
            student_list = student_list.prefetch_related(
                'studentclasssitestatus_set__status',
                'studentclasssitestatus_set__class_site',
                'cohorts'
            )
        except ObjectDoesNotExist:
            student_list = []
        return student_list

    def get_context_data(self, **kwargs):
        context = super(AdvisorView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['advisor'])
        if self.mentor is not None:
            context['studentListHeader'] = " ".join([self.mentor.first_name, self.mentor.last_name])
            context['advisor'] = self.mentor
        else:
            context['studentListHeader'] = " ".join([user.first_name, user.last_name])
            context['advisor'] = user
        return context


class CohortView(LoginRequiredMixin, UserLogPageViewMixin, ListView):
    template_name = 'seumich/cohort_detail.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super(CohortView, self).get_context_data(**kwargs)
        context['studentListHeader'] = self.cohort.description
        context['cohort'] = self.cohort
        return context

    def get_queryset(self):
        self.cohort = get_object_or_404(Cohort, code=self.kwargs['code'])
        student_list = Student.objects.filter(
            studentcohortmentor__cohort=self.cohort).filter(
            id__gte=0).distinct()
        student_list = student_list.prefetch_related(
            'studentclasssitestatus_set__status',
            'studentclasssitestatus_set__class_site',
            'cohorts')
        return student_list


class ClassSiteView(LoginRequiredMixin, UserLogPageViewMixin, ListView):
    template_name = 'seumich/class_site_detail.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super(ClassSiteView, self).get_context_data(**kwargs)
        context['studentListHeader'] = self.class_site.description
        context['class_site'] = self.class_site
        return context

    def get_queryset(self):
        self.class_site = get_object_or_404(ClassSite,
                                            id=self.kwargs['class_site_id'])
        student_list = Student.objects.filter(
            studentclasssitestatus__class_site=self.class_site).filter(
            id__gte=0).distinct()
        student_list = student_list.prefetch_related(
            'studentclasssitestatus_set__status',
            'studentclasssitestatus_set__class_site',
            'cohorts')
        return student_list


class IndexView(LoginRequiredMixin, UserLogPageViewMixin, View):

    def get(self, request):
        return redirect('seumich:advisor', advisor=request.user.username)


class StudentView(LoginRequiredMixin, UserLogPageViewMixin, TemplateView):
    template_name = 'seumich/student_detail.html'

    def get_context_data(self, student, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        selected_student = get_object_or_404(Student, username=student)
        context['student'] = selected_student
        prefetch_student_score = Prefetch(
            'class_site__studentclasssitescore_set',
            queryset=StudentClassSiteScore.objects.filter(
                student=selected_student))
        context['classSites'] = (StudentClassSiteStatus.objects
                                 .filter(
                                     student=selected_student
                                 )
                                 .prefetch_related(
                                     'class_site__classsitescore_set',
                                     'status',
                                     prefetch_student_score
                                 ))
        context['advisors'] = (StudentCohortMentor.objects
                               .filter(
                                   student=selected_student)
                               .prefetch_related('mentor', 'cohort'))
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
            class_site=class_site).prefetch_related('assignment', '_due_date')
        context['current_status'] = student.studentclasssitestatus_set.get(
            class_site=class_site).status.description

        course_url_prefix = config("CANVAS_COURSE_URL_PREFIX", default="")
        logger.info("course_url_prefix " + course_url_prefix)
        if (course_url_prefix != ""):
            context['class_site_canvas_url'] = course_url_prefix + class_site.code

            logger.info("class_site_canvas_url " + course_url_prefix + class_site.code)
        return context
