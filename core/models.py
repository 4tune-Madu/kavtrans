from django.db import models


#Donation cause

from django.db import models

class DonationCause(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='donations/')
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



class Donation(models.Model):
    cause = models.ForeignKey('DonationCause', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_account = models.ForeignKey('PaymentAccount', on_delete=models.SET_NULL, null=True)

    donor_name = models.CharField(max_length=255, blank=True, null=True)
    donor_email = models.EmailField(blank=True, null=True)

    proof = models.ImageField(upload_to='donation_proofs/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount}"

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