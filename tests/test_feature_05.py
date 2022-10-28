from django.test import TestCase, Client

from .utils import Document

# from projects.models import Project


class FeatureTests(TestCase):
    def test_can_get_projects_urlpatterns(self):
        try:
            from projects.urls import urlpatterns  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find module 'projects.urls'")
        except ImportError:
            self.fail("Could not find 'projects.urls.urlpatterns'")

    def test_list_response_is_200(self):
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            self.assertEqual(
                response.status_code,
                200,
                msg="Did not get a 200 OK for the path projects/",
            )

    def test_page_has_fundamental_five(self):
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            self.assertTrue(
                document.has_fundamental_five(),
                msg="The response did not have the fundamental five",
            )

    def test_list_html_has_main_tag(self):
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            self.assertIsNotNone(
                document.select("html", "body", "main"),
                msg="The response did not have a main tag as a direct child of the body",  # noqa: E501
            )

    def test_main_tag_has_a_div_tag(self):
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            self.assertIsNotNone(
                document.select("html", "body", "main", "div"),
                msg="The response did not have a div tag as a direct child of the main",  # noqa: E501
            )

    def test_div_tag_has_an_h1_tag_with_content_my_projects(self):
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            h1 = document.select("html", "body", "main", "div", "h1")
            self.assertIsNotNone(
                h1,
                msg="The response did not have an h1 tag as a direct child of the div",  # noqa: E501
            )
            self.assertIn(
                "My Projects",
                h1.inner_text(),
                msg="h1 did not have content 'My Projects'",
            )

    def test_div_tag_has_a_p_tag_when_no_projects_with_message(self):
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            p = document.select("html", "body", "main", "div", "p")
            self.assertIsNotNone(
                p,
                msg="The response did not have a p tag as a direct child of the div",  # noqa: E501
            )
            self.assertIn(
                "You are not assigned to any projects",
                p.inner_text(),
                msg="p tag did not have content 'You are not assigned to any projects'",  # noqa: E501
            )

    def test_div_tag_has_a_table_with_headers_name_and_number(
        self,
    ):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        Project.objects.bulk_create(
            [
                Project(name="ZZZZZZ", description="AAAAA"),
            ]
        )
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            table = document.select("html", "body", "main", "div", "table")
            self.assertIsNotNone(
                table,
                msg="The response did not have a table tag as a direct child of the div",  # noqa: E501
            )
            self.assertIn(
                "Name",
                table.inner_text(),
                msg="table did not have 'Name' header in it",
            )
            self.assertIn(
                "Number of tasks",
                table.inner_text(),
                msg="table did not have 'Number of tasks' in it'",
            )

    def test_div_tag_has_a_table_tag_when_projects_exist_with_project_names(
        self,
    ):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        Project.objects.bulk_create(
            [
                Project(name="ZZZZZZ", description="AAAAA"),
                Project(name="YYYYYY", description="BBBBB"),
            ]
        )
        client = Client()
        response = client.get("/projects/")
        if (
            response.status_code != 302
            or not response.has_header("Location")
            or not response.headers.get("Location", "").startswith(
                "/accounts/login/"
            )
        ):
            content = response.content.decode("utf-8")
            document = Document()
            document.feed(content)
            table = document.select("html", "body", "main", "div", "table")
            self.assertIsNotNone(
                table,
                msg="The response did not have a table tag as a direct child of the div",  # noqa: E501
            )
            self.assertIn(
                "ZZZZZZ",
                table.inner_text(),
                msg="table did not have project name in it",
            )
            self.assertIn(
                "YYYYYY",
                table.inner_text(),
                msg="table did not have project name in it",
            )
