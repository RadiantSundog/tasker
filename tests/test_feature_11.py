from django.test import TestCase
from django.db import models
from django.utils import timezone
from django.db.utils import OperationalError
from django.contrib.auth.models import User


class FeatureTests(TestCase):
    def test_task_model_exists(self):
        try:
            from tasks.models import Task  # noqa: F401
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models.Task'")

    def test_task_model_has_char_name_field(self):
        try:
            from tasks.models import Task

            name = Task.name
            self.assertIsInstance(
                name.field,
                models.CharField,
                msg="Task.name should be a character field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.name'")

    def test_task_model_has_name_with_max_length_200_characters(self):
        try:
            from tasks.models import Task

            name = Task.name
            self.assertEqual(
                name.field.max_length,
                200,
                msg="The max length of Task.name should be 200",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.name'")

    def test_task_model_has_name_that_is_not_nullable(self):
        try:
            from tasks.models import Task

            name = Task.name
            self.assertFalse(
                name.field.null,
                msg="Task.name should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.name'")

    def test_task_model_has_name_that_is_not_blank(self):
        try:
            from tasks.models import Task

            name = Task.name
            self.assertFalse(
                name.field.blank,
                msg="Task.name should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.name'")

    def test_task_model_has_date_time_start_date_field(self):
        try:
            from tasks.models import Task

            start_date = Task.start_date
            self.assertIsInstance(
                start_date.field,
                models.DateTimeField,
                msg="Task.start_date should be a date-time field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.start_date'")

    def test_task_model_has_start_date_that_is_not_nullable(self):
        try:
            from tasks.models import Task

            start_date = Task.start_date
            self.assertFalse(
                start_date.field.null,
                msg="Task.start_date should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.start_date'")

    def test_task_model_has_start_date_that_is_cannot_be_blank(self):
        try:
            from tasks.models import Task

            start_date = Task.start_date
            self.assertFalse(
                start_date.field.blank,
                msg="Task.start_date should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.start_date'")

    def test_task_model_has_date_time_due_date_field(self):
        try:
            from tasks.models import Task

            due_date = Task.due_date
            self.assertIsInstance(
                due_date.field,
                models.DateTimeField,
                msg="Task.due_date should be a date-time field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.due_date'")

    def test_task_model_has_due_date_that_is_not_nullable(self):
        try:
            from tasks.models import Task

            due_date = Task.due_date
            self.assertFalse(
                due_date.field.null,
                msg="Task.due_date should not be nullable",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.due_date'")

    def test_task_model_has_due_date_that_is_cannot_be_blank(self):
        try:
            from tasks.models import Task

            due_date = Task.due_date
            self.assertFalse(
                due_date.field.blank,
                msg="Task.due_date should not be allowed a blank value",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.due_date'")

    def test_task_model_has_project_foreign_key_field(self):
        try:
            from tasks.models import Task

            project = Task.project
            self.assertIsInstance(
                project.field,
                models.ForeignKey,
                msg="Task.project should be a foreign key field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.project'")

    def test_task_model_has_project_related_name_of_tasks(self):
        try:
            from tasks.models import Task

            project = Task.project
            self.assertEqual(
                project.field.related_query_name(),
                "tasks",
                msg="Task.project should have a related name of 'tasks'",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.project'")

    def test_task_model_has_project_related_to_projects_project(self):
        try:
            from projects.models import Project
            from tasks.models import Task

            project = Task.project
            self.assertEqual(
                project.field.related_model,
                Project,
                msg="Task.project should be related to the 'projects.Project' model",  # noqa: E501
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.project'")

    def test_task_model_has_project_has_on_delete_cascade(self):
        try:
            from tasks.models import Task

            project = Task.project
            self.assertEqual(
                project.field.remote_field.on_delete,
                models.CASCADE,
                msg="Task.project should have CASCADE for on delete",  # noqa: E501
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.project'")

    def test_task_model_has_assignee_foreign_key_field(self):
        try:
            from tasks.models import Task

            assignee = Task.assignee
            self.assertIsInstance(
                assignee.field,
                models.ForeignKey,
                msg="Task.assignee should be a foreign key field",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.assignee'")

    def test_task_model_has_assignee_related_name_of_tasks(self):
        try:
            from tasks.models import Task

            assignee = Task.assignee
            self.assertEqual(
                assignee.field.related_query_name(),
                "tasks",
                msg="Task.assignee should have a related name of 'tasks'",
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.assignee'")

    def test_task_model_has_assignee_related_to_auth_user(self):
        try:
            from django.contrib.auth.models import User
            from tasks.models import Task

            assignee = Task.assignee
            self.assertEqual(
                assignee.field.related_model,
                User,
                msg="Task.assignee should be related to the 'auth.User' model",  # noqa: E501
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.assignee'")

    def test_task_model_has_assignee_has_on_delete_set_null(self):
        try:
            from tasks.models import Task

            assignee = Task.assignee
            self.assertEqual(
                assignee.field.remote_field.on_delete,
                models.CASCADE,
                msg="Task.assignee should have CASCADE for on delete",  # noqa: E501
            )
        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Task'")
        except AttributeError:
            self.fail("Could not find 'Task.assignee'")

    def test_task_can_create_tasks(self):
        try:
            from projects.models import Project
            from tasks.models import Task

            user = User.objects.create_user("testuser")
            project = Project.objects.create(
                name="Test Project",
                description="Test Description",
                owner=user,
            )
            try:
                Task.objects.create(
                    name="Test Task",
                    start_date=timezone.now(),
                    due_date=timezone.now(),
                    project=project,
                    assignee=user,
                )
            except OperationalError:
                self.fail(
                    "Could not create a task because there was no database table"
                )

        except ModuleNotFoundError:
            self.fail("Could not find 'tasks.models'")
        except ImportError:
            self.fail("Could not find 'tasks.models.Project'")
