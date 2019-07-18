
from django.contrib.auth import get_user_model
from django.urls import reverse

from .basetest_case import EIPTestCase

User = get_user_model()


class ChangePasswordTestCase(EIPTestCase):
    def change_password(self, fail=True):

        # Fetch the change passwort page
        response = self.client.get(reverse('user:change_password'))

        if fail:
            self.assertEqual(response.status_code, 302)
        else:
            self.assertEqual(response.status_code, 200)

        # Fill in the change password form
        form_data = {'old_password': 'soultechsoultech',
                     'new_password1': 'secret',
                     'new_password2': 'secret'}

        response = self.client.post(
            reverse('user:change_password'), form_data)
        self.assertEqual(response.status_code, 302)

        # Check the new password was accepted
        user = User.objects.get(username='kimbugp')
        if fail:
            import pdb; pdb.set_trace()
            self.assertTrue(user.check_password('testtest'))
        else:
            self.assertTrue(user.check_password('123'))

    def test_change_password_anonymous(self):
        self.change_password()

    def test_copy_workout_logged_in(self, fail=True):
        self.user_login('soultech')
        self.change_password(fail=False)
