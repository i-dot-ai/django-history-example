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
    TYPE_CHOICES = [
        ("sentiment", "Sentiment"),
        ("theme_generation", "Theme Generation"),
        ("theme_mapping", "Theme Mapping"),
        ("other", "Other"),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()


class Theme(TimeStampedModel, UUIDPrimaryKeyModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)

    history = HistoricalRecords()
