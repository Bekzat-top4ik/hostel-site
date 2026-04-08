from decimal import Decimal

from django.core.management.base import BaseCommand

from rooms.models import Room


ROOMS = [
    {
        "title": "Standard Single",
        "short_description": "Уютный одноместный номер для спокойного отдыха.",
        "description": (
            "Комфортный номер для одного гостя. "
            "Подходит для коротких поездок, командировок и спокойного отдыха. "
            "В номере удобная кровать, базовая мебель и приятная атмосфера."
        ),
        "price_per_night": Decimal("1800.00"),
        "capacity": 1,
    },
    {
        "title": "Standard Double",
        "short_description": "Удобный двухместный номер с базовым комфортом.",
        "description": (
            "Практичный номер для двух гостей. "
            "Хороший вариант для друзей, пары или путешественников, "
            "которым нужен чистый и удобный номер по честной цене."
        ),
        "price_per_night": Decimal("2500.00"),
        "capacity": 2,
    },
    {
        "title": "Comfort Double",
        "short_description": "Просторный номер с повышенным уровнем комфорта.",
        "description": (
            "Более просторный и удобный номер для двух гостей. "
            "Подходит для тех, кто хочет чуть больше уюта, "
            "комфорта и свободного пространства."
        ),
        "price_per_night": Decimal("3200.00"),
        "capacity": 2,
    },
    {
        "title": "Family Room",
        "short_description": "Семейный номер для комфортного размещения нескольких гостей.",
        "description": (
            "Большой номер для семьи или небольшой группы гостей. "
            "Подходит для длительного проживания, отдыха с близкими "
            "и удобного размещения нескольких человек."
        ),
        "price_per_night": Decimal("4200.00"),
        "capacity": 4,
    },
]


class Command(BaseCommand):
    help = "Создает стартовые номера для проекта"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for room_data in ROOMS:
            room, created = Room.objects.update_or_create(
                title=room_data["title"],
                defaults={
                    "short_description": room_data["short_description"],
                    "description": room_data["description"],
                    "price_per_night": room_data["price_per_night"],
                    "capacity": room_data["capacity"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Создан номер: {room.title}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Обновлен номер: {room.title}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Создано: {created_count}, обновлено: {updated_count}"
            )
        )