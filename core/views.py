from django.shortcuts import render
from packages.models import Package
from tracking.models import TrackingHistory
from core.models import DonationCause          # ✅ ADD
from django.db.models import Sum               # ✅ ADD

def home(request):

    tracking_result = None
    latest_update = None

    tracking_number = request.GET.get("tracking_number")

    if tracking_number:
        try:
            tracking_result = Package.objects.get(
                tracking_number__iexact=tracking_number
            )
            latest_update = TrackingHistory.objects.filter(
                package=tracking_result
            ).order_by("-timestamp").first()

        except Package.DoesNotExist:
            tracking_result = "not_found"

    # ✅ DONATION DATA
    causes = DonationCause.objects.filter(is_active=True)
    total_raised = DonationCause.objects.aggregate(total=Sum('amount_raised'))['total'] or 0
    total_target = DonationCause.objects.aggregate(total=Sum('target_amount'))['total'] or 0
    total_causes = causes.count()

    return render(request, "core/home7.html", {
        "tracking_result": tracking_result,
        "latest_update": latest_update,
        "causes": causes,              # ✅
        "total_raised": total_raised,  # ✅
        "total_target": total_target,  # ✅
        "total_causes": total_causes,  # ✅
    })


# Donation Cause
from .models import DonationCause

def donation_page(request):
    causes = DonationCause.objects.all().order_by('-created_at')

    return render(request, "core/donations.html", {
        "causes": causes
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import DonationCause
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="admin_login")
def donation_causes(request):
    causes = DonationCause.objects.all()
    return render(request, "dashboard/donation_causes.html", {"causes": causes})

from decimal import Decimal, InvalidOperation

@login_required(login_url="admin_login")
def add_donation_cause(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        try:
            target_amount = Decimal(request.POST.get("target_amount") or "0")
            amount_raised = Decimal(request.POST.get("amount_raised") or "0")
        except InvalidOperation:
            messages.error(request, "Please enter valid numbers for amounts.")
            return redirect("add_donation_cause")

        image = request.FILES.get("image")

        DonationCause.objects.create(
            title=title,
            description=description,
            target_amount=target_amount,
            amount_raised=amount_raised,
            image=image
        )

        messages.success(request, "Donation cause added successfully.")
        return redirect("donation_causes")

    return render(request, "dashboard/add_donation_cause.html")

@login_required(login_url="admin_login")
def edit_donation_cause(request, cause_id):
    cause = get_object_or_404(DonationCause, id=cause_id)

    if request.method == "POST":
        cause.title = request.POST.get("title")
        cause.description = request.POST.get("description")
        cause.target_amount = request.POST.get("target_amount")
        cause.amount_raised = request.POST.get("amount_raised", 0)

        # update image if a new one is uploaded
        if "image" in request.FILES:
            cause.image = request.FILES["image"]

        cause.save()
        messages.success(request, "Donation cause updated successfully.")
        return redirect("donation_causes")

    return render(request, "dashboard/edit_donation_cause.html", {"cause": cause})


from django.db.models import Sum
from .models import DonationCause

@login_required(login_url="admin_login")
def donation_dashboard(request):
    causes = DonationCause.objects.all().order_by('-created_at')

    total_raised = DonationCause.objects.aggregate(
        total=Sum('amount_raised')
    )['total'] or 0

    total_target = DonationCause.objects.aggregate(
        total=Sum('target_amount')
    )['total'] or 0

    total_causes = causes.count()

    context = {
        "causes": causes,
        "total_raised": total_raised,
        "total_target": total_target,
        "total_causes": total_causes,
    }

    return render(request, "dashboard/donations.html", context)

from django.views.decorators.http import require_POST

@login_required(login_url="admin_login")
@require_POST
def delete_donation_cause(request, cause_id):
    cause = get_object_or_404(DonationCause, id=cause_id)
    cause.delete()
    messages.success(request, "Donation cause deleted successfully.")
    return redirect("donation_dashboard")


from django.shortcuts import render

def donation_success(request):
    return render(request, "donation_success.html")


from django.shortcuts import render

def donation_cancel(request):
    return render(request, "donation_cancel.html")





from django.shortcuts import render, redirect, get_object_or_404
from .models import DonationCause, PaymentAccount, Donation
from django.contrib.auth.decorators import login_required
import random

# STEP 1: ENTER AMOUNT
def donate_amount(request, cause_id):
    cause = get_object_or_404(DonationCause, id=cause_id)

    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            return render(request, "donate.html", {
                "cause": cause,
                "error": "Please enter amount"
            })

        # SAVE amount in session
        request.session['donation_amount'] = amount

        return redirect('choose_payment', cause_id=cause.id)

    return render(request, "dashboard/donate.html", {"cause": cause})


# STEP 2: CHOOSE PAYMENT
from django.shortcuts import render, get_object_or_404, redirect
from .models import DonationCause, BankAccount, CryptoWallet, PayPalAccount, Donation
import random

def choose_payment(request, cause_id):
    cause = get_object_or_404(DonationCause, id=cause_id)
    amount = request.session.get('donation_amount')

    if not amount:
        return redirect('donate_amount', cause_id=cause.id)

    if request.method == "POST":
        payment_type = request.POST.get("payment_type")
        if not payment_type:
            return render(request, "dashboard/choose_payment.html", {
                "cause": cause,
                "amount": amount,
                "error": "Please select a payment method"
            })

        # Save payment type in session
        request.session['payment_type'] = payment_type

        # If crypto, also save the selected currency
        if payment_type == 'crypto':
            crypto_currency = request.POST.get("crypto_currency")
            if not crypto_currency:
                return render(request, "dashboard/choose_payment.html", {
                    "cause": cause,
                    "amount": amount,
                    "error": "Please select a crypto currency"
                })
            request.session['crypto_currency'] = crypto_currency

        return redirect('payment_details', cause_id=cause.id)

    return render(request, "dashboard/choose_payment.html", {
        "cause": cause,
        "amount": amount
    })

from django.contrib.contenttypes.models import ContentType

def payment_details(request, cause_id):
    cause = get_object_or_404(DonationCause, id=cause_id)
    amount = request.session.get('donation_amount')
    payment_type = request.session.get('payment_type')
    crypto_currency = request.session.get('crypto_currency', None)

    if not amount or not payment_type:
        return redirect('choose_payment', cause_id=cause.id)

    # Select random account based on type (and currency for crypto)
    account = None
    if payment_type == 'bank':
        account = BankAccount.objects.filter(is_active=True).order_by('?').first()
    elif payment_type == 'crypto':
        qs = CryptoWallet.objects.filter(is_active=True)
        if crypto_currency:
            qs = qs.filter(currency=crypto_currency)
        account = qs.order_by('?').first()
    elif payment_type == 'paypal':
        account = PayPalAccount.objects.filter(is_active=True).order_by('?').first()

    if not account:
        return render(request, "dashboard/payment_details.html", {
            "cause": cause,
            "amount": amount,
            "error": "No active account available for this payment method"
        })

    if request.method == "POST":
        donation = Donation.objects.create(
            cause=cause,
            amount=amount,
            payment_type=payment_type,
            payment_account_type=ContentType.objects.get_for_model(account),
            payment_account_id=account.id
        )
        return render(request, "dashboard/donation_success.html", {
            "donation": donation,
            "account_details": account,
            "payment_type": payment_type
        })

    return render(request, "dashboard/payment_details.html", {
        "cause": cause,
        "amount": amount,
        "account": account,
        "payment_type": payment_type
    })

def causes_page(request):
    causes = DonationCause.objects.all()

    context = {
        'causes': causes
    }
    return render(request, 'dashboard/causes_page.html', context)

def donor_details(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if request.method == "POST":
        donation.donor_name = request.POST.get("name")
        donation.donor_email = request.POST.get("email")
        donation.note = request.POST.get("note")
        donation.save()

        return redirect("donation_thank_you")

    return render(request, "dashboard/donor_details.html", {"donation": donation})

def donation_thank_you(request):
    return render(request, "dashboard/donation_thank_you.html")