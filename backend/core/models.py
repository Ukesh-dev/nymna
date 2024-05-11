from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Report(models.Model):
    """
    A model representing a report.

    Attributes:
        STATUS_CHOICES (list): A list of tuples representing the possible statuses for a report.
        source (models.TextField): The source of the report.
        confidence (models.FloatField): The confidence level of the report, validated to be between 0 and 1.
        status (models.CharField): The status of the report, chosen from the STATUS_CHOICES list.
        timestamp_start (models.IntegerField): The start timestamp of the report, optional.
        timestamp_end (models.IntegerField): The end timestamp of the report, optional.
        video (models.CharField): The video associated with the report, optional.
    """

    STATUS_CHOICES = [
        ('minor', 'Minor'),
        ('mediocre', 'Mediocre'),
        ('severe', 'Severe'),
    ]

    source = models.TextField()
    confidence = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ],
        default=0
    )
    status = models.CharField(max_length=255, blank=True, null=True, choices=STATUS_CHOICES)
    timestamp_start = models.DateTimeField(null=True, blank=True)
    timestamp_end = models.DateTimeField(null=True, blank=True)
    video = models.CharField(max_length=255, blank=True, null=True)
