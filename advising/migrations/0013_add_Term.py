# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0012_add_class_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSiteTerm',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('class_site', models.ForeignKey(to='advising.ClassSite')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=6)),
                ('description', models.CharField(max_length=30)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='classsiteterm',
            name='term',
            field=models.ForeignKey(to='advising.Term'),
        ),
        migrations.AddField(
            model_name='classsite',
            name='terms',
            field=models.ManyToManyField(to='advising.Term', through='advising.ClassSiteTerm'),
        ),
    ]
