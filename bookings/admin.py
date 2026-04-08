from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "room",
        "phone",
        "check_in",
        "check_out",
        "guests_count",
        "status",
        "created_at",
    )
    list_filter = ("status", "check_in", "check_out", "room")
    search_fields = ("full_name", "phone", "comment")