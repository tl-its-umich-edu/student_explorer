# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0005_add_Cohort_and_StudentCohort'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='StudentClassSiteStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
                ('status', models.ForeignKey(to='advising.Status')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='class_sites',
            field=models.ManyToManyField(to='advising.ClassSite', through='advising.StudentClassSiteStatus'),
        ),
    ]
