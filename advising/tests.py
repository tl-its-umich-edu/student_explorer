from django.test import TestCase
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from advising.serializers import StudentSummarySerializer
import json

import advising.models
from advising.models import Student


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
        c = advising.models.ClassSite.objects.get(pk=1)

        w = advising.models.WeeklyStudentClassSiteScore.objects.filter(
            student=s, class_site=c)

        self.assertEqual('Physics 130', str(w[0].class_site))
        self.assertEqual('graciela', str(w[0].student))
        self.assertEqual('78', str(w[0].score))
        self.assertEqual('2015-10-01', str(w[0].week_end_date))

    def test_WeeklyClassSiteScore(self):
        c = advising.models.ClassSite.objects.get(pk=1)

        w = advising.models.WeeklyClassSiteScore.objects.filter(
            class_site=c)

        self.assertEqual('Physics 130', str(w[0].class_site))
        self.assertEqual('9', str(w[0].score))
        self.assertEqual('2015-10-01', str(w[0].week_end_date))

    def test_WeeklyClassSiteScore_date_range(self):
        c = advising.models.ClassSite.objects.get(pk=1)
        t = advising.models.Term.objects.get(id=1)

        w = advising.models.WeeklyClassSiteScore.objects.filter(
            class_site=c,
            week_end_date__gte=t.begin_date,
            week_end_date__lte=t.end_date)

        self.assertEqual(1, len(w))

    def test_WeeklyStudentClassSiteStatus(self):
        s = advising.models.Student.objects.get(pk=1)
        c = advising.models.ClassSite.objects.get(pk=1)

        w = advising.models.WeeklyStudentClassSiteStatus.objects.filter(
            student=s, class_site=c)

        self.assertEqual('Physics 130', str(w[0].class_site))
        self.assertEqual('graciela', str(w[0].student))
        self.assertEqual('Green', str(w[0].status))
        self.assertEqual('2015-10-01', str(w[0].week_end_date))

    def test_SourceSystem(self):
        systems = advising.models.SourceSystem.objects.all()

        self.assertEqual(2, len(systems))

    def test_EventType(self):
        events = advising.models.EventType.objects.all()

        self.assertEqual(1, len(events))
        self.assertEqual(u'session start', events[0].description)

    def test_WeeklyStudentClassSiteEvent(self):
        s = advising.models.Student.objects.get(pk=1)
        c = advising.models.ClassSite.objects.get(pk=1)

        events = advising.models.WeeklyStudentClassSiteEvent.objects.filter(
            student=s, class_site=c)

        self.assertEqual(2, len(events))
        self.assertEqual('Physics 130', str(events[0].class_site))
        self.assertEqual('graciela', str(events[0].student))
        self.assertEqual(4, events[0].event_count)
        self.assertEqual('2015-10-03', str(events[0].week_end_date))


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
        response = self.client.get(reverse('advising-api-root'))
        data = json.loads(response.content)

        self.assertIsNone(data['username'], 'username should be None')

    def test_api_config_username_authenticated(self):
        username = 'burl'

        user = get_user_model().objects.get(username=username)
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('advising-api-root'))
        data = json.loads(response.content)

        self.assertEqual(data['username'], username,
                         'username should be "%s"' % username)


class AdvisingApiStudentTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_students(self):
        response = self.client.get(reverse('student-list'))

        self.assertEqual(response.status_code, 200)

    def test_students_search_with_results(self):
        response = self.client.get(reverse('student-list'), {'search': 'gra'})

        data = json.loads(response.content)

        self.assertEqual(2, len(data))

    def test_students_search_with_no_results(self):
        response = self.client.get(reverse('student-list'), {'search': 'asdf'})

        data = json.loads(response.content)

        self.assertEqual(0, len(data))

    def test_students_search_check_data(self):
        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})

        data = json.loads(response.content)

        self.assertEqual(1, len(data))
        self.assertEqual('james', data[0]['username'])


class AdvisingApiAdvisorTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def setUp(self):
        self.client = APIClient()

    def test_advisors_list(self):
        response = self.client.get(reverse('advisor-list'))
        data = json.loads(response.content)

        self.assertEqual(len(data), 6)
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
        self.assertEqual(len(data), 6)

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

    def test_advisors_list(self):
        response = self.client.get(reverse('mentor-list'))
        data = json.loads(response.content)

        self.assertEqual(len(data), 3)
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
                u'students_url': u'http://testserver/api/mentors/zander/students/'
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
        self.assertEqual(len(data), 17)

    def test_mentors_student_list_not_exists(self):
        response = self.client.get(reverse('mentor-students-list',
                                           kwargs={'username': 'asdfasdf'}))

        self.assertEqual(response.status_code, 404)


class AdvisingSerializersTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def test_status_weight_via_api(self):
        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})
        data = json.loads(response.content)

        serialized_weight = data[0]['status_weight']

        self.assertEqual(serialized_weight, 10)

    def test_get_status_weight(self):
        test_student = Student.objects.get(username="james")
        calculated_weight = StudentSummarySerializer().get_status_weight(test_student)

        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})
        data = json.loads(response.content)

        serialized_weight = data[0]['status_weight']

        self.assertEqual(serialized_weight, calculated_weight)
