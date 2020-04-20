import json, os, sys

from django.core.wsgi import get_wsgi_application

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_explorer.settings')

application = get_wsgi_application()

from management.models import Student, Cohort, Mentor, StudentCohortMentor

FIXTURES_PATH = os.path.join('management', 'fixtures')


def main():

    # Opening JSON fixture files with fake management data
    with open(os.path.join(FIXTURES_PATH, 'cohorts.json'), encoding='utf8') as cohorts_file:
        cohorts = json.loads(cohorts_file.read())

    with open(os.path.join(FIXTURES_PATH, 'student_mentor_mappings.json'), encoding='utf8') as student_mentor_file:
        student_mentor_mappings = json.loads(student_mentor_file.read())

    for cohort in cohorts:
        Cohort.objects.get_or_create(
            code=cohort['code'].strip(),
            description=cohort['description'].strip(),
            group=cohort['group'].strip(),
            active=True
        )

    for student_mentor_mapping in student_mentor_mappings:
        student_id = student_mentor_mapping['student_id'].strip()
        code = student_mentor_mapping['code'].strip()
        mentor_id = student_mentor_mapping['mentor_id'].strip()

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
