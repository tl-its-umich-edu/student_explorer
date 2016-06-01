from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Advisor(TimeStampedModel):
    username = models.CharField(max_length=8)
    students = models.ManyToManyField('Student', through='StudentGroupAdvisor')
    groups = models.ManyToManyField('Group', through='StudentGroupAdvisor')

    def __unicode__(self):
        return self.username


class Student(TimeStampedModel):
    username = models.CharField(max_length=8)
    univ_id = models.CharField(max_length=11)
    advisors = models.ManyToManyField('Advisor', through='StudentGroupAdvisor')
    groups = models.ManyToManyField('Group', through='StudentGroupAdvisor')

    @property
    def email_address(self):
        return self.username + '@umich.edu'

    def __unicode__(self):
        return self.username


class Group(TimeStampedModel):
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.description


class Import(TimeStampedModel):
    pass


class StudentGroupAdvisor(TimeStampedModel):
    student = models.ForeignKey(Student)
    advisor = models.ForeignKey(Advisor)
    group = models.ForeignKey(Group)
    imp = models.ForeignKey(Import)

    def __unicode__(self):
        return '%s"s advisor is %s and is in the %s group' % (self.student,
                                                              self.advisor,
                                                              self.group
                                                              )

    class Meta:
        unique_together = ('imp', 'student', 'advisor', 'group')
