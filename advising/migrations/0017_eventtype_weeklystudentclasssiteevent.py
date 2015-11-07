# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0016_add_SourceSystem'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
                ('source_system', models.ForeignKey(to='advising.SourceSystem')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyStudentClassSiteEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_end_date', models.DateField()),
                ('event_count', models.IntegerField()),
                ('cumulative_event_count', models.IntegerField()),
                ('percentile_rank', models.FloatField()),
                ('cumulative_percentile_rank', models.FloatField()),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
                ('event_type', models.ForeignKey(to='advising.EventType')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
            options={
                'ordering': ('week_end_date',),
            },
        ),
    ]
