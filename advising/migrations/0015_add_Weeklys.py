# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0014_due_date_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyClassSiteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_end_date', models.DateField(null=True)),
                ('score', models.IntegerField(null=True)),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
            ],
            options={
                'ordering': ('week_end_date',),
            },
        ),
        migrations.CreateModel(
            name='WeeklyStudentClassSiteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_end_date', models.DateField(null=True)),
                ('score', models.IntegerField(null=True)),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
            options={
                'ordering': ('week_end_date',),
            },
        ),
        migrations.CreateModel(
            name='WeeklyStudentClassSiteStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_end_date', models.DateField(null=True)),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
                ('status', models.ForeignKey(to='advising.Status')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
        ),
    ]
