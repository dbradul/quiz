from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from quiz.api.serializers import TestDetailSerializer, QuestionSerializer
from quiz.models import Test, Question

TESTS_URL = reverse('api:tests-list')
# TEST_DETAILS_URL = reverse('api:test-details')


class PublicTestsApiTests(TestCase):
    """Test the publicly available tests API"""
    fixtures = [
        'quiz/tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_tests_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(TESTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_test_details_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(reverse('api:test-details', args=(1,)))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_test_results_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(reverse('api:test-results-list', args=(1,)))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestsApiTests(TestCase):
    fixtures = [
        'quiz/tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@quiz.com',
            'password'
        )

        self.client.force_authenticate(self.user)

    def test_extended_view_detail(self):
        """Test viewing a test details with questions"""

        test = Test.objects.create(title='History test', level=Test.LEVEL_CHOICES.BASIC)
        test.questions.create(text='When was Socrat born?', order_number=1)
        test.questions.create(text='What was Cuban Missile Crisis about?', order_number=2)

        res = self.client.get(reverse('api:test-details', args=(test.id,)))

        serializer = QuestionSerializer(test.questions, many=True)
        self.assertEqual(res.data['questions'], serializer.data)
