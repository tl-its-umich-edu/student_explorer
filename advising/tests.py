from django.test import TestCase
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

import json

import advising.models
import advising.serializers


class AdvisingModelsTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']

    def test_StudentClassSiteAssignment__percentage(self):
        obj = advising.models.StudentClassSiteAssignment()

        self.assertEqual(75.0, obj._percentage(3.0, 4.0))
        self.assertEqual(0.0, obj._percentage(0, 4.0))
        self.assertEqual(None, obj._percentage(10.0, 0))
        self.assertEqual(75.0, obj._percentage(3, 4))
        self.assertEqual(None, obj._percentage(10, None))
        self.assertEqual(None, obj._percentage(None, 10))
        self.assertEqual(None, obj._percentage(None, None))

    def test_WeeklyStudentClassSiteScore(self):
        s = advising.models.Student.objects.get(pk=1)
        c = advising.models.ClassSite.objects.get(pk=2)

        w = advising.models.WeeklyStudentClassSiteScore.objects.filter(
            student=s, class_site=c)

        self.assertEqual('Math 101 Lab', str(w[0].class_site))
        self.assertEqual('grace', str(w[0].student))
        self.assertEqual('62.2', str(w[0].score))
        self.assertEqual('2015-09-12', str(w[0].week_end_date))

    def test_WeeklyClassSiteScore(self):
        c = advising.models.ClassSite.objects.get(pk=1)

        w = advising.models.WeeklyClassSiteScore.objects.filter(
            class_site=c)

        self.assertEqual('Math 101', str(w[0].class_site))
        self.assertEqual('0.0', str(w[0].score))
        self.assertEqual('2015-09-12', str(w[0].week_end_date))

    def test_WeeklyClassSiteScore_date_range(self):
        c = advising.models.ClassSite.objects.get(pk=1)
        t = advising.models.Term.objects.get(id=1)

        w = advising.models.WeeklyClassSiteScore.objects.filter(
            class_site=c,
            week_end_date__gte=t.begin_date,
            week_end_date__lte=t.end_date)

        self.assertEqual(8, len(w))

    def test_WeeklyStudentClassSiteStatus(self):
        s = advising.models.Student.objects.get(pk=1)
        c = advising.models.ClassSite.objects.get(pk=2)

        w = advising.models.WeeklyStudentClassSiteStatus.objects.filter(
            student=s, class_site=c)

        self.assertEqual('Math 101 Lab', str(w[0].class_site))
        self.assertEqual('grace', str(w[0].student))
        self.assertEqual('Not Applicable', str(w[0].status))
        self.assertEqual('2015-09-12', str(w[0].week_end_date))

    def test_SourceSystem(self):
        systems = advising.models.SourceSystem.objects.all()

        self.assertEqual(2, len(systems))

    def test_EventType(self):
        events = advising.models.EventType.objects.all()

        self.assertEqual(1, len(events))
        self.assertEqual(u'session start', events[0].description)

    def test_WeeklyStudentClassSiteEvent(self):
        s = advising.models.Student.objects.get(pk=1)
        c = advising.models.ClassSite.objects.get(pk=2)

        events = advising.models.WeeklyStudentClassSiteEvent.objects.filter(
            student=s, class_site=c)

        self.assertEqual(8, len(events))
        self.assertEqual('Math 101 Lab', str(events[1].class_site))
        self.assertEqual('grace', str(events[1].student))
        self.assertEqual(3, int(events[1].event_count))
        self.assertEqual('2015-09-19', str(events[1].week_end_date))


class AdvisingApiTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_bad_url(self):
        response = self.client.get(
            '%s/rubarb-rubarb-rubarb/' % reverse('advising-api-root'))

        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 500)

    def test_api_root_unauthenticated(self):
        response = self.client.get(reverse('advising-api-root'))

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def test_api_config_username_unauthenticated(self):
        response = self.client.get(reverse('current-user-detail'))

        self.assertEqual(response.status_code, 404)

    def test_api_config_username_authenticated(self):
        username = 'burl'

        user = get_user_model().objects.get(username=username)
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('current-user-detail'))
        data = json.loads(response.content)

        self.assertEqual(data['username'], username,
                         'username should be "%s"' % username)


class AdvisingApiStudentTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_students_list(self):
        response = self.client.get(reverse('student-list'))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(23, data['count'])

    def test_students_search_with_results(self):
        response = self.client.get(reverse('student-list'), {'search': 'gra'})

        data = json.loads(response.content)

        self.assertEqual(2, data['count'])

    def test_students_search_with_no_results(self):
        response = self.client.get(reverse('student-list'), {'search': 'asdf'})

        data = json.loads(response.content)

        self.assertEqual(0, data['count'])

    def test_students_search_check_data(self):
        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})

        data = json.loads(response.content)

        self.assertEqual(1, data['count'])
        self.assertEqual('james', data['results'][0]['username'])

    def test_students_detail_exists(self):
        response = self.client.get(reverse('student-detail',
                                           kwargs={'username': 'grace'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('grace', data['username'])

    def test_students_detail_not_exists(self):
        response = self.client.get(reverse('student-detail',
                                           kwargs={'username': 'asdfa'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

    def test_students_advisors_list_exists(self):
        response = self.client.get(reverse('student-advisors-list',
                                           kwargs={'username': 'grace'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 1)

    def test_students_advisors_list_not_exists(self):
        response = self.client.get(reverse('student-advisors-list',
                                           kwargs={'username': 'afddf'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'count': 0,
                u'next': None,
                u'previous': None,
                u'results': []
            }, data)

    def test_students_mentors_list_exists(self):
        response = self.client.get(reverse('student-mentors-list',
                                           kwargs={'username': 'grace'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 1)

    def test_students_mentors_list_not_exists(self):
        response = self.client.get(reverse('student-mentors-list',
                                           kwargs={'username': 'afddf'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

    def test_students_class_site_list_exists(self):
        response = self.client.get(reverse('student-classsite-list',
                                           kwargs={'username': 'grace'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 2)

    def test_students_class_site_list_not_exists(self):
        response = self.client.get(reverse('student-classsite-list',
                                           kwargs={'username': 'afddf'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'count': 0,
                u'next': None,
                u'previous': None,
                u'results': []
            }, data)

    def test_students_class_site_detail_exists(self):
        response = self.client.get(reverse('student-classsite-detail',
                                           kwargs={'username': 'grace',
                                                   'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Yellow')

    def test_students_class_site_detail_not_exists(self):
        response = self.client.get(reverse('student-classsite-detail',
                                           kwargs={'username': 'adffd',
                                                   'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

        response = self.client.get(reverse('student-classsite-detail',
                                           kwargs={'username': 'grace',
                                                   'code': '575'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

    def test_students_class_site_assignment_list_exists(self):
        response = self.client.get(reverse('student-classsite-assignment-list',
                                           kwargs={'username': 'grace',
                                                   'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 2)

    def test_students_class_site_assignment_list_not_exists(self):
        response = self.client.get(reverse('student-classsite-assignment-list',
                                           kwargs={'username': 'adffd',
                                                   'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'count': 0,
                u'next': None,
                u'previous': None,
                u'results': []
            }, data)

        response = self.client.get(reverse('student-classsite-assignment-list',
                                           kwargs={'username': 'grace',
                                                   'code': '575'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'count': 0,
                u'next': None,
                u'previous': None,
                u'results': []
            }, data)

    def test_students_class_site_history_list_exists(self):
        response = self.client.get(reverse('student-classsite-history-list',
                                           kwargs={'username': 'grace',
                                                   'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data[0], {
            u'week_end_date': u'2015-09-12',
            u'score': 0.0,
            u'class_score': 0.0,
            u'week_number': 1
        })

    def test_students_class_site_history_list_not_exists(self):
        response = self.client.get(reverse('student-classsite-history-list',
                                           kwargs={'username': 'adffd',
                                                   'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

        response = self.client.get(reverse('student-classsite-history-list',
                                           kwargs={'username': 'grace',
                                                   'code': '575'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)


class AdvisingApiAdvisorTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_advisors_list(self):
        response = self.client.get(reverse('advisor-list'))
        data = json.loads(response.content)

        self.assertEqual(data['count'], 6)
        self.assertEqual(response.status_code, 200)

    def test_advisors_detail_exists(self):
        response = self.client.get(reverse('advisor-detail',
                                           kwargs={'username': 'zander'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'username': u'zander',
                u'first_name': u'Zander',
                u'last_name': u'Agrippa',
                u'univ_id': u'20000001',
                u'url': u'http://testserver/api/advisors/zander/',
                u'students_url': (u'http://testserver/api/advisors/zander/'
                                  'students/'),
            }, data)

    def test_advisors_detail_not_exists(self):
        response = self.client.get(reverse('advisor-detail',
                                           kwargs={'username': 'asdfasdf'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

    def test_advisors_student_list_exists(self):
        response = self.client.get(reverse('advisor-students-list',
                                           kwargs={'username': 'zander'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 6)

    def test_advisors_student_list_not_exists(self):
        response = self.client.get(reverse('advisor-students-list',
                                           kwargs={'username': 'asdfasdf'}))

        self.assertEqual(response.status_code, 404)
        # data = json.loads(response.content)
        # self.assertDictEqual({u'detail': u'Not found.'}, data)


class AdvisingApiMentorTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_mentors_list(self):
        response = self.client.get(reverse('mentor-list'))
        data = json.loads(response.content)

        self.assertEqual(data['count'], 3)
        self.assertEqual(response.status_code, 200)

    def test_mentors_detail_exists(self):
        response = self.client.get(reverse('mentor-detail',
                                           kwargs={'username': 'zander'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'username': u'zander',
                u'first_name': u'Zander',
                u'last_name': u'Agrippa',
                u'univ_id': u'20000001',
                u'url': u'http://testserver/api/mentors/zander/',
                u'students_url': (u'http://testserver/api/mentors/zander/'
                                  'students/'),
                u'cohorts': [
                    {
                        u'code': u'SPPRO-F14',
                        u'description': u'Special Probation F14',
                        u'group': u'CSP',
                    },
                    {
                        u'code': u'SPPRO-W15',
                        u'description': u'Special Probation W15',
                        u'group': u'CSP',
                    },
                    {
                        u'code': u'SPPRO-F15',
                        u'description': u'Special Probation F15',
                        u'group': u'CSP',
                    },
                ],
            }, data)

    def test_mentors_detail_not_exists(self):
        response = self.client.get(reverse('mentor-detail',
                                           kwargs={'username': 'asdfasdf'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

    def test_mentors_student_list_exists(self):
        response = self.client.get(reverse('mentor-students-list',
                                           kwargs={'username': 'zander'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 16)

    def test_mentors_student_list_not_exists(self):
        response = self.client.get(reverse('mentor-students-list',
                                           kwargs={'username': 'asdfasdf'}))

        self.assertEqual(response.status_code, 404)


class AdvisingApiClassSiteTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_class_sites_list(self):
        response = self.client.get(reverse('class-site-list'))
        data = json.loads(response.content)

        self.assertEqual(data['count'], 6)
        self.assertEqual(response.status_code, 200)

    def test_class_sites_detail_exists(self):
        response = self.client.get(reverse('class-site-detail',
                                           kwargs={'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'url': u'http://testserver/api/class_sites/1/',
                u'code': u'1',
                u'description': u'Math 101',
                u'source_system': u'CTools',
                u'students_url': u'http://testserver/api/class_sites/'
                                 '1/students/',
                u'terms': [
                    u'Fall 2015'
                ],
            }, data)

    def test_class_sites_detail_not_exists(self):
        response = self.client.get(reverse('class-site-detail',
                                           kwargs={'code': '8'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)

    def test_class_sites_student_list_exists(self):
        response = self.client.get(reverse('class-site-students-list',
                                           kwargs={'code': '1'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 6)

    def test_class_sites_student_list_not_exists(self):
        response = self.client.get(reverse('class-site-students-list',
                                           kwargs={'code': '8'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            {
                u'count': 0,
                u'next': None,
                u'previous': None,
                u'results': []
            }, data)

    def test_class_sites_assignment_download_exists(self):
        response = self.client.get(reverse('class-site-assignment-download',
                                           kwargs={'code': '1'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Student,Assignment,Points Possible,Points Earned,'
                         'Class Points Possible,Class Points Earned,Grader '
                         'Comment,Due Date\r\ngrace,Assessment,22.0,0.0,327'
                         '36.0,0.0,,2015-09-14\r\ngrace,Exam 1,100.0,82.0,1'
                         '41900.0,102443.0,,2015-10-14\r\nshannon,Exam 1,10'
                         '0.0,98.0,600.0,500.0,Good!,2015-10-14\r\n',
                         response.content)

    def test_class_sites_assignment_download_not_exists(self):
        response = self.client.get(reverse('class-site-assignment-download',
                                           kwargs={'code': '8'}))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({u'detail': u'Not found.'}, data)


class AdvisingSerializersTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def test_status_weight_via_api(self):
        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})
        data = json.loads(response.content)

        serialized_weight = data['results'][0]['status_weight']

        self.assertEqual(serialized_weight, 10)

    def test_get_status_weight(self):
        test_student = advising.models.Student.objects.get(username="james")
        calculated_weight = (advising.serializers.StudentSerializer()
                             .get_status_weight(test_student))

        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})
        data = json.loads(response.content)

        serialized_weight = data['results'][0]['status_weight']

        self.assertEqual(serialized_weight, calculated_weight)
