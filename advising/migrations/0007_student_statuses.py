# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0006_add_Classsite_Status_StudentClassSiteStatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='statuses',
            field=models.ManyToManyField(to='advising.Status', through='advising.StudentClassSiteStatus'),
        ),
    ]
