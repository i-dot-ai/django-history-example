from django.core.management.base import BaseCommand

from consult.factories import ResponseFactory, UserFactory


def create_users(n: int) -> None:
    for _ in range(n):
        UserFactory()


def create_responses(n: int) -> None:
    # All Executions are theme generation for now
    for _ in range(n):
        ResponseFactory()


class Command(BaseCommand):
    help = "Populate the database with fake data - theme generation"

    def handle(self, *args, **kwargs):
        create_users(2)
        create_responses(30)
        self.stdout.write(self.style.SUCCESS("Successfully populated the database with fake data"))
