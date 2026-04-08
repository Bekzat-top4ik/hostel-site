from django.urls import path

from .views import room_detail_view, room_list_view

app_name = "rooms"

urlpatterns = [
    path("", room_list_view, name="room_list"),
    path("<slug:slug>/", room_detail_view, name="room_detail"),
]