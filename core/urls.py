from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("donations/", views.donation_dashboard, name="donation_dashboard"),
    path("donation-cause/", views.donation_causes, name="donation_causes"),
    path("donation-cause/add/", views.add_donation_cause, name="add_donation_cause"),
    path("donation-cause/edit/<int:cause_id>/", views.edit_donation_cause, name="edit_donation_cause"),
    path("donation-cause/delete/<int:cause_id>/", views.delete_donation_cause, name="delete_donation_cause"),


    path("donate/<int:cause_id>/", views.donate_amount, name="donate_amount"),
    path("donate/<int:cause_id>/payment/", views.choose_payment, name="choose_payment"),
]
