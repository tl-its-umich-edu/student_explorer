# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0013_add_Term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentclasssiteassignment',
            name='due_date',
            field=models.DateField(null=True),
        ),
    ]
