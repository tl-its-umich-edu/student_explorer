# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-08 14:43


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorStudentCourseObserver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=50)),
                ('mentor_uniqname', models.CharField(max_length=50)),
                ('course_id', models.CharField(max_length=50)),
                ('course_section_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mentorstudentcourseobserver',
            unique_together=set([('student_id', 'mentor_uniqname', 'course_id')]),
        ),
    ]
