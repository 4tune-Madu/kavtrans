from django.urls import path
from . import views

urlpatterns = [
    path(
        "updates/<str:tracking_number>/",
        views.tracking_updates,
        name="tracking_updates"
    ),

    path(
        "add-update/<str:tracking_number>/",
        views.add_tracking_update,
        name="add_tracking_update"
    ),

    path('tracking/update/edit/<int:update_id>/', views.edit_tracking_update, name='edit_tracking_update'),
    path('tracking/update/delete/<int:update_id>/', views.delete_tracking_update, name='delete_tracking_update'),
]