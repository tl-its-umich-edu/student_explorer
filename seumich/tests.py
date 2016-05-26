import os
from django.test import TestCase
from seumich.models import (UsernameField,
                            Advisor,
                            Date,
                            Mentor,
                            Status,
                            Student,
                            Term,
                            SourceSystem,
                            AdvisorRole,
                            Assignment,
                            ClassSite,
                            Cohort,
                            EventType,
                            ClassSiteTerm,
                            StudentAdvisorRole,
                            StudentCohortMentor,
                            ClassSiteScore,
                            StudentClassSiteScore,
                            StudentClassSiteAssignment,
                            StudentClassSiteStatus,
                            WeeklyClassSiteScore,
                            WeeklyStudentClassSiteEvent,
                            WeeklyStudentClassSiteStatus,
                            WeeklyStudentClassSiteScore)


class SeumichTest(TestCase):

    student = Student.objects.get(id=1)
    mentor = Mentor.objects.get(id=2)
    class_site = ClassSite.objects.get(id=2)
    week_end_date = Date.objects.get(id=2088)
    cohort = Cohort.objects.get(id=1)
    assignment = Assignment.objects.get(id=13)
    _due_date = Date.objects.get(id=2098)
    status = Status.objects.get(id=1)
    term = Term.objects.get(id=1)

    def setUp(self):
        os.system((
            'mysql -h 127.0.0.1 -u student_explorer -pstudent_explorer '
            'test_student_explorer < '
            'seumich/fixtures/dev_data_drop_create_and_insert.sql'
        ))

    def test_from_db_value(self):
        obj = UsernameField()
        self.assertEqual('grace', obj.from_db_value('Grace', None, None, None))
        self.assertEqual('james', obj.from_db_value('JAMES', None, None, None))

    def test_get_db_prep_value(self):
        obj = UsernameField()
        self.assertEqual('GRACE', obj.get_db_prep_value('Grace', None, None))
        self.assertEqual('JAMES', obj.get_db_prep_value('james', None, None))

    def test_advisor_string_representation(self):
        """
        Testing whether the advisor's fetched description
        matches the expected description
        """
        advisor = Advisor.objects.get(id=1)
        self.assertEqual(str(advisor), 'zander')

    def test_date_string_representation(self):
        """
        Testing whether the date's fetched description
        matches the expected description
        """
        date = Date.objects.get(id=2016)
        self.assertEqual(str(date), '2015-07-09')

    def test_cohorts(self):
        """
        Testing the 'cohorts' property of Model 'Mentor'
        """
        self.assertQuerysetEqual(
            list(self.mentor.cohorts),
            ['<Cohort: Special Probation F14>',
             '<Cohort: Special Probation W15>',
             '<Cohort: Special Probation F15>']
        )

    def test_mentor_string_representation(self):
        """
        Testing whether the mentor's fetched username
        matches the expected username
        """
        self.assertEqual(str(self.mentor), 'burl')

    def test_status_string_representation(self):
        """
        Testing whether the status's fetched description
        matches the expected description
        """
        status = Status.objects.get(id=3)
        self.assertEqual(str(status), 'Red')

    def test_student_email(self):
        """
        Testing whether the student's fetched email address
        matches the expected email address
        """
        student = Student.objects.get(id=21)
        self.assertEqual(student.email_address, 'james@umich.edu')

    def test_student_string_representation(self):
        """
        Testing whether the student's fetched description
        matches the expected description
        """
        self.assertEqual(str(self.student), 'grace')

    def test_begin_date(self):
        """
        Testing whether the term's fetched begin date
        matches the expected begin date
        """
        self.assertEqual(self.term.begin_date,
                         Date.objects.get(date="2015-09-08"))

    def test_end_date(self):
        """
        Testing whether the term's fetched end date
        matches the expected end date
        """
        self.assertEqual(self.term.end_date,
                         Date.objects.get(date="2015-12-14"))

    def test_week_end_dates(self):
        """
        Testing whether the term's fetched week end dates
        match the expected week end dates
        """
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
        self.assertEqual(self.term.week_end_dates(), dates_list)

    def test_term_string_representation(self):
        """
        Testing whether the term's fetched description
        matches the expected description
        """
        self.assertEqual(str(self.term), 'Fall 2015')

    def test_sourcesystem_string_representation(self):
        """
        Testing whether the source system's fetched description
        matches the expected description
        """
        source_system = SourceSystem.objects.get(code='CNVS')
        self.assertEqual(str(source_system), 'Canvas')

    def test_advisor_role_string_representation(self):
        """
        Testing whether the advisor role's fetched description
        matches the expected description
        """
        advisor_role = AdvisorRole.objects.get(id=1)
        self.assertEqual(str(advisor_role), 'Department Advisor')

    def test_assignment_string_representation(self):
        """
        Testing whether the assignment's fetched description
        matches the expected description
        """
        assignment = Assignment.objects.get(id=15)
        self.assertEqual(str(assignment), 'Quiz extra 2')

    def test_class_site_string_representation(self):
        """
        Testing whether the class site's fetched description
        matches the expected description
        """
        class_site = ClassSite.objects.get(id=1)
        self.assertEqual(str(class_site), 'Math 101')

    def test_cohort_string_representation(self):
        """
        Testing whether the cohort's fetched description
        matches the expected description
        """
        cohort = Cohort.objects.get(id=3)
        self.assertEqual(str(cohort), 'Special Probation F15')

    def test_event_type_string_representation(self):
        """
        Testing whether the event type's fetched description
        matches the expected description
        """
        event_type = EventType.objects.get(id=1)
        self.assertEqual(str(event_type), 'session start')

    def test_class_site_term_string_representation(self):
        """
        Testing whether the class site term's fetched description
        matches the expected description
        """
        class_site_term = (ClassSiteTerm.objects.
                           filter(class_site=self.class_site, term=self.term))
        self.assertEqual(
            str(class_site_term[0]),
            'Math 101 Lab was held in Fall 2015')

    def test_student_advisor_role_string_representation(self):
        """
        Testing whether the student advisor role's fetched description
        matches the expected description
        """
        student = Student.objects.get(id=4)
        advisor = Advisor.objects.get(id=1)
        role = AdvisorRole.objects.get(id=3)

        student_advisor_role = (StudentAdvisorRole.objects.
                                filter(student=student, advisor=advisor,
                                       role=role))
        self.assertEqual(str(student_advisor_role[0]),
                         'zander advises may as Honors Advisor')

    def test_student_cohort_mentor_string_representation(self):
        """
        Testing whether the student cohort mentor's fetched description
        matches the expected description
        """
        student_cohort_mentor = (StudentCohortMentor.objects.
                                 filter(student=self.student,
                                        mentor=self.mentor,
                                        cohort=self.cohort))
        self.assertEqual(str(student_cohort_mentor[0]),
                         'grace is in the Special Probation F14 cohort')

    def test_class_site_score_string_representation(self):
        """
        Testing whether the class site score's fetched description
        matches the expected description
        """
        class_site_score = (ClassSiteScore.objects.
                            filter(class_site=self.class_site))
        self.assertEqual(str(class_site_score[0]),
                         'Math 101 Lab has an average score of 81.9')

    def test_student_class_site_score_string_representation(self):
        """
        Testing whether the student class site score's fetched description
        matches the expected description
        """
        student_class_site_score = (StudentClassSiteScore.objects.
                                    filter(student=self.student,
                                           class_site=self.class_site))
        self.assertEqual(str(student_class_site_score[0]),
                         'grace has an average score of 86.3 in Math 101 Lab')

    def test_studentclasssiteassignment_string_representation(self):
        """
        Testing whether the student class site assignment's fetched description
        matches the expected description
        """
        student_class_site_assignment = (StudentClassSiteAssignment.objects.
                                         filter(student=self.student,
                                                class_site=self.class_site,
                                                assignment=self.assignment))
        self.assertEqual(
            str(student_class_site_assignment[0]),
            'grace has assignment Quiz extra 1 in Math 101 Lab')

    def test_studentclasssiteassignment_due_date(self):
        """
        Testing whether the student class site assignment's due date
        matches the expected due date
        """
        student_class_site_assignment = (StudentClassSiteAssignment.objects.
                                         filter(_due_date=self._due_date))
        self.assertEqual(
            student_class_site_assignment[0].due_date,
            Date.objects.get(date="2015-09-29"))
        student_class_site_assignment = (StudentClassSiteAssignment.objects.
                                         filter(_due_date=None))
        self.assertEqual(student_class_site_assignment[0].due_date, None)

    def test_studentclasssiteassignment_percentage(self):
        """
        Testing whether the student's percentage
        matches the expected percentage
        """
        student_class_site_assignment = (StudentClassSiteAssignment.objects.
                                         filter(student=self.student,
                                                class_site=self.class_site,
                                                assignment=self.assignment))
        self.assertEqual(student_class_site_assignment[0].percentage, 82.0)

    def test_studentclasssiteassignment_class_percentage(self):
        """
        Testing whether the class's percentage
        matches the expected percentage
        """
        student_class_site_assignment = (StudentClassSiteAssignment.objects.
                                         filter(student=self.student,
                                                class_site=self.class_site,
                                                assignment=self.assignment))
        self.assertEqual(
            round(student_class_site_assignment[0].class_percentage, 2), 84.76)

    def test_studentclasssiteassignment_relative_to_average(self):
        """
        Testing whether the student's relative to average
        matches the expected relative to average
        """
        student_class_site_assignment = (StudentClassSiteAssignment.objects.
                                         filter(student=self.student,
                                                class_site=self.class_site,
                                                assignment=self.assignment))
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

    def test_studentclasssitestatus_string_representation(self):
        """
        Testing whether the student class site status's fetched
        description matches the expected description
        """
        student_class_site_status = (StudentClassSiteStatus.
                                     objects.filter(student=self.student,
                                                    class_site=self.class_site,
                                                    status=self.status))
        self.assertEqual(
            str(student_class_site_status[0]),
            'grace has status Green in Math 101 Lab')

    def test_weeklyclasssitescore_string_representation(self):
        """
        Testing whether the weekly class site score's fetched description
        matches the expected description
        """
        weekly_class_site_score = (WeeklyClassSiteScore.objects.
                                   filter(class_site=self.class_site,
                                          week_end_date=self.week_end_date))
        self.assertEqual(
            str(weekly_class_site_score[0]),
            'Average score is 81 in Math 101 Lab on 2015-09-19')

    def test_WeeklyClassSiteScore(self):
        c = ClassSite.objects.get(pk=1)

        w = WeeklyClassSiteScore.objects.filter(
            class_site=c)

        self.assertEqual('Math 101', str(w[0].class_site))
        self.assertEqual('0', str(w[0].score))
        self.assertEqual('2015-09-12', str(w[0].week_end_date))

    def test_WeeklyClassSiteScore_date_range(self):
        c = ClassSite.objects.get(pk=1)
        t = Term.objects.get(id=1)

        w = WeeklyClassSiteScore.objects.filter(
            class_site=c,
            week_end_date__gte=t.begin_date,
            week_end_date__lte=t.end_date)

        self.assertEqual(8, len(w))

    def test_weeklystudentclasssiteevent_string_representation(self):
        """
        Testing whether the weekly student class site event's fetched
        description matches the expected description
        """
        weekly_student_class_site_event = (WeeklyStudentClassSiteEvent.
                                           objects.filter(student=self.
                                                          student,
                                                          class_site=self.
                                                          class_site,
                                                          week_end_date=self.
                                                          week_end_date))
        self.assertEqual(
            str(weekly_student_class_site_event[0]),
            'grace in Math 101 Lab on 2015-09-19 had 3 events (0.68 %ile)')

    def test_WeeklyStudentClassSiteEvent(self):
        events = WeeklyStudentClassSiteEvent.objects.filter(
            student=self.student, class_site=self.class_site)

        self.assertEqual(8, len(events))
        self.assertEqual('Math 101 Lab', str(events[1].class_site))
        self.assertEqual('grace', str(events[1].student))
        self.assertEqual(3, int(events[1].event_count))
        self.assertEqual('2015-09-19', str(events[1].week_end_date))

    def test_weeklystudentclasssitescore_string_representation(self):
        """
        Testing whether the weekly student class site score's fetched
        description matches the expected description
        """
        weekly_student_class_site_score = (WeeklyStudentClassSiteScore.
                                           objects.filter(student=self.
                                                          student,
                                                          class_site=self.
                                                          class_site,
                                                          week_end_date=self.
                                                          week_end_date))
        self.assertEqual(
            str(weekly_student_class_site_score[0]),
            'grace has score 62 in Math 101 Lab on 2015-09-19')

    def test_WeeklyStudentClassSiteScore(self):
        w = WeeklyStudentClassSiteScore.objects.filter(
            student=self.student, class_site=self.class_site)

        self.assertEqual('Math 101 Lab', str(w[0].class_site))
        self.assertEqual('grace', str(w[0].student))
        self.assertEqual('62', str(w[0].score))
        self.assertEqual('2015-09-12', str(w[0].week_end_date))

    def test_weeklystudentclasssitestatus_string_representation(self):
        """
        Testing whether the weekly student class site status's fetched
        description matches the expected description
        """
        status = Status.objects.get(id=2)
        weekly_student_class_site_status = (WeeklyStudentClassSiteStatus.
                                            objects.filter(student=self.
                                                           student,
                                                           class_site=self.
                                                           class_site,
                                                           week_end_date=self.
                                                           week_end_date,
                                                           status=status))
        self.assertEqual(
            str(weekly_student_class_site_status[0]),
            'grace has status Yellow in Math 101 Lab on 2015-09-19')

    def test_WeeklyStudentClassSiteStatus(self):
        w = WeeklyStudentClassSiteStatus.objects.filter(
            student=self.student, class_site=self.class_site)

        self.assertEqual('Math 101 Lab', str(w[0].class_site))
        self.assertEqual('grace', str(w[0].student))
        self.assertEqual('Not Applicable', str(w[0].status))
        self.assertEqual('2015-09-12', str(w[0].week_end_date))
