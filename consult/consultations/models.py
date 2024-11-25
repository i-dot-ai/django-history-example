import uuid

from django.db import models
from simple_history.models import HistoricalRecords


class UUIDPrimaryKeyModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        abstract = True


class Execution(TimeStampedModel, UUIDPrimaryKeyModel):
    class Type(models.TextChoices):
        SENTIMENT = "sentiment", "Sentiment"
        THEME_GENERATION = "theme_generation", "Theme Generation"
        THEME_MAPPING = "theme_mapping", "Theme Mapping"
        OTHER = "other", "Other"

    type = models.CharField(max_length=20, choices=Type)
    description = models.TextField()


class Theme(TimeStampedModel, UUIDPrimaryKeyModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)

    history = HistoricalRecords()

