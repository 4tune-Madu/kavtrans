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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import BankAccount, CryptoWallet, PayPalAccount

# Admin: List all payment accounts
# dashboard/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import BankAccount, CryptoWallet, PayPalAccount

@login_required(login_url="admin_login")
def payment_accounts(request):
    # Fetch all active and inactive accounts
    bank_accounts = BankAccount.objects.all()
    crypto_accounts = CryptoWallet.objects.all()
    paypal_accounts = PayPalAccount.objects.all()

    # Combine into a single list for the template
    accounts = []

    for acc in bank_accounts:
        accounts.append({
            "id": acc.id,
            "name": f"{acc.bank_name} - {acc.account_name}",
            "account_type": "bank",
            "details": f"Account: {acc.account_number} | Branch: {acc.branch} | SWIFT: {acc.swift_code}",
            "is_active": acc.is_active
        })

    for acc in crypto_accounts:
        accounts.append({
            "id": acc.id,
            "name": acc.currency,
            "account_type": "crypto",
            "details": f"Wallet: {acc.wallet_address} | Network: {acc.network or 'N/A'}",
            "is_active": acc.is_active
        })

    for acc in paypal_accounts:
        accounts.append({
            "id": acc.id,
            "name": acc.email,
            "account_type": "paypal",
            "details": f"PayPal Email: {acc.email}",
            "is_active": acc.is_active
        })

    # Sort by newest first
    accounts.sort(key=lambda x: x["id"], reverse=True)

    return render(request, "dashboard/payment_accounts.html", {"accounts": accounts})


# Admin: Add payment account
@login_required(login_url="admin_login")
def add_payment_account(request):
    if request.method == "POST":
        account_type = request.POST.get("account_type")

        if account_type == "bank":
            BankAccount.objects.create(
                account_name=request.POST.get("account_name"),
                account_number=request.POST.get("account_number"),
                bank_name=request.POST.get("bank_name"),
                swift_code=request.POST.get("swift_code"),
                branch=request.POST.get("branch"),
                currency=request.POST.get("currency", "USD"),
                notes=request.POST.get("notes", ""),
                is_active=request.POST.get("is_active") == "on"
            )

        elif account_type == "crypto":
            CryptoWallet.objects.create(
                currency=request.POST.get("currency"),
                wallet_address=request.POST.get("wallet_address"),
                network=request.POST.get("network", ""),
                notes=request.POST.get("notes", ""),
                is_active=request.POST.get("is_active") == "on"
            )

        elif account_type == "paypal":
            PayPalAccount.objects.create(
                email=request.POST.get("email"),
                notes=request.POST.get("notes", ""),
                is_active=request.POST.get("is_active") == "on"
            )

        messages.success(request, "Payment account added successfully.")
        return redirect("payment_accounts")

    return render(request, "dashboard/add_payment_account.html")


# Admin: Edit payment account
from django.shortcuts import get_object_or_404, redirect, render
from core.models import BankAccount, CryptoWallet, PayPalAccount
from django.contrib import messages

MODEL_MAP = {
    "bank": BankAccount,
    "crypto": CryptoWallet,
    "paypal": PayPalAccount
}



@login_required(login_url="admin_login")
def edit_payment_account(request, account_type, id):
    # Get model class
    Model = MODEL_MAP.get(account_type)
    if not Model:
        messages.error(request, "Invalid account type.")
        return redirect("payment_accounts")

    account = get_object_or_404(Model, id=id)

    if request.method == "POST":
        # Update fields dynamically
        if account_type == "bank":
            account.account_name = request.POST.get("account_name")
            account.account_number = request.POST.get("account_number")
            account.bank_name = request.POST.get("bank_name")
            account.swift_code = request.POST.get("swift_code")
            account.branch = request.POST.get("branch")
        elif account_type == "crypto":
            account.currency = request.POST.get("currency")
            account.wallet_address = request.POST.get("wallet_address")
            account.network = request.POST.get("network")
        elif account_type == "paypal":
            account.email = request.POST.get("email")

        account.is_active = request.POST.get("is_active") == "on"
        account.save()
        messages.success(request, "Payment account updated.")
        return redirect("payment_accounts")

    # Pass account_type separately for template logic
    return render(request, "dashboard/edit_payment_account.html", {
        "account": account,
        "account_type": account_type
    })


def delete_payment_account(request, account_type, id):
    Model = MODEL_MAP.get(account_type)
    account = get_object_or_404(Model, id=id)
    account.delete()
    messages.success(request, "Payment account deleted.")
    return redirect("payment_accounts")

