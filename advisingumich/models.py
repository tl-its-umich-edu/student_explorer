from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True, db_column='STDNT_KEY')
    username = models.CharField(max_length=16, db_column='STDNT_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='STDNT_UM_ID')
    first_name = models.CharField(max_length=500,
                                  db_column='STDNT_PREF_FIRST_NM')
    last_name = models.CharField(max_length=500, db_column='STDNT_PREF_SURNM')

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = '"CNLYR002"."DM_STDNT"'


class Advisor(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ADVSR_KEY')
    username = models.CharField(max_length=16, db_column='ADVSR_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='ADVSR_UM_ID')
    first_name = models.CharField(max_length=500,
                                  db_column='ADVSR_PREF_FIRST_NM')
    last_name = models.CharField(max_length=500, db_column='ADVSR_PREF_SURNM')

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = '"CNLYR002"."DM_ADVSR"'


class AdvisorRole(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ADVSR_ROLE_KEY')
    code = models.CharField(max_length=4, db_column='ADVSR_ROLE_CD')
    description = models.CharField(max_length=30, db_column='ADVSR_ROLE_DES')

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_ADVSR_ROLE"'


class StudentAdvisorRole(models.Model):
    student = models.ForeignKey(Student, db_column='STDNT_KEY',
                                primary_key=True)
    advisor = models.ForeignKey(Advisor, db_column='ADVSR_KEY',
                                primary_key=True)
    role = models.ForeignKey(AdvisorRole, db_column='ADVSR_ROLE_KEY',
                             primary_key=True)

    def __unicode__(self):
        return '%s advises %s as %s' % (self.advisor, self.student, self.role)

    class Meta:
        db_table = '"CNLYR002"."BG_STDNT_ADVSR_ROLE"'
        unique_together = (('student', 'advisor', 'role'),)
