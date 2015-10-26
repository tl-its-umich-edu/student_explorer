from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True, db_column='STDNT_KEY')
    username = models.CharField(max_length=16, db_column='STDNT_UM_UNQNM')
    univ_id = models.CharField(max_length=11, db_column='STDNT_UM_ID')
    first_name = models.CharField(max_length=500,
                                  db_column='STDNT_PREF_FIRST_NM')
    last_name = models.CharField(max_length=500, db_column='STDNT_PREF_SURNM')
    advisors = models.ManyToManyField('Advisor', through='StudentAdvisorRole')
    cohorts = models.ManyToManyField('Cohort', through='StudentCohort')
    class_sites = models.ManyToManyField('ClassSite',
                                         through='StudentClassSiteStatus')
    statuses = models.ManyToManyField('Status',
                                      through='StudentClassSiteStatus')

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
    students = models.ManyToManyField('Student', through='StudentAdvisorRole')

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


class Cohort(models.Model):
    id = models.IntegerField(primary_key=True, db_column='CHRT_KEY')
    code = models.CharField(max_length=20, db_column='CHRT_CD')
    description = models.CharField(max_length=50, db_column='CHRT_DES')
    group = models.CharField(max_length=100, db_column='CHRT_GRP_NM')

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_CHRT"'


class StudentCohort(models.Model):
    student = models.ForeignKey(Student, db_column='STDNT_KEY',
                                primary_key=True)
    cohort = models.ForeignKey(Cohort, db_column='CHRT_KEY')

    def __unicode__(self):
        return '%s is in the %s cohort' % (self.student, self.cohort)

    class Meta:
        db_table = '"CNLYR002"."BG_STDNT_CHRT_MNTR"'
        unique_together = ('student', 'cohort')


class ClassSite(models.Model):
    id = models.IntegerField(primary_key=True, db_column='CLASS_SITE_KEY')
    code = models.CharField(max_length=20, db_column='CLASS_SITE_CD')
    description = models.CharField(max_length=50, db_column='CLASS_SITE_DES')

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_CLASS_SITE"'


class Status(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ACAD_PERF_KEY')
    code = models.CharField(max_length=20, db_column='ACAD_PERF_VAL')
    description = models.CharField(max_length=50, db_column='ACAD_PERF_TXT')
    order = models.IntegerField(db_column='ACAD_PERF_ORDNL_NBR')

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ('order',)
        db_table = '"CNLYR002"."DM_ACAD_PERF"'


class StudentClassSiteStatus(models.Model):
    student = models.ForeignKey(Student, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, db_column='CLASS_SITE_KEY')
    status = models.ForeignKey(Status, db_column='ACAD_PERF_KEY')

    def __unicode__(self):
        return '%s has status %s in %s' % (self.student, self.status,
                                           self.class_site)

    class Meta:
        db_table = '"CNLYR002"."FC_STDNT_CLASS_ACAD_PERF"'
        unique_together = ('student', 'class_site', 'status')


class Assignment(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ASSGN_KEY')
    code = models.CharField(max_length=20, db_column='ASSGN_CD')
    description = models.CharField(max_length=50, db_column='ASSGN_DES')

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = '"CNLYR002"."DM_ASSGN"'


class StudentClassAssignment(models.Model):
    student = models.ForeignKey(Student, db_column='STDNT_KEY',
                                primary_key=True)
    class_site = models.ForeignKey(ClassSite, db_column='CLASS_SITE_KEY')
    assignment = models.ForeignKey(Assignment, db_column='ASSGN_KEY')
    points_possible = models.FloatField(max_length=10,
                                        db_column='STDNT_ASSGN_PNTS_PSBL_NBR')
    points_earned = models.FloatField(max_length=10,
                                      db_column='STDNT_ASSGN_PNTS_ERND_NBR')
    included_in_grade = models.CharField(max_length=1,
                                         db_column='INCL_IN_CLASS_GRD_IND')
    grader_comment = models.CharField(max_length=4000, null=True,
                                      db_column='STDNT_ASSGN_GRDR_CMNT_TXT')
    weight = models.FloatField(max_length=126,
                               db_column='ASSGN_WT_NBR')

    def __unicode__(self):
        return '%s has assignemnt %s in %s' % (self.student, self.assignment,
                                               self.class_site)

    class Meta:
        # db_table = '"CNLYR002"."FC_STDNT_CLASS_ASSGN"'
        db_table = '"CNLYR002"."FC_STDNT_CLASS_WKLY_ASSGN"'
        unique_together = ('student', 'class_site', 'assignment')
