from __future__ import unicode_literals

from django.db import models


class Advisor(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ADVR_KEY')
    username = models.CharField(max_length=8, db_column='ADVR_UM_UNQNM')
    students = models.ManyToManyField('Student', through='StudentGroupAdvisor')

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = 'advisor'


class Student(models.Model):
    id = models.IntegerField(primary_key=True, db_column='STDNT_KEY')
    username = models.CharField(max_length=8, db_column='STDNT_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='STDNT_UM_ID')
    advisors = models.ManyToManyField('Advisor', through='StudentGroupAdvisor')
    groups = models.ManyToManyField('Group', through='StudentGroupAdvisor')

    @property
    def email_address(self):
        return self.username + '@umich.edu'

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = 'student'


class Group(models.Model):
    id = models.IntegerField(primary_key=True, db_column='GRP_KEY')
    description = models.CharField(max_length=50, db_column='GRP_DES')

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = 'group'


class StudentGroupAdvisor(models.Model):
    student = models.ForeignKey(Student, db_column='STDNT_KEY',
                                primary_key=True)
    advisor = models.ForeignKey(Advisor, db_column='ADVR_KEY')
    group = models.ForeignKey(Group, db_column='GRP_KEY')

    def __unicode__(self):
        return '%s"s advisor is %s and is in the %s group' % (self.student,
                                                              self.advisor,
                                                              self.group
                                                              )

    class Meta:
        unique_together = ('student', 'advisor', 'group')
        db_table = 'student_advisor_group'
