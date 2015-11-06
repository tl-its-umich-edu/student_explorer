# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0015_add_Weeklys'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=6)),
                ('description', models.CharField(max_length=30)),
                ('long_description', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='source_system',
            field=models.ForeignKey(to='advising.SourceSystem', null=True),
        ),
        migrations.AddField(
            model_name='classsite',
            name='source_system',
            field=models.ForeignKey(to='advising.SourceSystem', null=True),
        ),
        migrations.AddField(
            model_name='cohort',
            name='source_system',
            field=models.ForeignKey(to='advising.SourceSystem', null=True),
        ),
    ]
