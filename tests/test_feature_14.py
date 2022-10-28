from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Document


class FeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.noor_credentials = {"username": "noor", "password": "1234abcd."}
        self.noor = User.objects.create_user(**self.noor_credentials)
        self.alisha = User.objects.create_user(
            username="alisha", password="1234abcd."
        )
        self.client.post(reverse("login"), self.noor_credentials)
        self.response = self.client.get("/projects/create/")
        self.content = self.response.content.decode("utf-8")
        self.document = Document()
        self.document.feed(self.content)

    def test_create_project_resolves_to_accounts_create_project(self):
        path = reverse("create_project")
        self.assertEqual(
            path,
            "/projects/create/",
            msg="Could not resolve path name 'create_project' to '/projects/create/",
        )

    def test_accounts_create_project_returns_200(self):
        self.assertEqual(
            self.response.status_code,
            200,
            msg="Did not get the create project page",
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

    def test_form_has_password_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        textareas = form.get_all_children("textarea")
        description = None
        for textarea in textareas:
            if textarea.attrs.get("name") == "description":
                description = textarea
                break
        self.assertIsNotNone(
            description,
            msg="Could not find the description textarea",
        )

    def test_form_has_owner_select(self):
        form = self.document.select("html", "body", "main", "div", "form")
        selects = form.get_all_children("select")
        owner = None
        for select in selects:
            if select.attrs.get("name") == "owner":
                owner = select
                break
        self.assertIsNotNone(
            owner,
            msg="Could not find the owner select",
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

    def test_create_project_works(self):
        response = self.client.post(
            reverse("create_project"),
            {
                "name": "ZZZZZZ",
                "description": "AAAAAA",
                "owner": str(self.noor.id),
            },
        )
        self.assertEqual(
            response.status_code,
            302,
            msg="Project creation does not seem to work",
        )

    def test_create_redirects_to_list_of_projects(self):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        response = self.client.post(
            reverse("create_project"),
            {
                "name": "ZZZZZZ",
                "description": "AAAAAA",
                "owner": str(self.noor.id),
            },
        )
        Project.objects.get(name="ZZZZZZ")
        self.assertEqual(
            response.headers.get("Location"),
            reverse("list_projects"),
            msg="Create does not redirect to detail",
        )

    def test_list_view_has_link_to_create(self):
        response = self.client.get(reverse("list_projects"))
        content = response.content.decode("utf-8")
        document = Document()
        document.feed(content)
        html = document.select("html")
        links = html.get_all_children("a")
        create_link = None
        for link in links:
            if link.attrs.get("href") == reverse("create_project"):
                create_link = link
                break
        self.assertIsNotNone(
            create_link,
            msg="Could not find the create link for projects on the list view",
        )
