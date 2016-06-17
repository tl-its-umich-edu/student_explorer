from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class Feedback(TimeStampedModel):
    user = models.ForeignKey(User)
    feedback_message = models.TextField()

    def __unicode__(self):
        return self.feedback_message
