from django.urls import path
from . import views


urlpatterns = [

    path("login/", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),
    
    path("", views.dashboard_home, name="dashboard_home"),

    path("packages/create/", views.package_create, name="package_create"),
    path("packages/", views.package_list, name="package_list"),
    path("packages/<int:package_id>/", views.package_detail, name="package_detail"),
    
    path("donations/", views.donations, name="donations"),
    path("donate/<int:cause_id>/", views.donate_to_cause, name="donate_to_cause"),

    path('payment-accounts/', views.payment_accounts, name='payment_accounts'),
    path('payment-accounts/delete/<int:id>/', views.delete_payment_account, name='delete_payment_account'),


    # Payment Accounts (Dashboard)
    path("payment-accounts/", views.payment_accounts, name="payment_accounts"),
    path("payment-accounts/add/", views.add_payment_account, name="add_payment_account"),
    path("payment-accounts/edit/<int:id>/", views.edit_payment_account, name="edit_payment_account"),
    path("payment-accounts/delete/<int:id>/", views.delete_payment_account, name="delete_payment_account"),

]