from packages.models import Package
from django.contrib.auth.decorators import login_required

@login_required(login_url="admin_login")
def package_list(request):
    status_filter = request.GET.get("status")
    
    packages = Package.objects.all().order_by("-created_at")
    
    if status_filter:
        packages = packages.filter(status=status_filter)
    
    return render(request, "dashboard/package_list.html", {
        "packages": packages,
        "status_filter": status_filter
    })