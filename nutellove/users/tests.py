from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth

# import pprint

# Create your tests here.


class UserCreationFormTestCase(TestCase):
    """
    Testing a user creation
    """

    def test_user_registration_in_db(self):
        """
        Test the registration of a user in database
        """
        old_users = User.objects.count()

        response = self.client.post(reverse('users:register'), {
            'username': "test",
            'email': "test@est.fr",
            'password1': "mdptest1234",
            'password2': "mdptest1234",
        })

        # pp = pprint.PrettyPrinter()

        # pp.pprint(response)
        # pp.pprint(response.content.decode())

        new_users = User.objects.count()  # count users after
        self.assertEqual(new_users, old_users + 1)

    def test_registration_failed_password_too_short(self):

        response = self.client.post(reverse('users:register'), {
            'username': "test",
            'email': "test@est.fr",
            'password1': "1234",
            'password2': "1234",
        }, follow=True)

        self.assertIn(b"Ce mot de passe est trop court", response.content)


class UserLoginFormTestCase(TestCase):
    """
    Testing user loggin/logout
    """

    def setUp(self):

        User.objects.create_user(username="testuser", email="test@test.fr", password="mdptest1234")
        self.user = User.objects.get(username="testuser")

    def test_user_logged_in(self):
        """
        """
        username = self.user.username

        response = self.client.post(reverse('users:login'), {
            'username': username,
            'password': "mdptest1234",
        })

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_user_logged_out(self):
        """
        Test user logged out
        """

        response = self.client.get(reverse('users:logout'))

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class UserAccountPageTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username="testuser", email="test@test.fr", password="mdptest1234")
        self.user = User.objects.get(username="testuser")

        # connect our user
        self.client.post(reverse('users:login'), {
            'username': "testuser",
            'password': "mdptest1234",
        })

    def test_user_page_displays_user_name(self):
        """
        Test if the user page account displays the name of the user,
        and then if he's correctly connected and recognized
        """
        response = self.client.get(reverse('users:account'))

        self.assertIn(b"testuser", response.content)

    def test_change_user_password_success(self):

        response = self.client.post(reverse('users:change_password'), {
            'old_password': "mdptest1234",
            'new_password1': "mdpmodif1234",
            'new_password2': "mdpmodif1234"
        })

        self.assertRedirects(response, '/users/account/')

    def test_change_user_password_fail(self):

        response = self.client.post(reverse('users:change_password'), {
            # passing a wrong old password, to fail password change
            'old_password': "wrongpass",
            'new_password1': "mdpmodif1234",
            'new_password2': "mdpmodif1234"
        })

        self.assertIn(b"messagebar-error", response.content)
