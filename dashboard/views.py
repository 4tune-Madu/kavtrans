from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#Admin login//logout

def admin_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("dashboard_home")
        else:
            error = "Invalid credentials"

    return render(request, "dashboard/login.html", {"error": error})

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

#DAshboard home
from packages.models import Package


from packages.models import Package
from django.contrib.auth.decorators import login_required

@login_required(login_url="admin_login")
def dashboard_home(request):
    total_packages = Package.objects.count()
    delivered = Package.objects.filter(status="delivered").count()
    in_transit = Package.objects.filter(status="in_transit").count()
    pending = Package.objects.filter(status="pending").count()

    # Fetch the 5 most recent packages
    packages = Package.objects.order_by('-id')[:5]

    return render(request, "dashboard/home.html", {
        "total_packages": total_packages,
        "delivered": delivered,
        "in_transit": in_transit,
        "pending": pending,
        "packages": packages, 
    })

from packages.models import Package
from tracking.models import TrackingHistory

#Create package

@login_required(login_url="admin_login")
def package_create(request):

    if request.method == "POST":

        Package.objects.create(
            owner=request.user,  
            sender_name=request.POST.get("sender_name"),
            receiver_name=request.POST.get("receiver_name"),
            receiver_phone=request.POST.get("receiver_phone"),
            receiver_address=request.POST.get("receiver_address"),
            description=request.POST.get("description"),
            weight=request.POST.get("weight"),
        )

        return redirect("package_list")

    return render(request, "dashboard/package_create.html")

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

from django.shortcuts import get_object_or_404
from tracking.models import TrackingHistory

@login_required(login_url="admin_login")
def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == "POST":
        location = request.POST.get("location")
        status = request.POST.get("status")
        note = request.POST.get("note")

        # Create tracking history
        TrackingHistory.objects.create(
            package=package,
            location=location,
            status=status,
            note=note
        )

        # Update package current status and location
        package.status = status
        package.current_location = location
        package.save()

        return redirect("package_detail", package_id=package.id)

    return render(request, "dashboard/package_detail.html", {
        "package": package
    })



from core.models import DonationCause

# dashboard/views.py
from core.models import DonationCause
from django.db.models import Sum

def donations(request):
    causes = DonationCause.objects.filter(is_active=True)
    total_raised = DonationCause.objects.aggregate(total=Sum('amount_raised'))['total'] or 0
    total_target = DonationCause.objects.aggregate(total=Sum('target_amount'))['total'] or 0
    total_causes = causes.count()

    context = {
        "causes": causes,
        "total_raised": total_raised,
        "total_target": total_target,
        "total_causes": total_causes,
    }

    return render(request, "dashboard/donation.html", context)

from django.shortcuts import render, get_object_or_404
from core.models import DonationCause

def donate_to_cause(request, cause_id):
    cause = get_object_or_404(DonationCause, id=cause_id)

    return render(request, "dashboard/donate_to_cause.html", {
        "cause": cause
    })


# dashboard/views.py

from core.models import PaymentAccount
from django.shortcuts import render, redirect

def payment_accounts(request):

    accounts = PaymentAccount.objects.all()

    if request.method == "POST":
        account_type = request.POST.get("account_type")
        name = request.POST.get("name")
        details = request.POST.get("details")

        PaymentAccount.objects.create(
            account_type=account_type,
            name=name,
            details=details
        )

        return redirect("payment_accounts")

    return render(request, "dashboard/payment_accounts.html", {
        "accounts": accounts
    })

def delete_payment_account(request, id):
    account = PaymentAccount.objects.get(id=id)
    account.delete()
    return redirect("payment_accounts")



#Admin ACC payments
from core.models import PaymentAccount
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="admin_login")
def payment_accounts(request):
    accounts = PaymentAccount.objects.all().order_by("-id")
    return render(request, "dashboard/payment_accounts.html", {"accounts": accounts})


@login_required(login_url="admin_login")
def add_payment_account(request):
    if request.method == "POST":
        account_type = request.POST.get("account_type")
        name = request.POST.get("name")
        details = request.POST.get("details")

        PaymentAccount.objects.create(
            account_type=account_type,
            name=name,
            details=details
        )

        messages.success(request, "Payment account added successfully.")
        return redirect("payment_accounts")

    return render(request, "dashboard/add_payment_account.html")


@login_required(login_url="admin_login")
def edit_payment_account(request, id):
    account = get_object_or_404(PaymentAccount, id=id)

    if request.method == "POST":
        account.account_type = request.POST.get("account_type")
        account.name = request.POST.get("name")
        account.details = request.POST.get("details")
        account.is_active = request.POST.get("is_active") == "on"
        account.save()

        messages.success(request, "Payment account updated.")
        return redirect("payment_accounts")

    return render(request, "dashboard/edit_payment_account.html", {"account": account})


@login_required(login_url="admin_login")
def delete_payment_account(request, id):
    account = get_object_or_404(PaymentAccount, id=id)
    account.delete()

    messages.success(request, "Payment account deleted.")
    return redirect("payment_accounts")