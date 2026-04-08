from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from rooms.models import Room
from .forms import BookingForm
from .utils import send_telegram_message


def booking_create_view(request, slug=None):
    room = None

    if slug:
        room = get_object_or_404(Room, slug=slug, is_active=True)

    if request.method == "POST":
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            booking = form.save()

            message = (
                f"Новая заявка!\n\n"
                f"Имя: {booking.full_name}\n"
                f"Телефон: {booking.phone}\n"
                f"Номер: {booking.room.title}\n"
                f"Гости: {booking.guests_count}\n"
                f"Заезд: {booking.check_in}\n"
                f"Выезд: {booking.check_out}\n"
                f"Комментарий: {booking.comment or '—'}"
            )

            send_telegram_message(message)

            messages.success(request, "Заявка успешно отправлена.")
            return redirect(reverse("bookings:booking_success") + f"?id={booking.id}")
    else:
        form = BookingForm(room=room)

    return render(request, "bookings/booking_form.html", {
        "form": form,
        "room": room,
    })


def booking_success_view(request):
    booking_id = request.GET.get("id")
    return render(request, "bookings/booking_success.html", {
        "booking_id": booking_id,
    })