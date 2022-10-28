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
        self.response = self.client.get("/tasks/create/")
        self.content = self.response.content.decode("utf-8")
        self.document = Document()
        self.document.feed(self.content)
        self.project = Project.objects.create(
            name="ZZZZZZ",
            description="AAAAAA",
            owner=self.noor,
        )

    def login(self):
        self.noor_credentials = {"username": "noor", "password": "1234abcd."}
        self.noor = User.objects.create_user(**self.noor_credentials)
        self.alisha = User.objects.create_user(
            username="alisha", password="1234abcd."
        )
        self.client.post(reverse("login"), self.noor_credentials)

    def test_create_tasks_resolves_to_path(self):
        path = reverse("create_task")
        self.assertEqual(
            path,
            "/tasks/create/",
            msg="The 'create_task' did not resolve to the expected path",
        )

    def test_project_detail_page_has_link_to_create_task(self):
        response = self.client.get(
            reverse("show_project", args=[self.project.id])
        )
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        html = document.select("html")
        links = html.get_all_children("a")
        create_link = None
        for link in links:
            if link.attrs.get("href") == reverse("create_task"):
                create_link = link
                break
        self.assertIsNotNone(
            create_link,
            msg="Could not find the link to create task on the project detail page",  # noqa: E501
        )

    def test_accounts_create_project_returns_200(self):
        self.assertEqual(
            self.response.status_code,
            200,
            msg="Did not get the create task page",
        )

    def test_page_has_fundamental_five(self):
        self.assertTrue(
            self.document.has_fundamental_five(),
            msg="The response did not have the fundamental five",
        )

    def test_form_is_post(self):
        form = self.document.select("html", "body", "main", "div", "form")
        self.assertIsNotNone(
            form,
            msg=(
                "Did not find the form at the path "
                "html > body > main > div > form"
            ),
        )
        self.assertIn(
            "method",
            form.attrs,
            msg="Did not find 'method' for the form",
        )
        self.assertEqual(
            form.attrs.get("method").lower(),
            "post",
            msg="Form was not a post form",
        )

    def test_form_has_name_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        name = None
        for input in inputs:
            if input.attrs.get("name") == "name":
                name = input
                break
        self.assertIsNotNone(
            name,
            msg="Could not find the name input",
        )

    def test_form_has_start_date_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        start_date = None
        for input in inputs:
            if input.attrs.get("name") == "start_date":
                start_date = input
                break
        self.assertIsNotNone(
            start_date,
            msg="Could not find the start date input",
        )

    def test_form_has_due_date_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        due_date = None
        for input in inputs:
            if input.attrs.get("name") == "due_date":
                due_date = input
                break
        self.assertIsNotNone(
            due_date,
            msg="Could not find the due date input",
        )

    def test_form_has_project_select(self):
        form = self.document.select("html", "body", "main", "div", "form")
        selects = form.get_all_children("select")
        project = None
        for select in selects:
            if select.attrs.get("name") == "project":
                project = select
                break
        self.assertIsNotNone(
            project,
            msg="Could not find the project select",
        )

    def test_form_has_assignee_select(self):
        form = self.document.select("html", "body", "main", "div", "form")
        selects = form.get_all_children("select")
        assignee = None
        for select in selects:
            if select.attrs.get("name") == "assignee":
                assignee = select
                break
        self.assertIsNotNone(
            assignee,
            msg="Could not find the assignee select",
        )

    def test_form_has_no_is_completed(self):
        form = self.document.select("html", "body", "main", "div", "form")
        inputs = form.get_all_children("input")
        is_completed = None
        for input in inputs:
            if input.attrs.get("name") == "is_completed":
                is_completed = input
                break
        self.assertIsNone(
            is_completed,
            msg="Found is completed when I shouldn't have",
        )

    def test_form_has_button(self):
        form = self.document.select("html", "body", "main", "div", "form")
        buttons = form.get_all_children("button")
        button = None
        for button in buttons:
            if button.inner_text().strip() == "Create":
                button = button
                break
        self.assertIsNotNone(
            button,
            msg="Could not find the 'Create' button",
        )

    def test_form_works(self):
        data = {
            "name": "YYYYYY",
            "start_date": timezone.now(),
            "due_date": timezone.now(),
            "project": str(self.project.id),
            "assignee": str(self.noor.id),
        }
        response = self.client.post(reverse("create_task"), data)
        self.assertEqual(
            response.status_code,
            302,
            msg="Create task form does not redirect on create",
        )
