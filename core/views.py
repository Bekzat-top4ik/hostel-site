from django.shortcuts import render

from rooms.models import Room


def home_view(request):
    rooms = Room.objects.filter(is_active=True).prefetch_related("images")[:6]
    return render(request, "core/home.html", {"rooms": rooms})