# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0003_make_roles_unique'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advisor',
            old_name='advisees',
            new_name='students',
        ),
    ]
