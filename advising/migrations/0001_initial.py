# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=10)),
                ('univ_id', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AdvisorRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=10)),
                ('univ_id', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAdvisorRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('advisor', models.ForeignKey(to='advising.Advisor')),
                ('role', models.ForeignKey(to='advising.AdvisorRole')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
        ),
        migrations.AddField(
            model_name='advisor',
            name='advisees',
            field=models.ManyToManyField(to='advising.Student', through='advising.StudentAdvisorRole'),
        ),
    ]
