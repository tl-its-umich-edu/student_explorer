# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0017_eventtype_weeklystudentclasssiteevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyclasssitescore',
            name='score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='weeklystudentclasssitescore',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]
