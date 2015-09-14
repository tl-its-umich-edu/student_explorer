# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0002_add_advisors_to_student'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentadvisorrole',
            unique_together=set([('student', 'advisor', 'role')]),
        ),
    ]
