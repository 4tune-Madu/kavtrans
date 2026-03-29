from django.db import models
from django.conf import settings
from .utils import generate_tracking_number


class Package(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("picked_up", "Picked Up"),
        ("in_transit", "In Transit"),
        ("arrived_facility", "Arrived At Facility"),
        ("out_for_delivery", "Out For Delivery"),
        ("delivered", "Delivered"),
    ]

    tracking_number = models.CharField(
        max_length=30,
        unique=True,
        default=generate_tracking_number,
        editable=False
    )


    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)

    receiver_phone = models.CharField(max_length=20)
    receiver_address = models.TextField()

    description = models.TextField()

    weight = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )

    current_location = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number

import random
from django.db import models

def generate_tracking_number():
    return f"KAT{random.randint(1000000000,9999999999)}"