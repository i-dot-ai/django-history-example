import factory
from faker import Faker

from consult.accounts.models import User
from consult.consultations.models import Execution, FrameworkTheme, Theme

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())


class ExecutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Execution

    type = factory.LazyAttribute(
        lambda _: fake.random_element(elements=[choice[0] for choice in Execution.Type.choices])
    )
    description = factory.LazyAttribute(lambda _: fake.sentence())


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Theme

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence())
    execution = factory.SubFactory(ExecutionFactory)


class FrameworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FrameworkTheme

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence())
    framework_id = factory.LazyAttribute(lambda _: FrameworkTheme.get_next_framework_id())
