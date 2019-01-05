# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(default='', max_length=255)),
                ('related_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('related_content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-timestamp',),
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.CreateModel(
            name='MentorStudentCourseObserver',
            fields=[
                ('student_id', models.CharField(max_length=50)),
                ('mentor_uniqname', models.CharField(max_length=50)),
                ('mentor_id', models.CharField(max_length=50)),
                ('course_id', models.CharField(max_length=50)),
                ('course_section_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='MentorStudentCourseObserver',
            unique_together=set([('student', 'mentor_id', 'course_id')]),
        ),
    ]
