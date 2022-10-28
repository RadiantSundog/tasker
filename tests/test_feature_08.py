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

    def test_projects_list_is_protected(self):
        response = self.client.get(reverse("list_projects"))
        self.assertEqual(
            response.status_code,
            302,
            msg="Project list view is not protected",
        )
        self.assertTrue(
            response.headers.get("Location").startswith(reverse("login")),
            msg="Project list view did not redirect to login page",
        )

    def test_projects_list_shows_no_member_projects_when_none_exist(self):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        self.login()
        project = Project.objects.create(name="Project", description="Project")
        project.owner = self.alisha
        project.save()
        response = self.client.get(reverse("list_projects"))
        document = Document()
        document.feed(response.content.decode("utf-8"))
        self.assertEqual(
            response.status_code,
            200,
            msg="Redirected for logged in user",
        )
        self.assertIn(
            "You are not assigned to any projects",
            document.select("html").inner_text(),
            msg="Did not find 'You are not assigned to any projects' in list view",  # noqa: E501
        )

    def test_projects_list_shows_no_projects_when_member_of_one(self):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        self.login()
        project = Project.objects.create(name="ZZZZZZ", description="AAAAAA")
        project.owner = self.noor
        project.save()
        response = self.client.get(reverse("list_projects"))
        document = Document()
        document.feed(response.content.decode("utf-8"))
        self.assertEqual(
            response.status_code,
            200,
            msg="Redirected for logged in user",
        )
        self.assertIn(
            "ZZZZZZ",
            document.select("html").inner_text(),
            msg="Did not find project name in list view",  # noqa: E501
        )
