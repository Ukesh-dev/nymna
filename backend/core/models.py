from django.db import models

# Create your models here.
class Report(models.Model):
    source = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    confidence = models.PositiveIntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=255, blank=True, null=True, choices=[
        ('minor', 'Minor'),
        ('mediocre', 'Mediocre'),
        ('severe', 'Severe'),
    ])