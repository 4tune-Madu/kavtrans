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


from django.contrib import admin
from django.utils.html import format_html
from .models import CelebrityEndorsement


@admin.register(CelebrityEndorsement)
class CelebrityEndorsementAdmin(admin.ModelAdmin):
    """
    Admin panel for managing celebrity/notable endorsements on the donation page.
    """

    list_display  = ('endorser_preview', 'name', 'title', 'cause', 'is_active', 'display_order', 'created_at')
    list_editable = ('is_active', 'display_order')
    list_filter   = ('is_active', 'cause')
    search_fields = ('name', 'title', 'quote')
    ordering      = ('display_order', '-created_at')

    fieldsets = (
        ('Endorser Identity', {
            'fields': ('name', 'title', 'image'),
            'description': 'Upload a high-quality portrait image and enter the endorser\'s full name and role.'
        }),
        ('Endorsement Content', {
            'fields': ('quote', 'cause'),
            'description': 'The statement they are making and optionally which specific cause they are endorsing.'
        }),
        ('Visibility & Order', {
            'fields': ('is_active', 'display_order'),
            'description': 'Control whether this appears on the site and in what order relative to others.'
        }),
    )

    def endorser_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid #ff6b00;" />',
                obj.image.url
            )
        return '—'

    endorser_preview.short_description = 'Photo'