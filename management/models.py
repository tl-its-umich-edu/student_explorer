from __future__ import unicode_literals

import logging
from django.db import models

from tracking.eventnames import EventNames
from tracking.utils import create_event


logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Mentor(BaseModel):
    username = models.CharField(max_length=20, primary_key=True)

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(Mentor, self).save(*args, **kwargs)


class Cohort(BaseModel):
    code = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=100)
    group = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        create_event(EventNames.CohortDeleted,request = request)
        super(Cohort, self).delete(*args, **kwargs)


class Student(BaseModel):
    username = models.CharField(max_length=20, primary_key=True)

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(Student, self).save(*args, **kwargs)


class StudentCohortMentor(BaseModel):
    student = models.ForeignKey(Student)
    cohort = models.ForeignKey(Cohort)
    mentor = models.ForeignKey(Mentor)

    class Meta:
        unique_together = ('student', 'cohort', 'mentor')
