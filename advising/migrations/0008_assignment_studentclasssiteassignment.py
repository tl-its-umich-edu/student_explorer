# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0007_student_statuses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentClassSiteAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points_possible', models.FloatField(max_length=10)),
                ('points_earned', models.FloatField(max_length=10)),
                ('included_in_grade', models.CharField(max_length=1)),
                ('grader_comment', models.CharField(max_length=4000, null=True)),
                ('weight', models.FloatField(max_length=126)),
                ('due_date', models.IntegerField()),
                ('assignment', models.ForeignKey(to='advising.Assignment')),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
            options={
                'ordering': ('due_date',),
            },
        ),
    ]
