from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Document


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

    def test_logged_out_user_has_login_and_signup_links(self):
        response = self.client.get(reverse("login"))
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        nav = document.select("html", "body", "header", "nav")
        has_login = False
        has_signup = False
        links = nav.get_all_children("a")
        for link in links:
            if link.attrs.get("href", "").startswith(reverse("login")):
                has_login = True
            elif link.attrs.get("href", "").startswith(reverse("signup")):
                has_signup = True
        self.assertTrue(
            has_login and has_signup,
            msg="Could not find a login and signup link for a logged out user",
        )

    def test_logged_in_user_has_projects_tasks_and_logout_links(self):
        self.login()
        response = self.client.get(reverse("login"))
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        nav = document.select("html", "body", "header", "nav")
        has_logout = False
        has_projects = False
        has_tasks = False
        links = nav.get_all_children("a")
        for link in links:
            if link.attrs.get("href", "").startswith(reverse("logout")):
                has_logout = True
            elif link.attrs.get("href", "").startswith(
                reverse("list_projects")
            ):
                has_projects = True
            elif link.attrs.get("href", "").startswith(
                reverse("show_my_tasks")
            ):
                has_tasks = True
        self.assertTrue(
            has_logout and has_projects and has_tasks,
            msg="Could not find a logout, projects, and tasks link for a logged in user",  # noqa: E501
        )
