from django.test import TestCase
from django.db import models
from django.db.utils import OperationalError
from django.contrib.auth.models import User


class FeatureTests(TestCase):
    def test_project_model_exists(self):
        try:
            from projects.models import Project  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")

    def test_project_model_has_char_name_field(self):
        try:
            from projects.models import Project

            name = Project.name
            self.assertIsInstance(
                name.field,
                models.CharField,
                msg="Project.name should be a character field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.name'")

    def test_project_model_has_name_with_max_length_200_characters(self):
        try:
            from projects.models import Project

            name = Project.name
            self.assertEqual(
                name.field.max_length,
                200,
                msg="The max length of Project.name should be 200",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.name'")

    def test_project_model_has_name_that_is_not_nullable(self):
        try:
            from projects.models import Project

            name = Project.name
            self.assertFalse(
                name.field.null,
                msg="Project.name should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.name'")

    def test_project_model_has_name_that_is_not_blank(self):
        try:
            from projects.models import Project

            name = Project.name
            self.assertFalse(
                name.field.blank,
                msg="Project.name should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.name'")

    def test_project_model_has_text_description_field(self):
        try:
            from projects.models import Project

            description = Project.description
            self.assertIsInstance(
                description.field,
                models.TextField,
                msg="Project.description should be a text field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.description'")

    def test_project_model_has_description_that_is_not_nullable(self):
        try:
            from projects.models import Project

            description = Project.description
            self.assertFalse(
                description.field.null,
                msg="Project.description should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.description'")

    def test_project_model_has_description_that_is_cannot_be_blank(self):
        try:
            from projects.models import Project

            description = Project.description
            self.assertFalse(
                description.field.blank,
                msg="Project.description should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.description'")

    def test_project_model_has_an_owner(self):
        try:
            from projects.models import Project

            owner = Project.owner
            self.assertIsInstance(
                owner.field,
                models.ForeignKey,
                msg="Project.owner should be a foreign key field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.owner'")

    def test_project_model_has_owner_related_name_of_projects(self):
        try:
            from projects.models import Project

            owner = Project.owner
            self.assertEqual(
                owner.field.related_query_name(),
                "projects",
                msg="Project.owner should have a related name of 'projects'",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.owner'")

    def test_project_model_has_owner_related_to_auth_user(self):
        try:
            from django.contrib.auth.models import User
            from projects.models import Project

            owner = Project.owner
            self.assertEqual(
                owner.field.related_model,
                User,
                msg="Project.owner should be related to the 'auth.User' model",  # noqa: E501
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.owner'")

    def test_project_model_has_nullable_owner(self):
        try:
            from projects.models import Project

            owner = Project.owner
            self.assertEqual(
                owner.field.null,
                True,
                msg="Project.owner should be nullable",  # noqa: E501
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.owner'")

    def test_project_can_create_projects(self):
        try:
            from projects.models import Project

            user = User.objects.create_user("testuser")

            try:
                Project.objects.create(
                    name="Test Project",
                    description="Test Description",
                    owner=user,
                )
            except OperationalError:
                self.fail(
                    "Could not create a project because there was no database table"
                )

        except ModuleNotFoundError:
            self.fail("Could not find 'projects.models'")
        except ImportError:
            self.fail("Could not find 'projects.models.Project'")
        except AttributeError:
            self.fail("Could not find 'Project.owner'")
