from django.shortcuts import render, redirect, get_object_or_404
from packages.models import Package
from .models import TrackingHistory
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="admin_login")
def add_tracking_update(request, tracking_number):
    package = get_object_or_404(Package, tracking_number=tracking_number)

    if request.method == "POST":
        location = request.POST.get("location")
        status = request.POST.get("status")
        note = request.POST.get("note")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        latitude = float(latitude) if latitude else None
        longitude = float(longitude) if longitude else None

        # 1️⃣ Create the tracking update as before
        TrackingHistory.objects.create(
            package=package,
            location=location,
            status=status,
            note=note,
            latitude=latitude,
            longitude=longitude
        )

        # 2️⃣ Update the package's current location and status
        package.current_location = location       # <-- updated
        package.status = status                   # <-- updated
        package.save()                            # <-- save changes to database

        # Optional: add a success message
        messages.success(request, "Tracking update added successfully.")

        # 3️⃣ Redirect to the tracking updates page for this package
        return redirect("tracking_updates", tracking_number=package.tracking_number)

    return render(request, "dashboard/add_tracking.html", {"package": package})

from django.shortcuts import render, get_object_or_404
from packages.models import Package
from .models import TrackingHistory
from django.contrib.auth.decorators import login_required


@login_required(login_url="admin_login")
def tracking_updates(request, tracking_number):

    package = get_object_or_404(Package, tracking_number=tracking_number)

    updates = TrackingHistory.objects.filter(
        package=package
    ).order_by("-timestamp")

    context = {
        "package": package,
        "updates": updates
    }

    return render(request, "dashboard/tracking_updates.html", context)


@login_required(login_url="admin_login")
def edit_tracking_update(request, update_id):
    update = get_object_or_404(TrackingHistory, id=update_id)
    package = update.package

    if request.method == "POST":
        location = request.POST.get("location")
        status = request.POST.get("status")
        note = request.POST.get("note")

        # Update the tracking update
        update.location = location
        update.status = status
        update.note = note
        update.save()

        # Update package's current location if this was the latest update
        latest_update = TrackingHistory.objects.filter(package=package).order_by('-timestamp').first()
        if latest_update:
            package.current_location = latest_update.location
            package.status = latest_update.status
            package.save()

        return redirect("tracking_updates", tracking_number=package.tracking_number)

    return render(request, "dashboard/edit_tracking_update.html", {"update": update})

@login_required(login_url="admin_login")
def delete_tracking_update(request, update_id):
    """
    Delete a tracking update and redirect back to the package tracking page.
    """
    update = get_object_or_404(TrackingHistory, id=update_id)
    tracking_number = update.package.tracking_number
    update.delete()  # Delete the record
    return redirect("tracking_updates", tracking_number=tracking_number)