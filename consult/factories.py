from factory import DjangoModelFactory, SubFactory
from faker import Faker

from consult.accounts.models import User
from consult.consultations.models import Execution, Theme

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()
    email = fake.email()
    username = fake.user_name()
    email = fake.email()


class ExecutionFactory(DjangoModelFactory):
    class Meta:
        model = Execution

    type_choices = [choice[0] for choice in Execution.TYPE_CHOICES]
    type = fake.random_element(elements=type_choices)
    description = fake.sentence()


class ThemeFactory(DjangoModelFactory):
    class Meta:
        model = Theme

    name = fake.word()
    description = fake.sentence()
    execution = SubFactory(ExecutionFactory)
