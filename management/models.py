from __future__ import unicode_literals

from django.db import models


class Mentor(models.Model):
    username = models.CharField(max_length=20, primary_key=True)


class Cohort(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=100)
    group = models.CharField(max_length=50)
    active = models.BooleanField(default=True)


class Student(models.Model):
    username = models.CharField(max_length=20, primary_key=True)


class StudentCohortMentor(models.Model):
    student = models.ForeignKey(Student)
    cohort = models.ForeignKey(Cohort)
    mentor = models.ForeignKey(Mentor)

    class Meta:
        unique_together = ('student', 'cohort', 'mentor')
