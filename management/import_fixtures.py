import os, sys

import xlrd
from django.core.wsgi import get_wsgi_application

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_explorer.settings')

application = get_wsgi_application()

from management.models import Student, Cohort, Mentor, StudentCohortMentor

FIXTURES_PATH = os.path.join('management', 'fixtures', 'Student_Explorer_Management_Fixtures.xlsx')


def main():
    # Open Excel workbook with fake management data
    xl_workbook = xlrd.open_workbook(FIXTURES_PATH)

    cohort_sheet = xl_workbook.sheet_by_name('Cohorts')
    for row_idx in range(1, cohort_sheet.nrows):
        code = cohort_sheet.cell(row_idx, 0).value.strip()
        description = cohort_sheet.cell(row_idx, 1).value.strip()
        group = cohort_sheet.cell(row_idx, 2).value.strip()
        Cohort.objects.get_or_create(
            code=code,
            description=description,
            group=group,
            active=True
        )

    student_cohort_mentor_sheet = xl_workbook.sheet_by_name('Students')
    for row_idx in range(1, student_cohort_mentor_sheet.nrows):
        student_id = student_cohort_mentor_sheet.cell(row_idx, 0).value.strip()
        code = student_cohort_mentor_sheet.cell(row_idx, 1).value.strip()
        mentor_id = student_cohort_mentor_sheet.cell(row_idx, 2).value.strip()
        cohort = Cohort.objects.get(code=code)
        student = Student.objects.get_or_create(username=student_id)[0]
        mentor = Mentor.objects.get_or_create(username=mentor_id)[0]
        StudentCohortMentor.objects.get_or_create(
            student=student,
            cohort=cohort,
            mentor=mentor
        )

if __name__ == '__main__':
    main()
    
