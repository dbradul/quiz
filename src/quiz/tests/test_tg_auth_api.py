import json
import re
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


class TGAuthApiTests(TestCase):
    fixtures = [
        'quiz/tests/fixtures/dump.json',
    ]

    AUTH_TOKEN_PATTERN = 'start\=([0-9a-fA-F\-]{36})$'
    TG_URL_PATTERN = f'https://t.me/hillel_quiz_bot\?{AUTH_TOKEN_PATTERN}'

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='user@quiz.com',
            password='password',
            tg_auth_token=uuid.uuid4()
        )

    def test_when_user_is_logged_out(self):
        """Request jwt token when not logged in"""
        self.client.logout()

        res = self.client.get(reverse('api:tg_introduce'))
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual('%s?next=%s' % (settings.LOGIN_URL, reverse('api:tg_introduce')), res.url)

    def test_when_user_is_logged_in(self):
        """Request jwt token when logged in"""
        self.client.force_login(self.user)

        res = self.client.get(reverse('api:tg_introduce'))
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRegexpMatches(res.url, self.TG_URL_PATTERN)

        auth_token = re.match(self.TG_URL_PATTERN, res.url).group(1)
        self.assertEqual(str(self.user.tg_auth_token), auth_token)

        res = self.client.get(reverse('api:tg_auth', args=(auth_token,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(res.content)['username'], self.user.username)

