# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0019_auto_20151111_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSiteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_score_average', models.FloatField()),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
            ],
        ),
        migrations.CreateModel(
            name='StudentClassSiteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_score_average', models.FloatField()),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
                ('student', models.ForeignKey(to='advising.Student')),
            ],
        ),
    ]
