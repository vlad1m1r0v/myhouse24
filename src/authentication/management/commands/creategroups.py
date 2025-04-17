from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create groups for staff"

    def handle(self, *args, **options):
        if Group.objects.all().count() == 5:
            self.stdout.write(self.style.SUCCESS("Groups already exist"))
            return
        else:
            Group.objects.all().delete()

            Group.objects.bulk_create([
                Group(name="Директор"),
                Group(name="Керуючий"),
                Group(name="Бухгалтер"),
                Group(name="Електрик"),
                Group(name="Сантехнік")
            ])

        self.stdout.write(self.style.SUCCESS("Groups created successfully"))
