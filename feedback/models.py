

from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class Feedback(TimeStampedModel):
    user = models.ForeignKey(User)
    feedback_message = models.TextField()

    def __str__(self):
        return self.feedback_message
