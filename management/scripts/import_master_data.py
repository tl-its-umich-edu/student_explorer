import os
import sys

from django.core.wsgi import get_wsgi_application


sys.path.append("../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'student_explorer.settings')

application = get_wsgi_application()

# script goes below

from management.models import Student, Cohort, Mentor, StudentCohortMentor
import xlrd

xl_workbook = xlrd.open_workbook('Student Explorer Data Master.xlsx')


cohort_sheet = xl_workbook.sheet_by_name('Cohorts')
for row_idx in range(1, cohort_sheet.nrows):
    code = cohort_sheet.cell(row_idx, 0).value.strip()
    description = cohort_sheet.cell(row_idx, 1).value.strip()
    group = cohort_sheet.cell(row_idx, 2).value.strip()
    cohort, created = Cohort.objects.get_or_create(code=code,
                                                   description=description,
                                                   group=group,
                                                   active=True)


student_cohort_mentor_sheet = xl_workbook.sheet_by_name('Students')
for row_idx in range(1, student_cohort_mentor_sheet.nrows):
    student_id = student_cohort_mentor_sheet.cell(row_idx, 0).value.strip()
    code = student_cohort_mentor_sheet.cell(row_idx, 1).value.strip()
    mentor_id = student_cohort_mentor_sheet.cell(row_idx, 2).value.strip()
    cohort = Cohort.objects.get(code=code)
    student, created = Student.objects.get_or_create(
        username=student_id)
    mentor, created = Mentor.objects.get_or_create(
        username=mentor_id)
    StudentCohortMentor.objects.get_or_create(student=student,
                                              cohort=cohort,
                                              mentor=mentor
                                              )
