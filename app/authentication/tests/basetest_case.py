import logging
import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse


class BaseTestCase(object):
    fixtures = ['users', 'subjects']
    current_user = 'anonymous'
    current_password = ''

    def setUp(self):
        # disable logging
        logging.disable(logging.INFO)
        self.media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self.media_root

    def tearDown(self):
        shutil.rmtree(self.media_root)


class EIPTestCase(BaseTestCase, TestCase):
    user_success = ('simon',)
    user_fail = ('test',)

    def user_login(self, user='simon', password='123'):
        self.client.login(username=user, password=password)
        self.current_user = user
        self.current_password = password

    def user_logout(self):
        self.client.logout()
        self.current_user = 'anonymous'
