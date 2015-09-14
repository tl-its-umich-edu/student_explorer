# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='advisors',
            field=models.ManyToManyField(to='advising.Advisor', through='advising.StudentAdvisorRole'),
        ),
    ]
