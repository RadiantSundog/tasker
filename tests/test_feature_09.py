from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class FeatureTests(TestCase):
    def setUp(self):
        self.client = Client()

    def login(self):
        self.noor_credentials = {"username": "noor", "password": "1234abcd."}
        self.noor = User.objects.create_user(**self.noor_credentials)
        self.alisha = User.objects.create_user(
            username="alisha", password="1234abcd."
        )
        self.client.post(reverse("login"), self.noor_credentials)

    def test_logout_resolves_to_accounts_logout(self):
        path = reverse("logout")
        self.assertEqual(
            path,
            "/accounts/logout/",
            msg="Could not resolve path name 'logout' to '/accounts/logout/",
        )

    def test_logout_redirects_to_login_page(self):
        self.login()
        response = self.client.get(reverse("logout"))
        self.assertEqual(
            response.status_code,
            302,
            msg="Did not get a redirect when logging out",
        )
        self.assertEqual(
            response.headers.get("Location"),
            reverse("login"),
            msg="Did not redirect to the login page",
        )

    def test_logout_cause_redirect_on_project_list_page(self):
        self.login()
        response = self.client.get(reverse("list_projects"))
        if response.status_code == 200:
            self.client.get(reverse("logout"))
            response = self.client.get(reverse("list_projects"))
            self.assertEqual(
                response.status_code,
                302,
                msg="Logout did not seem to work",
            )
