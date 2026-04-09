from django.db import models


#Donation cause

from django.db import models
from cloudinary.models import CloudinaryField

class DonationCause(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)  # <- use CloudinaryField
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percentage(self):
        if self.target_amount > 0:
            return round((self.amount_raised / self.target_amount) * 100, 2)
        return 0

    def __str__(self):
        return self.title



from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Donation(models.Model):
    cause = models.ForeignKey(DonationCause, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=20)

    donor_name = models.CharField(max_length=255, blank=True, null=True)
    donor_email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    # Generic relation to any account type
    payment_account_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    payment_account_id = models.PositiveIntegerField()
    payment_account = GenericForeignKey('payment_account_type', 'payment_account_id')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cause.title} - {self.amount} via {self.payment_type}"

import random



class PaymentAccount(models.Model):

    ACCOUNT_TYPES = [
        ('bank', 'Bank Transfer'),
        ('crypto', 'Crypto'),
        ('paypal', 'PayPal'),
    ]

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    name = models.CharField(max_length=255)
    details = models.TextField()  # account number, wallet, email, etc.
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.account_type})"

# Bank Accounts
class BankAccount(models.Model):
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default='USD')
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_name}"

# Crypto Wallets
class CryptoWallet(models.Model):
    CURRENCY_CHOICES = [
        ('BTC','Bitcoin'),
        ('ETH','Ethereum'),
        ('USDT','USDT'),
        ('TRON','TRON')
    ]
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    wallet_address = models.CharField(max_length=200)
    network = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.currency} - {self.wallet_address[:10]}..."

# PayPal Accounts
class PayPalAccount(models.Model):
    email = models.EmailField()
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    full_description = models.TextField()

    image = models.ImageField(upload_to='services/', blank=True, null=True)

    # Optional extras (very useful)
    feature_1 = models.CharField(max_length=200, blank=True)
    feature_2 = models.CharField(max_length=200, blank=True)
    feature_3 = models.CharField(max_length=200, blank=True)
    feature_4 = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title



from django.db import models
from cloudinary.models import CloudinaryField
###Endoresement section.

class CelebrityEndorsement(models.Model):
    """
    A celebrity or notable figure publicly endorsing KAVTRANS donation causes.
    Uploaded and managed entirely from the Django admin dashboard.
    """

    name = models.CharField(
        max_length=150,
        help_text="Full name or stage name of the endorser (e.g. 'Burna Boy')"
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Their title or profession (e.g. 'Grammy Award-winning Artist')"
    )

    image = CloudinaryField(
    'image',
    folder='endorsements',
    help_text="Professional photo..."
)

    quote = models.TextField(
        help_text="Their endorsement statement or comment about the cause"
    )

    cause = models.ForeignKey(
        'DonationCause',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='endorsements',
        help_text="Optionally link this endorsement to a specific cause"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this endorsement from the public page without deleting it"
    )

    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first. Use this to control display order."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Celebrity Endorsement'
        verbose_name_plural = 'Celebrity Endorsements'

    def __str__(self):
        return f"{self.name} — {self.title or 'Endorser'}"