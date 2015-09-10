from django.db import models

# Create your models here.
class Student(models.Model):
	name = models.CharField(max_length=50)
	student_ID = models.CharField(max_length=10)
	status = models.TextField(blank=True, null=True)
	cohorts = models.TextField(blank=True, null=True)
	GPA = models.DecimalField(max_digits=4, decimal_places=3)
	year = models.CharField(max_length=10)
