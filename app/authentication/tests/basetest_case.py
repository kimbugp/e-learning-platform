import logging
import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

STATUS_CODES_FAIL = (302, 403, 404)


def get_reverse(url, kwargs={}):
    try:
        url = reverse(url, kwargs=kwargs)
    except NoReverseMatch:
        url = url
    return url


def get_user_list(users):
    if isinstance(users, tuple):
        return users
    else:
        return [users]

class BaseTestCase(object):
    fixtures = ['users', 'subjects']
    current_user = 'anonymous'
    current_password = ''

    def setUp(self):
        # disable logging
        logging.disable(logging.INFO)

        # Set MEDIA_ROOT
        self.media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self.media_root

    def tearDown(self):
        cache.clear()

        # Clear MEDIA_ROOT folder
        shutil.rmtree(self.media_root)


class EIPTestCase(BaseTestCase, TestCase):
    user_success = ('kimbugp',)
    user_fail = ('test',)
    
    def user_login(self, user='kimbugp'):
        password = '{0}{0}'.format(user)
        import pdb; pdb.set_trace()
        self.client.login(username=user, password=password)
        self.current_user = user
        self.current_password = password

    def user_logout(self):
        self.client.logout()
        self.current_user = 'anonymous'
