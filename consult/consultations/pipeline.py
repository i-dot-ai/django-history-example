"""
Dummy methods to replicate parts of the pipeline to generate frameworks and mappings.
"""

from random import randint

from consult.consultations.models import FrameworkTheme, ResponseMapping
from consult.factories import FrameworkFactory


def generate_dummy_framework():
    next_id = FrameworkTheme.get_next_framework_id()
    for _ in range(0, randint(1, 5)):
        FrameworkFactory(framework_id=next_id, user=None, parent=None)
    return next_id


def generate_mapping(responses, framework_id: int):
    themes = FrameworkTheme.objects.filter(framework_id=framework_id).order_by("?")
    number_themes = themes.count()

    for response in responses:
        theme_for_response = themes[randint(0, number_themes - 1)]
        ResponseMapping(response=response, framework_theme=theme_for_response).save()
