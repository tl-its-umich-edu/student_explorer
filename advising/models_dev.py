from django.db import models
from advising import utils


# "Dimension" models


class Advisor(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    students = models.ManyToManyField('Student', through='StudentAdvisorRole')

    def __unicode__(self):
        return self.username


class Mentor(models.Model):
    username = models.CharField(max_length=16)
    univ_id = models.CharField(max_length=11)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    students = models.ManyToManyField('Student', through='StudentCohortMentor')

    def __unicode__(self):
        return self.username


class Status(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    order = models.IntegerField()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ('order',)


class Student(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    advisors = models.ManyToManyField('Advisor', through='StudentAdvisorRole')
    mentors = models.ManyToManyField('Mentor', through='StudentCohortMentor')
    cohorts = models.ManyToManyField('Cohort', through='StudentCohortMentor')
    class_sites = models.ManyToManyField('ClassSite',
                                         through='StudentClassSiteStatus')
    statuses = models.ManyToManyField('Status',
                                      through='StudentClassSiteStatus')

    def __unicode__(self):
        return self.username


class Term(models.Model):
    code = models.CharField(max_length=6)
    description = models.CharField(max_length=30)
    begin_date = models.DateField()
    end_date = models.DateField()

    def week_end_dates(self):
        from datetime import timedelta

        delta = self.end_date - self.begin_date
        dates = []
        for i in range(delta.days + 1):
            date = self.begin_date + timedelta(days=i)
            if date.weekday() == 5:
                dates.append(date)

        return dates

    def todays_week_end_date(self):
        from datetime import date, timedelta

        d = date.today()
        while d.weekday() != 5:
            d += timedelta(days=1)
        return d

    def __unicode__(self):
        return self.description


class SourceSystem(models.Model):
    code = models.CharField(max_length=6)
    description = models.CharField(max_length=30)
    long_description = models.CharField(max_length=30)

    def __unicode__(self):
        return self.description


# "Dimension" models that depend on SourceSystem


class AdvisorRole(models.Model):
    code = models.CharField(max_length=4)
    description = models.CharField(max_length=30)

    def __unicode__(self):
        return self.description


class Assignment(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    source_system = models.ForeignKey(SourceSystem, null=True)

    def __unicode__(self):
        return self.description


class ClassSite(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    terms = models.ManyToManyField('Term', through='ClassSiteTerm')
    source_system = models.ForeignKey(SourceSystem, null=True)

    def __unicode__(self):
        return self.description


class Cohort(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    group = models.CharField(max_length=100)
    source_system = models.ForeignKey(SourceSystem, null=True)

    def __unicode__(self):
        return self.description


class EventType(models.Model):
    source_system = models.ForeignKey(SourceSystem)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.description


# "Bridge" models


class ClassSiteTerm(models.Model):
    class_site = models.ForeignKey(ClassSite)
    term = models.ForeignKey(Term)

    def __unicode__(self):
        return '%s was held in %s' % (self.class_site, self.term)


class StudentAdvisorRole(models.Model):
    student = models.ForeignKey(Student)
    advisor = models.ForeignKey(Advisor)
    role = models.ForeignKey(AdvisorRole)

    def __unicode__(self):
        return '%s advises %s as %s' % (self.advisor, self.student, self.role)

    class Meta:
        unique_together = ('student', 'advisor', 'role')


class StudentCohortMentor(models.Model):
    student = models.ForeignKey(Student)
    mentor = models.ForeignKey(Mentor)
    cohort = models.ForeignKey(Cohort)

    def __unicode__(self):
        return '%s is in the %s cohort' % (self.student, self.cohort)


# "Fact" models


class ClassSiteScore(models.Model):
    class_site = models.ForeignKey(ClassSite)
    current_score_average = models.FloatField()

    def __unicode__(self):
        return '%s has an average score of %s' % (
            self.class_site, self.current_score_average)


class StudentClassSiteScore(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    current_score_average = models.FloatField()

    def __unicode__(self):
        return '%s has an average score of %s in %s' % (
            self.student, self.current_score_average, self.class_site)


class StudentClassSiteAssignment(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    assignment = models.ForeignKey(Assignment)
    points_possible = models.FloatField(max_length=10)
    points_earned = models.FloatField(max_length=10)
    class_points_possible = models.FloatField(max_length=10, default=0)
    class_points_earned = models.FloatField(max_length=10, default=0)
    included_in_grade = models.CharField(max_length=1)
    grader_comment = models.CharField(max_length=4000, null=True)
    weight = models.FloatField(max_length=126)
    due_date = models.DateField(null=True)

    def __unicode__(self):
        return '%s has assignment %s in %s' % (self.student, self.assignment,
                                               self.class_site)

    @property
    def percentage(self):
        return self._percentage(self.points_earned,
                                self.points_possible)

    @property
    def class_percentage(self):
        return self._percentage(self.class_points_earned,
                                self.class_points_possible)

    def _percentage(self, x, y):
        if x is None:
            return None
        if y is None:
            return None
        if y == 0:
            return None

        return float(x) / float(y) * 100

    class Meta:
        ordering = ('due_date',)


class StudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return '%s has status %s in %s' % (self.student, self.status,
                                           self.class_site)


class WeeklyClassSiteScore(models.Model):
    class_site = models.ForeignKey(ClassSite)
    week_end_date = models.DateField(null=True)
    score = models.FloatField(null=True)

    def __unicode__(self):
        return 'Average score is %s in %s on %s' % (
            self.score, self.class_site, self.week_end_date)

    class Meta:
        ordering = ('week_end_date',)


class WeeklyStudentClassSiteEvent(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    week_end_date = models.DateField()
    event_type = models.ForeignKey(EventType)

    event_count = models.IntegerField()
    cumulative_event_count = models.IntegerField()
    percentile_rank = models.FloatField()
    cumulative_percentile_rank = models.FloatField()

    def __unicode__(self):
        return '%s in %s on %s had %s events (%s %%ile)' % (
            self.student, self.class_site, self.week_end_date,
            self.event_count, self.percentile_rank)

    class Meta:
        ordering = ('week_end_date',)


class WeeklyStudentClassSiteScore(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    week_end_date = models.DateField(null=True)
    score = models.FloatField(null=True)

    def __unicode__(self):
        return '%s has score %s in %s on %s' % (
            self.student, self.score, self.class_site, self.week_end_date)

    class Meta:
        ordering = ('week_end_date',)


class WeeklyStudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    week_end_date = models.DateField(null=True)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return '%s has status %s in %s on %s' % (
            self.student, self.status, self.class_site, self.week_end_date)
