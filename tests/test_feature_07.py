from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .utils import Document


class FeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get("/accounts/login/")
        self.content = self.response.content.decode("utf-8")
        self.document = Document()
        self.document.feed(self.content)

    def test_login_resolves_to_accounts_login(self):
        path = reverse("login")
        self.assertEqual(
            path,
            "/accounts/login/",
            msg="Could not resolve path name 'login' to '/accounts/login/",
        )

    def test_accounts_login_returns_200(self):
        self.assertEqual(
            self.response.status_code,
            200,
            msg="Did not get the login page",
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
        if form:
            self.assertIn(
                "method",
                form.attrs,
                msg="Did not find 'method' for the form",
            )
            method = form.attrs.get("method")
            if method:
                self.assertEqual(
                    method.lower(),
                    "post",
                    msg="Form was not a post form",
                )

    def test_form_has_username_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        if not form:
            self.fail(
                "Did not find the form at the path html > body > main > div > form"
            )
        inputs = form.get_all_children("input")
        username = None
        for input in inputs:
            if input.attrs.get("name") == "username":
                username = input
                break
        self.assertIsNotNone(
            username,
            msg="Could not find the username input",
        )

    def test_form_has_password_input(self):
        form = self.document.select("html", "body", "main", "div", "form")
        if not form:
            self.fail(
                "Did not find the form at the path html > body > main > div > form"
            )
        inputs = form.get_all_children("input")
        password = None
        for input in inputs:
            if input.attrs.get("name") == "password":
                password = input
                break
        self.assertIsNotNone(
            password,
            msg="Could not find the password input",
        )

    def test_form_has_button(self):
        form = self.document.select("html", "body", "main", "div", "form")
        if not form:
            self.fail(
                "Did not find the form at the path html > body > main > div > form"
            )
        buttons = form.get_all_children("button")
        button = None
        for button in buttons:
            if button.inner_text().strip() == "Login":
                button = button
                break
        self.assertIsNotNone(
            button,
            msg="Could not find the 'Login' button",
        )

    def test_login_works(self):
        User.objects.create_user("noor", password="1234abcd.")
        response = self.client.post(
            reverse("login"),
            {"username": "noor", "password": "1234abcd."},
        )
        self.assertEqual(
            response.status_code,
            302,
            msg="Login does not seem to work",
        )

    def test_login_fails_for_unknown_user(self):
        response = self.client.post(
            reverse("login"),
            {"username": "noor", "password": "1234abcd."},
        )
        self.assertEqual(
            response.status_code,
            200,
            msg="Login does not seem to work",
        )
