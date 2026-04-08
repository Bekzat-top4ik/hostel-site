from django.contrib import admin
from .models import Room, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "price_per_night", "capacity", "is_active", "created_at")
    list_filter = ("is_active", "capacity")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [RoomImageInline]