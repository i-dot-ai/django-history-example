from random import randint

from consult.factories import FrameworkFactory
from consult.consultations.models import Framework


def generate_dummy_framework():
    next_id = Framework.get_next_framework_id()
    for _ in range(0, randint(1, 5)):
        FrameworkFactory(framework_id=next_id)
    return next_id



