from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a default in-store user after first migration"

    def handle(self, *args, **options):
        User = get_user_model()
        email = "customer@venella.com"
        if not User.objects.filter(email=email).exists():
            from core.models.profiles import Profile

            # Create a default profile for the in-store user
            profile, created = Profile.objects.get_or_create(
                first_name="In",
                last_name="Store",
            )
            customer = User.objects.create_user(
                email=email,
                password="customer123",
                role="customer",
                profile=profile,
                is_active=True,
            )
            customer.set_password("customer123")
            customer.save()

            self.stdout.write(self.style.SUCCESS(f"User {email} created."))
        else:
            self.stdout.write(self.style.WARNING(f"User {email} already exists."))
