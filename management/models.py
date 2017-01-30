from __future__ import unicode_literals

from django.db import models


class Cohort(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    group = models.CharField(max_length=50)
    active = models.BooleanField(default=True)


class Student(models.Model):
    username = models.CharField(max_length=20)
    cohort = models.ForeignKey(Cohort)
    mentor_username = models.CharField(max_length=20)
