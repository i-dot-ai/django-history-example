from django.core.management.base import BaseCommand

from consult.consultations.models import Execution
from consult.factories import ExecutionFactory, ThemeFactory, UserFactory


def create_users(n: int) -> None:
    for _ in range(n):
        UserFactory()


def create_executions_and_themes(n: int) -> None:
    # All Executions are theme generation for now
    for _ in range(n):
        execution = ExecutionFactory(type=Execution.Type.THEME_GENERATION)
        for _ in range(3, 5):
            ThemeFactory(execution=execution)


class Command(BaseCommand):
    help = "Populate the database with fake data - theme generation"

    def handle(self, *args, **kwargs):
        create_users(2)
        create_executions_and_themes(3)
        self.stdout.write(self.style.SUCCESS("Successfully populated the database with fake data"))
