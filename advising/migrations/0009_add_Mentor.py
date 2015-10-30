# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0008_assignment_studentclasssiteassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=16)),
                ('univ_id', models.CharField(max_length=11)),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCohortMentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cohort', models.ForeignKey(to='advising.Cohort')),
                ('mentor', models.ForeignKey(to='advising.Mentor')),
            ],
        ),
        migrations.RemoveField(
            model_name='studentcohort',
            name='cohort',
        ),
        migrations.RemoveField(
            model_name='studentcohort',
            name='student',
        ),
        migrations.AlterField(
            model_name='student',
            name='cohorts',
            field=models.ManyToManyField(to='advising.Cohort', through='advising.StudentCohortMentor'),
        ),
        migrations.DeleteModel(
            name='StudentCohort',
        ),
        migrations.AddField(
            model_name='studentcohortmentor',
            name='student',
            field=models.ForeignKey(to='advising.Student'),
        ),
    ]
