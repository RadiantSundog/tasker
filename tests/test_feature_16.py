from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .utils import Document


class FeatureTests(TestCase):
    def setUp(self):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        self.client = Client()
        self.login()
        self.no_task_response = self.client.get("/tasks/mine/")
        self.content = self.no_task_response.content.decode("utf-8")
        self.no_task_document = Document()
        self.no_task_document.feed(self.content)
        self.project = Project.objects.create(
            name="ZZZZZZ",
            description="AAAAAA",
            owner=self.noor,
        )
        try:
            from tasks.models import Task  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models.Task'")
        self.task = Task.objects.create(
            name="YYYYYY",
            start_date=timezone.now(),
            due_date=timezone.now(),
            project=self.project,
            assignee=self.noor,
        )
        self.task_response = self.client.get("/tasks/mine/")
        self.content = self.task_response.content.decode("utf-8")
        self.task_document = Document()
        self.task_document.feed(self.content)

    def login(self):
        self.noor_credentials = {"username": "noor", "password": "1234abcd."}
        self.noor = User.objects.create_user(**self.noor_credentials)
        self.alisha = User.objects.create_user(
            username="alisha", password="1234abcd."
        )
        self.client.post(reverse("login"), self.noor_credentials)

    def test_show_my_tasks_resolves_to_path(self):
        path = reverse("show_my_tasks")
        self.assertEqual(
            path,
            "/tasks/mine/",
            msg="The 'show_my_tasks' did not resolve to the expected path",
        )

    def test_my_tasks_with_no_tasks_shows_message(self):
        html = self.no_task_document.select("html")
        self.assertIn(
            "You have no tasks",
            html.inner_text(),
            msg="Did not find the message 'You have no tasks'",
        )

    def test_my_tasks_with_one_task_to_see_task_name(self):
        html = self.task_document.select("html")
        self.assertIn(
            "YYYYYY",
            html.inner_text(),
            msg="Did not find the name of the task assigned to the user",
        )

    def test_my_tasks_with_one_task_to_see_task_status(self):
        html = self.task_document.select("html")
        self.assertNotIn(
            "Done",
            html.inner_text(),
            msg="Found the word 'Done' when I shouldn't have",
        )

    def test_my_tasks_with_one_task_has_four_td_tags(self):
        html = self.task_document.select("html")
        cells = html.get_all_children("td")
        self.assertEqual(
            len(cells),
            4,
            msg="Should only have td tags for data rows",
        )

    def test_has_h1_tag_for_no_tasks(self):
        h1 = self.no_task_document.select("html", "body", "main", "div", "h1")
        self.assertIsNotNone(
            h1,
            msg="Could not find h1 tag at html > body > main > div > h1",
        )
        self.assertIn(
            "My Tasks",
            h1.inner_text(),
            msg="Could not find 'My Tasks' in the h1 tag",
        )

    def test_has_h1_tag_for_tasks(self):
        h1 = self.task_document.select("html", "body", "main", "div", "h1")
        self.assertIsNotNone(
            h1,
            msg="Could not find h1 tag at html > body > main > div > h1",
        )
        self.assertIn(
            "My Tasks",
            h1.inner_text(),
            msg="Could not find 'My Tasks' in the h1 tag",
        )
