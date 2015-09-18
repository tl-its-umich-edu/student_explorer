from django.db import models
from django.conf import settings
import importlib

# Note that these model definitions are overriden below if
# settings.ADVISING_PACKAGE is set. This allows for customized models to
# accommodate external databases and their schema differences.


class Student(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    advisors = models.ManyToManyField('Advisor', through='StudentAdvisorRole')
    cohorts = models.ManyToManyField('Cohort', through='StudentCohort')
    class_sites = models.ManyToManyField('ClassSite',
                                         through='StudentClassSiteStatus')

    def __unicode__(self):
        return self.username


class Advisor(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    students = models.ManyToManyField('Student', through='StudentAdvisorRole')

    def __unicode__(self):
        return self.username


class AdvisorRole(models.Model):
    code = models.CharField(max_length=4)
    description = models.CharField(max_length=30)

    def __unicode__(self):
        return self.description


class StudentAdvisorRole(models.Model):
    student = models.ForeignKey(Student)
    advisor = models.ForeignKey(Advisor)
    role = models.ForeignKey(AdvisorRole)

    def __unicode__(self):
        return '%s advises %s as %s' % (self.advisor, self.student, self.role)

    class Meta:
        unique_together = ('student', 'advisor', 'role')


class Cohort(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    group = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description


class StudentCohort(models.Model):
    student = models.ForeignKey(Student)
    cohort = models.ForeignKey(Cohort)

    def __unicode__(self):
        return '%s is in the %s cohort' % (self.student, self.cohort)


class ClassSite(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.description


class Status(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    order = models.IntegerField()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ('order',)


class StudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student)
    class_site = models.ForeignKey(ClassSite)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return '%s has status %s in %s' % (self.student, self.status,
                                           self.class_site)

if hasattr(settings, 'ADVISING_PACKAGE'):
    # Override the definitions above if an alternate package has been
    # specified.

    advising_models_module = settings.ADVISING_PACKAGE + '.models'
    advising_models = importlib.import_module(advising_models_module)

    Student = advising_models.Student
    Advisor = advising_models.Advisor
    AdvisorRole = advising_models.AdvisorRole
    StudentAdvisorRole = advising_models.StudentAdvisorRole
    Cohort = advising_models.Cohort
    StudentCohort = advising_models.StudentCohort
    ClassSite = advising_models.ClassSite
    Status = advising_models.Status
    StudentClassSiteStatus = advising_models.StudentClassSiteStatus
