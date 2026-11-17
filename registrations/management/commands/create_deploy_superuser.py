import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create production superuser if it does not exist"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write("Superuser environment variables missing.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists. Skipping.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Production superuser created successfully.")
        )
