from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="Dell_chhinna").exists():
            User.objects.create_superuser("Dell_chhinna", "chinmaybharti00@gmail.com", "Dell_chhinna")
