from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Report(models.Model):
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
    timestamp_start = models.IntegerField(null=True, blank=True)
    timestamp_end = models.IntegerField(null=True, blank=True)
