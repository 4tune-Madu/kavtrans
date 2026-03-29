import random
import datetime
from django.apps import apps


def generate_tracking_number():

    Package = apps.get_model("packages", "Package")

    prefix = "KAT"
    year = datetime.datetime.now().year

    while True:
        random_number = random.randint(100000, 999999)
        tracking_number = f"{prefix}-{year}-{random_number}"

        if not Package.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number