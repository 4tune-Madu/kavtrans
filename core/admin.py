from django.contrib import admin

#Donation cause
from .models import DonationCause

admin.site.register(DonationCause)


from django.contrib import admin
from .models import PaymentAccount, BankAccount, CryptoWallet, PayPalAccount

# 1. Register the generic PaymentAccount if needed
#@admin.register(PaymentAccount)
#class PaymentAccountAdmin(admin.ModelAdmin):
#    list_display = ('name', 'account_type', 'is_active')
#    list_filter = ('account_type', 'is_active')
#    search_fields = ('name', 'details')

# 2. Register BankAccount with full fields
@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_name', 'account_number', 'branch', 'swift_code', 'currency', 'is_active')
    list_filter = ('bank_name', 'is_active', 'currency')
    search_fields = ('bank_name', 'account_name', 'account_number', 'branch', 'swift_code')

# 3. Register CryptoWallet
@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ('currency', 'wallet_address', 'network', 'is_active')
    list_filter = ('currency', 'is_active')
    search_fields = ('wallet_address', 'network')

# 4. Register PayPalAccount
@admin.register(PayPalAccount)
class PayPalAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_active',)

from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}