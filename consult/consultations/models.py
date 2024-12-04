import uuid

from django.db import models
from simple_history.models import HistoricalRecords

# For now, let's assume we have one consultation and one question


class UUIDPrimaryKeyModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Execution(UUIDPrimaryKeyModel):
    class Type(models.TextChoices):
        SENTIMENT = "sentiment", "Sentiment"
        THEME_GENERATION = "theme_generation", "Theme Generation"
        THEME_MAPPING = "theme_mapping", "Theme Mapping"
        OTHER = "other", "Other"

    type = models.CharField(max_length=20, choices=Type)
    description = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    def get_initial_themes_for_execution(self):
        all_created_themes = Theme.history.filter(execution=self, history_type="+")
        # proxy for initial create (user created ones will have history_user)
        themes_not_created_by_user = all_created_themes.filter(history_user=None)
        return themes_not_created_by_user


class Theme(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    history = HistoricalRecords()


class Response(UUIDPrimaryKeyModel):
    response = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)


class FrameworkTheme(UUIDPrimaryKeyModel):
    """A framework_id groups a bunch of themes that will be used for mapping."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    framework_id = models.IntegerField()  # Is this the right name?
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    @classmethod
    def get_next_framework_id(cls):
        last_framework = cls.objects.all().order_by("framework_id").last()
        return last_framework.framework_id + 1 if last_framework else 1

    def get_theme_history(self):
        parents = []
        current = self
        while current.parent is not None:
            parents.append(current.parent)
            current = current.parent
        return parents


class ResponseMapping(UUIDPrimaryKeyModel):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    framework_theme = models.ForeignKey(FrameworkTheme, on_delete=models.CASCADE)

    history = HistoricalRecords()

