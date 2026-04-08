from django.shortcuts import get_object_or_404, render

from .models import Room


def room_list_view(request):
    rooms = Room.objects.filter(is_active=True).prefetch_related("images")
    return render(request, "rooms/room_list.html", {"rooms": rooms})


def room_detail_view(request, slug):
    room = get_object_or_404(
        Room.objects.prefetch_related("images"),
        slug=slug,
        is_active=True,
    )
    return render(request, "rooms/room_detail.html", {"room": room})