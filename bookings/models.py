from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

from rooms.models import Room


phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{9,15}$",
    message="Введите корректный номер телефона."
)


class Booking(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="bookings"
    )
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    check_in = models.DateField()
    check_out = models.DateField()
    guests_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.full_name} - {self.room.title} ({self.check_in} / {self.check_out})"

    def clean(self):
        today = timezone.localdate()

        if self.check_in and self.check_in < today:
            raise ValidationError({"check_in": "Дата заезда не может быть в прошлом."})

        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError({"check_out": "Дата выезда должна быть позже даты заезда."})

        if self.room_id and self.guests_count and self.guests_count > self.room.capacity:
            raise ValidationError({"guests_count": "Количество гостей превышает вместимость номера."})

        if self.room_id and self.check_in and self.check_out:
            overlapping = Booking.objects.filter(
                room=self.room,
                status__in=[Booking.Status.NEW, Booking.Status.CONFIRMED],
                check_in__lt=self.check_out,
                check_out__gt=self.check_in,
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError("Этот номер уже занят на выбранные даты.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
