from __future__ import unicode_literals

from django.db import models


class Feedback(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    feedback_message = models.TextField()

    def __unicode__(self):
        return self.feedback_message
