from django.test import TestCase
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from advising.serializers import StudentSummarySerializer
import json

import advising.models
from advising.models import Student

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

    def test_students(self):
        response = self.client.get(reverse('student-list'))

        self.assertEqual(response.status_code, 200, 'Response should be 200')

    def test_students_search_with_results(self):
        response = self.client.get(reverse('student-list'), {'search': 'gra'})

        data = json.loads(response.content)

        self.assertEqual(2, len(data),
                         'Expected 2 entries in search for "gra"')

    def test_students_search_with_no_results(self):
        response = self.client.get(reverse('student-list'), {'search': 'asdf'})

        data = json.loads(response.content)

        self.assertEqual(0, len(data),
                         'Expected 2 entries in search for "asdf"')

    def test_students_search_check_data(self):
        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})

        data = json.loads(response.content)

        self.assertEqual(1, len(data),
                         'Expected 1 entries in search for "james"')
        self.assertEqual('james', data[0]['username'],
                         'Expected username "james"')

    def test_advisors(self):
        response = self.client.get(reverse('advisor-list'))

        self.assertEqual(response.status_code, 200, 'Response should be 200')


class AdvisingSerializersTestCase(TestCase):
    fixtures = ['dev_data.json', 'dev_users.json']
    client = None

    def test_status_weight_via_api(self):
        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})
        data = json.loads(response.content)

        serialized_weight = data[0]['status_weight']

        self.assertEqual(serialized_weight, 10)

    def  test_get_status_weight(self):
        test_student = Student.objects.get(username="james")
        calculated_weight = StudentSummarySerializer().get_status_weight(test_student)

        response = self.client.get(reverse('student-list'),
                                   {'search': 'james'})
        data = json.loads(response.content)

        serialized_weight = data[0]['status_weight']

        self.assertEqual(serialized_weight, calculated_weight)
