# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0004_rename_advisees_to_students'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cohort', models.ForeignKey(to='advising.Cohort')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='cohorts',
            field=models.ManyToManyField(to='advising.Cohort', through='advising.StudentCohort'),
        ),
    ]
