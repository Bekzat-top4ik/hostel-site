from django import forms

from rooms.models import Room
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "room",
            "full_name",
            "phone",
            "check_in",
            "check_out",
            "guests_count",
            "comment",
        ]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "comment": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        room = kwargs.pop("room", None)
        super().__init__(*args, **kwargs)

        self.fields["room"].queryset = Room.objects.filter(is_active=True)

        self.fields["full_name"].widget.attrs.update({
            "placeholder": "Введите ваше имя"
        })
        self.fields["phone"].widget.attrs.update({
            "placeholder": "+996555123456"
        })
        self.fields["check_in"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["check_out"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["guests_count"].widget.attrs.update({
            "min": 1,
            "placeholder": "Например: 2"
        })
        self.fields["comment"].widget.attrs.update({
            "placeholder": "Дополнительные пожелания"
        })

        if room is not None:
            self.fields["room"].initial = room
            self.fields["room"].widget = forms.HiddenInput()