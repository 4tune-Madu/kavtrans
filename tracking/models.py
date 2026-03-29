from django.db import models
from packages.models import Package


class TrackingHistory(models.Model):

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="tracking_updates"
    )

    location = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.package.tracking_number} - {self.location}"