# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0010_due_date_fix'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='students',
            field=models.ManyToManyField(to='advising.Student', through='advising.StudentCohortMentor'),
        ),
        migrations.AddField(
            model_name='student',
            name='mentors',
            field=models.ManyToManyField(to='advising.Mentor', through='advising.StudentCohortMentor'),
        ),
    ]
