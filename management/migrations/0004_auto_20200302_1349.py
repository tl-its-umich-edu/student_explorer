# Generated by Django 2.2.10 on 2020-03-02 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_mysql_cache'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]
