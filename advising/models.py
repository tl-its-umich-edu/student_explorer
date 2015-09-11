from django.db import models


class Student(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username


class Advisor(models.Model):
    username = models.CharField(max_length=10)
    univ_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    advisees = models.ManyToManyField(Student, through='StudentAdvisorRole')

    def __unicode__(self):
        return self.username


class AdvisorRole(models.Model):
    code = models.CharField(max_length=4)
    description = models.CharField(max_length=30)

    def __unicode__(self):
        return self.description


class StudentAdvisorRole(models.Model):
    student = models.ForeignKey(Student)
    advisor = models.ForeignKey(Advisor)
    role = models.ForeignKey(AdvisorRole)

    def __unicode__(self):
        return '%s advises %s as %s' % (self.advisor, self.student, self.role)
