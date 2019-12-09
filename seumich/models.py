from django.db import models
from seumich.mixins import SeumichDataMixin
from django.utils import timezone
import re  # Added for newlines in assignment comments fix

import logging, statistics

logger = logging.getLogger(__name__)


class UsernameField(models.CharField):
    '''Convert case for data warehouse values. Only handles read situations,
    this implementation would need to be extended if writing to the dataset is
    necessary.'''

    def from_db_value(self, value, expression, connection, context):
        return value.lower()

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super(UsernameField, self).get_db_prep_value(
            value, connection, prepared)
        if value is not None:
            return value.upper()
        return value


# "Dimension" models


class Advisor(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ADVSR_KEY')
    username = UsernameField(max_length=16, db_column='ADVSR_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='ADVSR_UM_ID')
    first_name = models.CharField(max_length=500,
                                  db_column='ADVSR_PREF_FIRST_NM')
    last_name = models.CharField(max_length=500, db_column='ADVSR_PREF_SURNM')
    students = models.ManyToManyField('Student', through='StudentAdvisorRole')

    def __str__(self):
        return self.username

    class Meta:
        db_table = '"CNLYR002"."DM_ADVSR"'


class Date(models.Model):
    id = models.IntegerField(primary_key=True, db_column='DT_KEY')
    date = models.DateField(db_column='CAL_DT')

    def __str__(self):
        return self.date.isoformat()

    class Meta:
        db_table = '"CNLYR001"."DM_DT"'


class Mentor(models.Model):
    id = models.IntegerField(primary_key=True, db_column='MNTR_KEY')
    username = UsernameField(max_length=16, db_column='MNTR_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='MNTR_UM_ID')
    first_name = models.CharField(max_length=500,
                                  db_column='MNTR_PREF_FIRST_NM')
    last_name = models.CharField(max_length=500, db_column='MNTR_PREF_SURNM')
    students = models.ManyToManyField('Student', through='StudentCohortMentor')

    def __str__(self):
        return self.username

    @property
    def cohorts(self):
        return Cohort.objects.filter(studentcohortmentor__mentor=self).distinct()

    class Meta:
        db_table = '"CNLYR002"."DM_MNTR"'


class Status(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ACAD_PERF_KEY')
    code = models.CharField(max_length=20, db_column='ACAD_PERF_VAL')
    description = models.CharField(max_length=50, db_column='ACAD_PERF_TXT')
    order = models.IntegerField(db_column='ACAD_PERF_ORDNL_NBR', null=True)

    def __str__(self):
        return self.description

    @property
    def code_value(self):
        if self.code == "R":
            return 10.0
        elif self.code == "Y":
            return 5.0
        elif self.code == "G":
            return 1.0
        # Return "something" for the greys
        return 0.05

    class Meta:
        ordering = ('order',)
        db_table = '"CNLYR002"."DM_ACAD_PERF"'


class Student(models.Model, SeumichDataMixin):
    id = models.IntegerField(primary_key=True, db_column='STDNT_KEY')
    username = UsernameField(max_length=16, db_column='STDNT_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='STDNT_UM_ID')
    first_name = models.CharField(max_length=500,
                                  db_column='STDNT_PREF_FIRST_NM')
    last_name = models.CharField(max_length=500, db_column='STDNT_PREF_SURNM')
    mentors = models.ManyToManyField('Mentor', through='StudentCohortMentor')
    cohorts = models.ManyToManyField('Cohort', through='StudentCohortMentor')
    class_sites = models.ManyToManyField('ClassSite',
                                         through='StudentClassSiteStatus')
    statuses = models.ManyToManyField('Status',
                                      through='StudentClassSiteStatus')

    @property
    def advisors(self):
        return self.aggrate_relationships(self.studentadvisorrole_set.all(),
                                          'advisor', 'role')
    @property
    def status_calculated_value(self):
        """ Calculate a numeric value to represent the status
        Uses this logic        
        if student has at least one of [red, yellow, green]: calculate by the average we've been doing
        elseif student has ONLY grays (one or more): assign a value of .05 return sum if sum < 1 so that more grays sort higher
        else: assign a value of 0 (should only apply to students with NO courses)

        :return: Calculation of values
        :rtype: float
        """
        mean_values = [student_class_site_status.status.code_value for student_class_site_status in self.studentclasssitestatus_set.all()]
        # If there's no values (No courses) return 0
        if len(mean_values) == 0:
            return 0
        values_sum = sum(mean_values)
        if values_sum < 1:
            return values_sum
        return statistics.mean(mean_values)

    @property
    def email_address(self):
        return self.username + '@umich.edu'

    def __str__(self):
        return self.username

    class Meta:
        db_table = '"CNLYR002"."DM_STDNT"'


class Term(models.Model):
    id = models.IntegerField(primary_key=True, db_column='TERM_KEY')
    code = models.CharField(max_length=6, db_column='TERM_CD')
    description = models.CharField(max_length=30, db_column='TERM_DES')
    _begin_date = models.DateField(db_column='TERM_BEGIN_DT')
    _end_date = models.DateField(db_column='ACAD_TERM_END_DT')

    @property
    def begin_date(self):
        return Date.objects.get(date=self._begin_date)

    @property
    def end_date(self):
        return Date.objects.get(date=self._end_date)

    def week_end_dates(self):
        from datetime import timedelta
        from datetime import datetime

        begin_date = datetime.strptime(str(self.begin_date), '%Y-%m-%d').date()
        end_date = datetime.strptime(str(self.end_date), '%Y-%m-%d').date()

        delta = end_date - begin_date
        dates = []
        for i in range(delta.days + 1):
            date = begin_date + timedelta(days=i)
            if date.weekday() == 5:
                dates.append(date)

        return list(Date.objects.filter(date__in=dates))

    def todays_week_end_date(self):
        from datetime import date, timedelta

        d = date.today()
        while d.weekday() != 5:
            d += timedelta(days=1)
        return Date.objects.get(date=d)

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR001"."DM_TERM"'


class SourceSystem(models.Model):
    id = models.IntegerField(primary_key=True, db_column='SRC_SYS_KEY')
    code = models.CharField(max_length=6, db_column='SRC_SYS_CD')
    description = models.CharField(max_length=30, db_column='SRC_SYS_NM')
    long_description = models.CharField(max_length=30, db_column='SRC_SYS_DES')

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_SRC_SYS"'


# "Dimension" models that depend on SourceSystem


class AdvisorRole(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ADVSR_ROLE_KEY')
    code = models.CharField(max_length=4, db_column='ADVSR_ROLE_CD')
    description = models.CharField(max_length=30, db_column='ADVSR_ROLE_DES')

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_ADVSR_ROLE"'


class Assignment(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ASSGN_KEY')
    code = models.CharField(max_length=20, db_column='ASSGN_CD')
    description = models.CharField(max_length=50, db_column='ASSGN_DES')
    source_system = models.ForeignKey(SourceSystem, on_delete=models.CASCADE, db_column='SRC_SYS_KEY',
                                      null=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_ASSGN"'


class ClassSite(models.Model):
    id = models.IntegerField(primary_key=True, db_column='CLASS_SITE_KEY')
    code = models.CharField(max_length=20, db_column='CLASS_SITE_CD')
    description = models.CharField(max_length=50, db_column='CLASS_SITE_DES')
    terms = models.ManyToManyField('Term', through='ClassSiteTerm')
    source_system = models.ForeignKey(SourceSystem, on_delete=models.CASCADE, db_column='SRC_SYS_KEY',
                                      null=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_CLASS_SITE"'


class Cohort(models.Model):
    id = models.IntegerField(primary_key=True, db_column='CHRT_KEY')
    code = models.CharField(max_length=20, db_column='CHRT_CD')
    description = models.CharField(max_length=50, db_column='CHRT_DES')
    group = models.CharField(max_length=100, db_column='CHRT_GRP_NM')
    source_system = models.ForeignKey(SourceSystem, on_delete=models.CASCADE, db_column='SRC_SYS_KEY',
                                      null=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_CHRT"'


class EventType(models.Model):
    id = models.IntegerField(primary_key=True, db_column='EVENT_TYP_KEY')
    source_system = models.ForeignKey(SourceSystem, on_delete=models.CASCADE, db_column='SRC_SYS_KEY',
                                      null=True)
    description = models.CharField(max_length=50, db_column='EVENT_TYP_NM')

    def __str__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_EVENT_TYP"'


# "Bridge" models


class ClassSiteTerm(models.Model):
    id = models.IntegerField(primary_key=True, db_column='CLASS_SITE_TERM_KEY')
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, db_column='TERM_KEY')

    def __str__(self):
        return '%s was held in %s' % (self.class_site, self.term)

    class Meta:
        db_table = '"CNLYR002"."BG_CLASS_SITE_TERM"'


class StudentAdvisorRole(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, db_column='ADVSR_KEY')
    role = models.ForeignKey(AdvisorRole, on_delete=models.CASCADE, db_column='ADVSR_ROLE_KEY')

    def __str__(self):
        return '%s advises %s as %s' % (self.advisor, self.student, self.role)

    class Meta:
        unique_together = ('student', 'advisor', 'role')
        db_table = '"CNLYR002"."BG_STDNT_ADVSR_ROLE"'


class StudentCohortMentor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, db_column='MNTR_KEY')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, db_column='CHRT_KEY')

    def __str__(self):
        return '%s is in the %s cohort' % (self.student, self.cohort)

    class Meta:
        unique_together = ('student', 'cohort', 'mentor')
        db_table = '"CNLYR002"."BG_STDNT_CHRT_MNTR"'


# "Fact" models


class ClassSiteScore(models.Model):
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, primary_key=True,
                                   db_column='CLASS_SITE_KEY')
    current_score_average = models.FloatField(db_column="CLASS_CURR_SCR_AVG")

    def __str__(self):
        return '%s has an average score of %s' % (
            self.class_site, self.current_score_average)

    class Meta:
        db_table = '"CNLYR002"."FC_CLASS_SCR"'


class StudentClassSiteScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, primary_key=True,
                                db_column='STDNT_KEY')
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    current_score_average = models.FloatField(db_column="STDNT_CURR_SCR_AVG")

    def __str__(self):
        return '%s has an average score of %s in %s' % (
            self.student, self.current_score_average, self.class_site)

    class Meta:
        unique_together = ('student', 'class_site')
        db_table = '"CNLYR002"."FC_STDNT_CLASS_SCR"'


class StudentClassSiteAssignment(models.Model, SeumichDataMixin):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, db_column='ASSGN_KEY')
    points_possible = models.FloatField(max_length=10,
                                        db_column='STDNT_ASSGN_PNTS_PSBL_NBR')
    points_earned = models.FloatField(max_length=10,
                                      db_column='STDNT_ASSGN_PNTS_ERND_NBR')
    class_points_possible = models.FloatField(
        max_length=10,
        db_column='CLASS_ASSGN_PNTS_PSBL_NBR')
    class_points_earned = models.FloatField(
        max_length=10,
        db_column='CLASS_ASSGN_PNTS_ERND_NBR')
    included_in_grade = models.CharField(max_length=1,
                                         db_column='INCL_IN_CLASS_GRD_IND')
    # Identifier name modified to be distinct from new function name
    raw_grader_comment = models.CharField(max_length=4000, null=True,
                                      db_column='STDNT_ASSGN_GRDR_CMNT_TXT')
    weight = models.FloatField(max_length=126,
                               db_column='ASSGN_WT_NBR')
    _due_date = models.ForeignKey(Date, on_delete=models.CASCADE, db_column='ASSGN_DUE_SBMT_DT_KEY',
                                  null=True)

    def __str__(self):
        return '%s has assignment %s in %s' % (self.student, self.assignment,
                                               self.class_site)
    # Function to insert breaks in place of newline characters so HTML will
    # actually render newlines
    @property
    def grader_comment(self):

        # Check if grader comment is empty string and exit if so
        if self.raw_grader_comment is None:
            return self.raw_grader_comment

        # Functionally, <br> or <br /> would also work, but using <br><br />
        # complies with XHTML standards, in case that is a necessity of this
        # project
        return re.sub(
            '/\n/g',
            '<br><br />',
            self.raw_grader_comment.rstrip()
        )

    @property
    def due_date(self):
        return self.valid_date_or_none(self._due_date)

    @property
    def percentage(self):
        return self._percentage(self.points_earned,
                                self.points_possible)

    @property
    def class_percentage(self):
        return self._percentage(self.class_points_earned,
                                self.class_points_possible)

    @property
    def relative_to_average(self):
        percentage = self.percentage
        class_percentage = self.class_percentage

        if ((percentage is None) or (class_percentage is None)):
            return None

        difference = self.percentage - self.class_percentage

        return 'near' if abs(difference) <= 5.0 else (
            'above' if difference > 0.0 else
            'below')

    def _percentage(self, x, y):
        if x is None:
            return None
        if y is None:
            return None
        if y == 0:
            return None

        return float(x) / float(y) * 100

    class Meta:
        ordering = ('_due_date',)
        unique_together = ('student', 'class_site', 'assignment')
        db_table = '"CNLYR002"."FC_STDNT_CLASS_ASSGN"'


class StudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_column='ACAD_PERF_KEY')

    def __str__(self):
        return '%s has status %s in %s' % (self.student, self.status,
                                           self.class_site)

    class Meta:
        ordering = ('status__order',)
        unique_together = ('student', 'class_site', 'status')
        db_table = '"CNLYR002"."FC_STDNT_CLASS_ACAD_PERF"'


class WeeklyClassSiteScore(models.Model):
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY',
                                   primary_key=True)
    week_end_date = models.ForeignKey(Date, on_delete=models.CASCADE, db_column='WEEK_END_DT_KEY')
    score = models.FloatField(db_column='CLASS_CURR_SCR_AVG')

    def __str__(self):
        return 'Average score is %s in %s on %s' % (
            self.score, self.class_site, self.week_end_date)

    class Meta:
        ordering = ('week_end_date',)
        unique_together = ('class_site', 'week_end_date')
        db_table = '"CNLYR002"."FC_CLASS_WKLY_SCR"'


class WeeklyStudentClassSiteEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    week_end_date = models.ForeignKey(Date, on_delete=models.CASCADE, db_column='WEEK_END_DT_KEY')
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, db_column='EVENT_TYP_KEY')

    event_count = models.IntegerField(db_column='STDNT_WKLY_EVENT_CNT')
    cumulative_event_count = models.IntegerField(
        db_column='STDNT_CUM_EVENT_CNT')
    percentile_rank = models.FloatField(db_column='STDNT_WKLY_PCTL_RNK')
    cumulative_percentile_rank = models.FloatField(
        db_column='STDNT_CUM_PCTL_RNK')

    def __str__(self):
        return '%s in %s on %s had %s events (%s %%ile)' % (
            self.student, self.class_site, self.week_end_date,
            self.event_count, self.percentile_rank)

    class Meta:
        ordering = ('week_end_date',)
        unique_together = ('student', 'class_site', 'week_end_date')
        db_table = '"CNLYR002"."FC_STDNT_CLASS_WKLY_EVENT"'


class WeeklyStudentClassSiteScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    week_end_date = models.ForeignKey(Date, on_delete=models.CASCADE, db_column='WEEK_END_DT_KEY')
    score = models.FloatField(db_column='STDNT_CURR_SCR_AVG')

    def __str__(self):
        return '%s has score %s in %s on %s' % (
            self.student, self.score, self.class_site, self.week_end_date)

    class Meta:
        ordering = ('week_end_date',)
        unique_together = ('student', 'class_site', 'week_end_date')
        db_table = '"CNLYR002"."FC_STDNT_CLASS_WKLY_SCR"'


class WeeklyStudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, on_delete=models.CASCADE, db_column='CLASS_SITE_KEY')
    week_end_date = models.ForeignKey(Date, on_delete=models.CASCADE, db_column='WEEK_END_DT_KEY')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_column='ACAD_PERF_KEY')

    def __str__(self):
        return '%s has status %s in %s on %s' % (
            self.student, self.status, self.class_site, self.week_end_date)

    class Meta:
        unique_together = ('student', 'class_site', 'week_end_date', 'status')
        db_table = '"CNLYR002"."FC_STDNT_CLS_WKLY_ACAD_PRF"'

class LearningAnalyticsStats(models.Model):
    dw_data_nm = models.CharField(primary_key=True, max_length=50, db_column='DW_DATA_NM')
    extrct_dt = models.DateTimeField(default=timezone.now, db_column='EXTRCT_DT')
    load_dt = models.DateTimeField(default=timezone.now, db_column='LOAD_DT')
    dw_ownr_nm = models.CharField(max_length=8, db_column='DW_OWNR_NM')

    def __str__(self):
        return self.dw_data_nm

    class Meta:
        db_table = '"CNLYR002"."LRNG_ANLTCS_STAT"'
