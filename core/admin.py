from django.contrib import admin

#Donation cause
from .models import DonationCause

admin.site.register(DonationCause)


from .models import PaymentAccount

admin.site.register(PaymentAccount)