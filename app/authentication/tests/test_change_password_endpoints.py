
from ..models import User
from django.urls import reverse

from .basetest_case import EIPTestCase


class ChangePasswordTestCase(EIPTestCase):
    def change_password(self, fail=True):

        # Fetch the change passwort page
        response = self.client.get(reverse('user:change_password'))

        if fail:
            self.assertEqual(response.status_code, 302)
        else:
            self.assertEqual(response.status_code, 200)

        # Fill in the change password form
        form_data = {'old_password': '123',
                     'new_password1': 'secret@2i1RE',
                     'new_password2': 'secret@2i1RE'}

        response = self.client.post(
            reverse('user:change_password'), form_data)
        return response

    def test_change_password_anonymous(self):
        response = self.change_password()
        user = User.objects.get(username='simon')

        self.assertFalse(user.check_password('secret@2i1RE'))

    def test_change_password_logged_in(self, fail=True):
        self.user_login()
        response = self.change_password(fail=False)
        user = User.objects.get(username='simon')
        self.assertTrue(user.check_password('secret@2i1RE'))
