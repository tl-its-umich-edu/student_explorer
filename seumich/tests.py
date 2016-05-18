import os
from django.test import TestCase
from seumich.models import UsernameField, Advisor, Date, Mentor, Status, Student, Term, SourceSystem, AdvisorRole, Assignment, ClassSite, Cohort, EventType, ClassSiteTerm, StudentAdvisorRole, StudentCohortMentor, ClassSiteScore, StudentClassSiteAssignment, StudentClassSiteStatus, WeeklyClassSiteScore, WeeklyStudentClassSiteEvent, WeeklyStudentClassSiteStatus, WeeklyStudentClassSiteScore


class MentorTest(TestCase):

    def setUp(self):
        os.system(
            'mysql -h 127.0.0.1 -u student_explorer -pstudent_explorer ' +
            'test_student_explorer < ' +
            'seumich/fixtures/dev_data_drop_create_and_insert.sql')

    def test_cohorts(self):
        """
        Testing the 'cohorts' property of Model 'Mentor'
        """
        mentor = Mentor.objects.get(id=2)
        self.assertQuerysetEqual(
            list(mentor.cohorts),
            ['<Cohort: Special Probation F14>',
                '<Cohort: Special Probation W15>',
                '<Cohort: Special Probation F15>']
        )

    def test_mentor_creation(self):
        """
        Testing whether the mentor's fetched username
        matches the expected username
        """
        mentor = Mentor.objects.get(id=2)
        self.assertEqual(mentor.__unicode__(), 'burl')


class StatusTest(TestCase):

    def test_status_creation(self):
        """
        Testing whether the status's fetched description
        matches the expected description
        """
        status = Status.objects.get(id=3)
        self.assertEqual(status.__unicode__(), 'Red')


class StudentTest(TestCase):

    def test_student_email(self):
        """
        Testing whether the student's fetched email address
        matches the expected email address
        """
        student = Student.objects.get(id=21)
        self.assertEqual(student.email_address, 'james@umich.edu')

    def test_student_creation(self):
        """
        Testing whether the student's fetched description
        matches the expected description
        """
        student = Student.objects.get(id=1)
        self.assertEqual(student.__unicode__(), 'grace')


class TermTest(TestCase):

    def test_begin_date(self):
        """
        Testing whether the term's fetched begin date
        matches the expected begin date
        """
        term = Term.objects.get(id=1)
        self.assertEqual(term.begin_date, Date.objects.get(date="2015-09-08"))

    def test_end_date(self):
        """
        Testing whether the term's fetched end date
        matches the expected end date
        """
        term = Term.objects.get(id=1)
        self.assertEqual(term.end_date, Date.objects.get(date="2015-12-14"))

    def test_week_end_dates(self):
        """
        Testing whether the term's fetched week end dates
        match the expected week end dates
        """
        term = Term.objects.get(id=1)
        dates_list = [Date.objects.get(date='2015-09-12'),
                      Date.objects.get(date='2015-09-19'),
                      Date.objects.get(date='2015-09-26'),
                      Date.objects.get(date='2015-10-03'),
                      Date.objects.get(date='2015-10-10'),
                      Date.objects.get(date='2015-10-17'),
                      Date.objects.get(date='2015-10-24'),
                      Date.objects.get(date='2015-10-31'),
                      Date.objects.get(date='2015-11-07'),
                      Date.objects.get(date='2015-11-14'),
                      Date.objects.get(date='2015-11-21'),
                      Date.objects.get(date='2015-11-28'),
                      Date.objects.get(date='2015-12-05'),
                      Date.objects.get(date='2015-12-12')]
        self.assertEqual(term.week_end_dates(), dates_list)

    def test_term_creation(self):
        """
        Testing whether the term's fetched description
        matches the expected description
        """
        term = Term.objects.get(id=1)
        self.assertEqual(term.__unicode__(), 'Fall 2015')


class SourceSystemTest(TestCase):

    def test_sourcesystem_creation(self):
        """
        Testing whether the source system's fetched description
        matches the expected description
        """
        source_system = SourceSystem.objects.get(code='CNVS')
        self.assertEqual(source_system.__unicode__(), 'Canvas')


class StudentClassSiteAssignmentTest(TestCase):
    student = Student.objects.get(id=1)
    class_site = ClassSite.objects.get(id=2)
    assignment = Assignment.objects.get(id=13)
    _due_date = Date.objects.get(id=2098)

    def test_studentclasssiteassignment_creation(self):
        """
        Testing whether the student class site assignment's fetched description
        matches the expected description
        """
        student_class_site_assignment = StudentClassSiteAssignment.objects. \
            filter(student=self.student, class_site=self.class_site,
                   assignment=self.assignment)
        self.assertEqual(
            student_class_site_assignment[0].__unicode__(),
            'grace has assignment Quiz extra 1 in Math 101 Lab')

    def test_studentclasssiteassignment_due_date(self):
        """
        Testing whether the student class site assignment's due date
        matches the expected due date
        """
        student_class_site_assignment = StudentClassSiteAssignment.objects. \
            filter(_due_date=self._due_date)
        self.assertEqual(
            student_class_site_assignment[0].due_date,
            Date.objects.get(date="2015-09-29"))
        student_class_site_assignment = StudentClassSiteAssignment.objects. \
            filter(_due_date=None)
        self.assertEqual(student_class_site_assignment[0].due_date, None)

    def test_studentclasssiteassignment_percentage(self):
        """
        Testing whether the student's percentage
        matches the expected percentage
        """
        student_class_site_assignment = StudentClassSiteAssignment.objects. \
            filter(student=self.student, class_site=self.class_site,
                   assignment=self.assignment)
        self.assertEqual(student_class_site_assignment[0].percentage, 82.0)

    def test_studentclasssiteassignment_class_percentage(self):
        """
        Testing whether the class's percentage
        matches the expected percentage
        """
        student_class_site_assignment = StudentClassSiteAssignment.objects. \
            filter(student=self.student, class_site=self.class_site,
                   assignment=self.assignment)
        self.assertEqual(
            round(student_class_site_assignment[0].class_percentage, 2), 84.76)

    def test_studentclasssiteassignment_relative_to_average(self):
        """
        Testing whether the student's relative to average
        matches the expected relative to average
        """
        student_class_site_assignment = StudentClassSiteAssignment.objects. \
            filter(student=self.student, class_site=self.class_site,
                   assignment=self.assignment)
        self.assertEqual(
            student_class_site_assignment[0].relative_to_average, 'near')

    def test_studentclasssiteassignment__percentage(self):
        obj = StudentClassSiteAssignment()

        self.assertEqual(75.0, obj._percentage(3.0, 4.0))
        self.assertEqual(0.0, obj._percentage(0, 4.0))
        self.assertEqual(None, obj._percentage(10.0, 0))
        self.assertEqual(75.0, obj._percentage(3, 4))
        self.assertEqual(None, obj._percentage(10, None))
        self.assertEqual(None, obj._percentage(None, 10))
        self.assertEqual(None, obj._percentage(None, None))
