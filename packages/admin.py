from django.contrib import admin
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):

    list_display = (
        "tracking_number",
        "receiver_name",
        "status",
        "current_location",
        "created_at",
    )

    search_fields = ("tracking_number", "receiver_name")