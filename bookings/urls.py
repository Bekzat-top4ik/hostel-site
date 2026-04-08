from django.urls import path

from .views import booking_create_view, booking_success_view

app_name = "bookings"

urlpatterns = [
    path("", booking_create_view, name="booking_create"),
    path("success/", booking_success_view, name="booking_success"),
    path("room/<slug:slug>/", booking_create_view, name="booking_create_for_room"),
]