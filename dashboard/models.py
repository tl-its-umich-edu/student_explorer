from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    is_policy_accepted = models.NullBooleanField(null=True)
    policy_accepted_date = models.DateField(null=True)
