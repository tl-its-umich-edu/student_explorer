# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0011_connect_mentor_and_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclasssiteassignment',
            name='class_points_earned',
            field=models.FloatField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='studentclasssiteassignment',
            name='class_points_possible',
            field=models.FloatField(default=0, max_length=10),
        ),
    ]
